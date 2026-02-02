from config import CHUNK_SIZE, OVERLAP

def chunk_text(text):
    words = text.split()
    chunks = []
    for i in range(0, len(words), CHUNK_SIZE-OVERLAP):
        chunks.append(" ".join(words[i:i+CHUNK_SIZE]))
    return chunks
