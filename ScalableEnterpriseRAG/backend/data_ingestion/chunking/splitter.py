
from typing import List
import logfire

def chunk_text(text: str, chunk_size: int = 1500) -> List[str]:
    """
    Splits text by paragraphs. If a single paragraph exceeds chunk_size,
    it is further split at the character level to stay within the limit.
    """
    with logfire.span("✂️ Text Chunking", text_length=len(text)):
        if not text.strip():
            return []

        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = ""

        for p in paragraphs:
            if len(current_chunk) + len(p) < chunk_size:
                current_chunk += p + "\n\n"
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                if len(p) > chunk_size:
                    # Paragraph itself is too large — split by characters
                    for k in range(0, len(p), chunk_size):
                        sub = p[k:k + chunk_size]
                        if sub.strip():
                            chunks.append(sub.strip())
                    current_chunk = ""
                else:
                    current_chunk = p + "\n\n"

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        valid_chunks = [c for c in chunks if c.strip()]
        logfire.info(f"✅ Generated {len(valid_chunks)} chunks")
        return valid_chunks
