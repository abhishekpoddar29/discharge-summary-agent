from typing import List

def chunk_text(
    text: str,
    chunk_size: int = 4000,
    overlap: int = 500
    ) -> List[str]:
    """
    Split large OCR text into overlapping chunks.

    Args:
        text: Full OCR extracted text
        chunk_size: Maximum characters per chunk
        overlap: Characters shared between chunks

    Returns:
        List of text chunks
    """

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += (chunk_size - overlap)

    return chunks

