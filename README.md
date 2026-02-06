# Multimodal RAG

A small multimodal retrieval-augmented generation (RAG) project that extracts content from PDFs, images and tables, builds FAISS indexes, and provides query/QA over combined modalities.

**Features**
- Extract text, images and tables from PDFs
- Chunk and embed documents
- Build FAISS indexes for text and image embeddings
- Simple demo apps for querying the multimodal index

**Requirements**
- Python 3.8+
- See `requirements.txt` for full dependency list

**Quickstart**

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Prepare data
- Put source PDFs into `data/raw_pdfs/`.
- Extracted artifacts appear in `data/extracted_images/` and `data/extracted_tables/` after running the processor scripts.

3. Run processors to extract and chunk content

```bash
python processor/pdf_loader.py
python processor/img_extractor.py
python processor/table_extractor.py
python processor/chunker.py
```

4. Create embeddings and FAISS indexes

```bash
python retriever/embed.py
python retriever/faiss_load.py
```

5. Run the demo apps

```bash
python app2.py
# or run the Streamlit app
streamlit run app.py
```

**File Structure (key files)**
- [app2.py](app2.py): Lightweight demo/CLI app to query the system.
- [app.py](app.py): Streamlit demo UI.
- [requirements.txt](requirements.txt): Python dependencies.
- [processor/](processor/): PDF, image, table extraction and chunking helpers (`pdf_loader.py`, `img_extractor.py`, `table_extractor.py`, `chunker.py`).
- [retriever/](retriever/): Embedding and FAISS index creation (`embed.py`, `faiss_load.py`, `faiss_indexes/`).
- [qa/](qa/): Prompting and answer composition helpers.
- [utils/](utils/): Utility helpers such as citation formatting.

**Data & Indexes**
- Raw PDFs: `data/raw_pdfs/`
- Extracted images: `data/extracted_images/`
- Extracted tables: `data/extracted_tables/` (CSV files)
- FAISS indexes: `faiss_indexes/` (`text.index`, `image.index`)

**Usage notes & tips**
- The processor scripts assume PDFs are placed in `data/raw_pdfs/`.
- Re-run the embedding scripts after adding new chunks to update indexes.
- If you change the embedding model or vector size, you should rebuild the FAISS indexes.
