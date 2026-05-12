
import os
import sys
import uuid
import json
import asyncio
import logfire
import vertexai
import tempfile

from typing import List
from google.cloud import storage
from qdrant_client import QdrantClient
from qdrant_client.http import models
from fastapi import FastAPI, Request, BackgroundTasks

from backend.config import settings
from backend.services.retrieval.embedding import embed_texts
from backend.data_ingestion.loaders.pdf import parse_pdf
from backend.data_ingestion.loaders.html import parse_html
from backend.data_ingestion.loaders.text import parse_text
from backend.data_ingestion.chunking.splitter import chunk_text

logfire.configure(service_name="enterprise-ingestion-service")
vertexai.init(project=settings.PROJECT_ID, location=settings.LOCATION)

storage_client = storage.Client(project=settings.PROJECT_ID)
qdrant_client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)

app = FastAPI()


# ---------------------------------------------------------------------------
# GCS helpers
# ---------------------------------------------------------------------------

def _sync_upload_to_gcs(data, bucket_name: str, blob_name: str, is_json: bool = False):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    if is_json:
        blob.upload_from_string(json.dumps(data), content_type="application/json")
    else:
        blob.upload_from_filename(data)


async def upload_to_gcs(data, bucket_name: str, blob_name: str, is_json: bool = False):
    with logfire.span("☁️ GCS Upload", bucket=bucket_name, blob=blob_name):
        try:
            await asyncio.to_thread(_sync_upload_to_gcs, data, bucket_name, blob_name, is_json)
            logfire.info(f"✅ Uploaded to {bucket_name}")
        except Exception as e:
            logfire.error(f"❌ GCS Upload Failed: {e}")


# ---------------------------------------------------------------------------
# Core file processor
# ---------------------------------------------------------------------------

async def process_file(
    file_path: str,
    filename: str,
    source_type: str,
    skip_raw_upload: bool = False,
    file_index: int = 0,
    total_files: int = 0,
) -> int:
    """
    Orchestrates parse → chunk → embed → index for a single file.
    Returns the number of vector points indexed (0 on failure or skip).
    """
    label = f"[{file_index}/{total_files}] {filename}" if total_files else filename

    with logfire.span("🚀 Processing File", file=filename, source=source_type,
                      progress=f"{file_index}/{total_files}"):
        try:
            raw_gcs_path = f"{source_type}/{filename}"

            if not skip_raw_upload:
                await upload_to_gcs(file_path, settings.RAW_BUCKET, raw_gcs_path)
            else:
                logfire.info(f"⏭️ Skipping RAW upload for {filename} (already in GCS)")

            ext = filename.lower().split(".")[-1]
            if ext == "pdf":
                full_text = await parse_pdf(file_path)
            elif ext in ("html", "htm"):
                full_text = await asyncio.to_thread(parse_html, file_path)
            elif ext == "txt":
                full_text = await asyncio.to_thread(parse_text, file_path)
            elif ext in ("docx", "pptx"):
                from backend.data_ingestion.loaders.office import parse_office
                full_text = await asyncio.to_thread(parse_office, file_path)
            else:
                logfire.warning(f"⏩ Skipping unsupported file type: {filename}")
                return 0

            if not full_text or not full_text.strip():
                logfire.warning(f"⚠️ No text extracted from {filename}")
                return 0

            chunks = chunk_text(full_text)
            if not chunks:
                return 0

            processed_data = {"filename": filename, "chunks": chunks, "source_type": source_type}
            processed_gcs_path = f"{source_type}/{filename}.json"
            await upload_to_gcs(processed_data, settings.PROCESSED_BUCKET, processed_gcs_path, is_json=True)

            with logfire.span("🧠 Vectorizing & Indexing", chunks=len(chunks)):
                logfire.info(f"📊 {label} — embedding {len(chunks)} chunks into {len(chunks)} vectors")
                embeddings = await embed_texts(chunks)

                points = [
                    models.PointStruct(
                        id=str(uuid.uuid4()),
                        vector=vector,
                        payload={
                            "text": chunk,
                            "source": filename,
                            "source_type": source_type,
                            "raw_gcs_path": f"gs://{settings.RAW_BUCKET}/{raw_gcs_path}",
                        },
                    )
                    for chunk, vector in zip(chunks, embeddings)
                ]

                await asyncio.to_thread(
                    qdrant_client.upsert,
                    collection_name=settings.QDRANT_COLLECTION,
                    points=points,
                )
                logfire.info(f"✨ Indexed {len(points)} points to Qdrant")
                return len(points)

        except Exception as e:
            logfire.error(f"💥 Failed to process {filename}: {e}")
            return 0


