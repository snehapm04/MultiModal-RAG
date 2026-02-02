import os
from PIL import Image
import fitz

def extract_images(doc, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    paths = []

    for i, page in enumerate(doc):
        for j, img in enumerate(page.get_images()):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            path = f"{out_dir}/page{i}_{j}.png"
            pix.save(path)
            paths.append((i, path))

    return paths
