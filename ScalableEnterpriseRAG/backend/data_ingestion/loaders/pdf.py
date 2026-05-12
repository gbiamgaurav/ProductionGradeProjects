
import io
import asyncio
import logfire
from pypdf import PdfReader, PdfWriter
from google.cloud import documentai
from backend.config import settings

client = documentai.DocumentProcessorServiceClient()
MAX_PAGES_PER_REQUEST = 15

# Global semaphore: max 5 concurrent Document AI calls across all files
_doc_ai_semaphore: asyncio.Semaphore | None = None

def _get_semaphore() -> asyncio.Semaphore:
    global _doc_ai_semaphore
    if _doc_ai_semaphore is None:
        _doc_ai_semaphore = asyncio.Semaphore(5)
    return _doc_ai_semaphore


async def parse_pdf(file_path: str) -> str:
    """
    Parses a PDF using Google Cloud Document AI.
    Page chunks are sent concurrently (up to 5 at a time globally).
    """
    with logfire.span("📄 Document AI Parsing", filename=file_path):
        try:
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)
            logfire.info(f"Total pages: {total_pages}")

            name = client.processor_path(
                settings.PROJECT_ID,
                settings.GCP_DOC_AI_LOCATION,
                settings.GCP_DOC_AI_PROCESSOR_ID
            )

            if total_pages <= MAX_PAGES_PER_REQUEST:
                with open(file_path, "rb") as f:
                    image_content = f.read()
                async with _get_semaphore():
                    full_text = await asyncio.to_thread(process_document_chunk, image_content, name)
            else:
                logfire.info(f"PDF exceeds {MAX_PAGES_PER_REQUEST} pages. Splitting into chunks...")

                # Build all page-chunk byte payloads up front (fast, CPU-bound)
                chunk_payloads = []
                for i in range(0, total_pages, MAX_PAGES_PER_REQUEST):
                    end = min(i + MAX_PAGES_PER_REQUEST, total_pages)
                    writer = PdfWriter()
                    for page_num in range(i, end):
                        writer.add_page(reader.pages[page_num])
                    with io.BytesIO() as bs:
                        writer.write(bs)
                        chunk_payloads.append((i + 1, end, bs.getvalue()))

                async def process_range(start: int, end: int, chunk_bytes: bytes) -> str:
                    async with _get_semaphore():
                        with logfire.span(f"Processing pages {start} to {end}"):
                            return await asyncio.to_thread(
                                process_document_chunk, chunk_bytes, name
                            )

                results = await asyncio.gather(
                    *[process_range(s, e, b) for s, e, b in chunk_payloads]
                )
                full_text = "\n".join(results)

            if not full_text.strip():
                logfire.warning(f"⚠️ Document AI returned empty text for {file_path}")
            else:
                logfire.info(f"✅ Document AI successfully parsed {len(full_text)} characters")

            return full_text

        except Exception as e:
            logfire.error(f"❌ Document AI Parse Failed: {e}")
            logfire.info("💡 Ensure the Processor ID is correct and the API is enabled.")
            raise


def process_document_chunk(image_content: bytes, name: str) -> str:
    """Sends a PDF byte chunk to Document AI and returns extracted text."""
    raw_document = documentai.RawDocument(
        content=image_content,
        mime_type="application/pdf"
    )
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    return result.document.text
