import torch
from retriever.embed import clip, clip_processor
from retriever.faiss_load import search

def text_to_image(query, k=5):

    inputs = clip_processor(text=[query], return_tensors="pt", padding=True)

    with torch.no_grad():
        text_outputs = clip.text_model(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"]
        )

        # CLS token pooling
        query_vec = text_outputs.last_hidden_state[:, 0, :]

        # Projection layer
        query_vec = clip.text_projection(query_vec)

    return search(
        "faiss_indexes/image.index",
        query_vec.cpu().numpy(),
        k
    )
