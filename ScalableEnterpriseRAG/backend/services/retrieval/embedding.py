
import asyncio
import vertexai
from vertexai.language_models import TextEmbeddingModel
from backend.config import settings

model = None
BATCH_SIZE = 50

def get_embedding_model():
    global model
    if model is None:
        vertexai.init(project=settings.PROJECT_ID, location=settings.LOCATION)
        model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    return model

def embed_query(query: str):
    """Embeds a single query string (sync — used by retrieval path)."""
    m = get_embedding_model()
    embeddings = m.get_embeddings([query])
    return embeddings[0].values

async def embed_texts(texts: list[str]) -> list:
    """
    Embeds a list of text strings.
    All batches are sent concurrently via asyncio.gather.
    """
    m = get_embedding_model()
    batches = [texts[i:i + BATCH_SIZE] for i in range(0, len(texts), BATCH_SIZE)]

    async def embed_batch(batch: list[str]):
        return await asyncio.to_thread(m.get_embeddings, batch)

    results = await asyncio.gather(*[embed_batch(b) for b in batches])
    return [e.values for result in results for e in result]