# ---------------------------------------------------------------------------
# Directory processor
# ---------------------------------------------------------------------------

async def process_directory(dir_path: str, source_type: str) -> int:
    files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    total = len(files)
    logfire.info(f"📂 Found {total} files to process — starting concurrent ingestion")

    semaphore = asyncio.Semaphore(5)  # max 5 files in-flight at once
    point_counts: list[int] = []

    async def bounded_process(idx: int, filename: str):
        async with semaphore:
            file_path = os.path.join(dir_path, filename)
            count = await process_file(
                file_path, filename, source_type,
                skip_raw_upload=False,
                file_index=idx,
                total_files=total,
            )
            point_counts.append(count)
            logfire.info(
                f"📈 Progress: {idx}/{total} files done — "
                f"{sum(point_counts)} total points indexed so far"
            )

    await asyncio.gather(*[bounded_process(i + 1, f) for i, f in enumerate(files)])

    total_points = sum(point_counts)
    logfire.info(f"✅ Directory complete: {total} files → {total_points} total points indexed")
    return total_points


# ---------------------------------------------------------------------------
# Universal ingestion entry point (CLI)
# ---------------------------------------------------------------------------

async def run_universal_ingestion(
    base_dir: str,
    explicit_source_type: str = None,
    wipe: bool = False,
):
    with logfire.span("🌍 Universal Ingestion Started", base_directory=base_dir):
        if wipe and qdrant_client.collection_exists(settings.QDRANT_COLLECTION):
            qdrant_client.delete_collection(settings.QDRANT_COLLECTION)
            logfire.info("🗑️ Wiped existing Qdrant collection")

        if not qdrant_client.collection_exists(settings.QDRANT_COLLECTION):
            qdrant_client.create_collection(
                collection_name=settings.QDRANT_COLLECTION,
                vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
            )
            logfire.info("✅ Created fresh Qdrant collection")

        subdirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

        if not subdirs:
            source_type = explicit_source_type or "general"
            await process_directory(base_dir, source_type)
        else:
            for subdir in subdirs:
                source_type = (
                    "true" if "true" in subdir.lower()
                    else "noisy" if "noisy" in subdir.lower()
                    else subdir
                )
                await process_directory(os.path.join(base_dir, subdir), source_type)


# ---------------------------------------------------------------------------
# Webhook (Eventarc) entry point
# ---------------------------------------------------------------------------

@app.post("/")
async def eventarc_webhook(request: Request, background_tasks: BackgroundTasks):
    try:
        data = await request.json()
        bucket = data.get("bucket")
        name = data.get("name")

        if not bucket or not name:
            logfire.error("❌ Invalid Eventarc payload")
            return {"status": "error", "message": "Invalid payload"}, 400

        logfire.info(f"📡 Eventarc Triggered: {name} in {bucket}")

        if bucket != settings.RAW_BUCKET:
            logfire.warning(f"🛑 Ignoring event from unauthorized bucket: {bucket}")
            return {"status": "ignored"}

        parts = name.split("/")
        source_type = parts[0] if len(parts) > 1 else "general"
        filename = parts[-1]

        background_tasks.add_task(process_from_gcs, bucket, name, filename, source_type)
        return {"status": "accepted", "file": name}

    except Exception as e:
        logfire.error(f"❌ Webhook Error: {e}")
        return {"status": "error"}, 500


async def process_from_gcs(bucket_name: str, blob_name: str, filename: str, source_type: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{filename}") as tmp:
        try:
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            await asyncio.to_thread(blob.download_to_filename, tmp.name)
            await process_file(tmp.name, filename, source_type, skip_raw_upload=True)
        finally:
            if os.path.exists(tmp.name):
                os.remove(tmp.name)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    wipe_requested = "--wipe" in sys.argv
    clean_args = [a for a in sys.argv if a != "--wipe"]
    target_dir = clean_args[1] if len(clean_args) > 1 else "DATA"
    explicit_type = clean_args[2] if len(clean_args) > 2 else None

    if os.path.exists(target_dir):
        asyncio.run(
            run_universal_ingestion(target_dir, explicit_source_type=explicit_type, wipe=wipe_requested)
        )
        logfire.info("🏁 Universal Ingestion Job Completed")
    else:
        print(f"Error: Path {target_dir} does not exist.")
