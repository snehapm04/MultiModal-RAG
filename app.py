import streamlit as st
import os

from processor.pdf_loader import load_pdf
from processor.txt_extractor import extract_text
from processor.img_extractor import extract_images
from processor.table_extractor import extract_tables
from processor.chunker import chunk_text

from retriever.embed import embed_text, embed_images
from retriever.faiss_load import build_index, search
from retriever.cross_modal import text_to_image
from qa.answer import generate

# ---------------- DIRS ----------------

os.makedirs("faiss_indexes", exist_ok=True)
os.makedirs("data/raw_pdfs", exist_ok=True)
os.makedirs("data/extracted_images", exist_ok=True)
os.makedirs("data/extracted_tables", exist_ok=True)

st.set_page_config(layout="wide")
st.title("📄 Multimodal RAG System")

# ---------------- SESSION ----------------

for k in [
    "text_chunks",
    "image_chunks",
    "table_chunks",
    "text_emb_done",
    "image_emb_done"
]:
    if k not in st.session_state:
        st.session_state[k] = []

# ---------------- SIDEBAR ----------------

st.sidebar.header("Pipeline")

st.sidebar.write("Text:", len(st.session_state.text_chunks))
st.sidebar.write("Images:", len(st.session_state.image_chunks))
st.sidebar.write("Tables:", len(st.session_state.table_chunks))

st.sidebar.divider()

st.sidebar.write("Text embedded:", bool(st.session_state.text_emb_done))
st.sidebar.write("Image embedded:", bool(st.session_state.image_emb_done))

READY = st.session_state.text_emb_done and st.session_state.image_emb_done

if READY:
    st.sidebar.success("✅ Ready for QnA")

# ---------------- UPLOAD ----------------

pdfs = st.file_uploader("Upload PDFs", accept_multiple_files=True)

# ---------------- STEP 1 ----------------

st.header("Step 1 — Extraction + Chunking")

col1, col2, col3 = st.columns(3)

# ---------- TEXT ----------

with col1:
    if st.button("📄 Chunk Text") and pdfs:

        st.session_state.text_chunks = []

        for pdf in pdfs:
            path = f"data/raw_pdfs/{pdf.name}"
            open(path, "wb").write(pdf.read())

            doc = load_pdf(path)
            pages = extract_text(doc)

            for _, text in pages:
                st.session_state.text_chunks += chunk_text(text)

        st.success("Text done")

# ---------- IMAGES ----------

with col2:
    if st.button("🖼 Extract Images") and pdfs:

        st.session_state.image_chunks = []

        for pdf in pdfs:
            path = f"data/raw_pdfs/{pdf.name}"
            doc = load_pdf(path)
            imgs = extract_images(doc, "data/extracted_images")

            for _, p in imgs:
                st.session_state.image_chunks.append(p)

        st.success("Images done")

# ---------- TABLES ----------

with col3:
    if st.button("📊 Extract Tables") and pdfs:

        st.session_state.table_chunks = []

        for pdf in pdfs:
            path = f"data/raw_pdfs/{pdf.name}"
            tables = extract_tables(path, "data/extracted_tables")

            for t in tables:
                st.session_state.table_chunks.append(open(t).read())

        st.success("Tables done")

# ---------------- STEP 2 ----------------

st.header("Step 2 — Embedding")

col4, col5 = st.columns(2)

with col4:
    if st.button("Embed Text + Tables"):

        combined = st.session_state.text_chunks + st.session_state.table_chunks

        with st.spinner("Embedding text..."):
            emb = embed_text(combined)
            build_index(emb, "faiss_indexes/text.index")

        st.session_state.text_emb_done = True
        st.success("Text embedded")

with col5:
    if st.button("Embed Images"):

        with st.spinner("Embedding images..."):
            emb = embed_images(st.session_state.image_chunks)
            build_index(emb, "faiss_indexes/image.index")

        st.session_state.image_emb_done = True
        st.success("Images embedded")

# ---------------- STEP 3 ----------------

st.divider()
st.header("💬 QnA")

if READY:

    query = st.text_input("Ask question")

    if st.button("Ask") and query:

        context = ""

        q = embed_text([query])
        idx = search("faiss_indexes/text.index", q)

        for i in idx[0]:
            if i < len(st.session_state.text_chunks):
                context += st.session_state.text_chunks[i] + "\n"

        imgs = text_to_image(query)

        st.subheader("Relevant Images")
        for i in imgs[0]:
            if i < len(st.session_state.image_chunks):
                st.image(st.session_state.image_chunks[i])

        answer = generate(context, query)
        st.markdown(answer)

else:
    st.info("Complete embedding first.")
