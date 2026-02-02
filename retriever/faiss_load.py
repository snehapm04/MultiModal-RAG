import faiss
import numpy as np

import faiss
import os

def build_index(vectors, path):

    os.makedirs(os.path.dirname(path), exist_ok=True)

    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    faiss.write_index(index, path)


def search(path, query, k=5):
    index = faiss.read_index(path)
    D,I = index.search(query,k)
    return I
