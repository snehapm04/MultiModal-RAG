import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from sentence_transformers import SentenceTransformer

# Lightweight text model
text_model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L3-v2")

clip = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def embed_text(texts):
    return text_model.encode(texts, convert_to_numpy=True)

def embed_images(paths):
    import numpy as np

    valid_images = []

    for p in paths:
        try:
            img = Image.open(p).convert("RGB")
            # Skip tiny junk images
            if img.size[0] < 50 or img.size[1] < 50:
                continue
            valid_images.append(img)
        except Exception:
            continue

    if len(valid_images) == 0:
        return None

    inputs = clip_processor(images=valid_images, return_tensors="pt")

    with torch.no_grad():
        outputs = clip.get_image_features(**inputs)

        # Support multiple possible output types from transformers' CLIPModel
        if isinstance(outputs, torch.Tensor):
            image_features = outputs
        elif hasattr(outputs, "image_embeds"):
            image_features = outputs.image_embeds
        elif hasattr(outputs, "pooler_output"):
            image_features = outputs.pooler_output
        elif hasattr(outputs, "last_hidden_state"):
            # mean-pool the sequence dimension as a fallback
            image_features = outputs.last_hidden_state.mean(dim=1)
        elif isinstance(outputs, (list, tuple)) and len(outputs) > 0 and isinstance(outputs[0], torch.Tensor):
            image_features = outputs[0]
        else:
            raise ValueError(f"Unsupported output type from CLIPModel.get_image_features: {type(outputs)}")

    # Convert features to numpy array
    if isinstance(image_features, torch.Tensor):
        return image_features.detach().cpu().numpy()
    else:
        return np.asarray(image_features)

