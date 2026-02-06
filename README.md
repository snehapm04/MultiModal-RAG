# Multimodal Retrieval-Augmented Generation (RAG) System

A sophisticated multimodal retrieval-augmented generation (RAG) system designed to extract, process, and query content from diverse document formats including PDFs, images, and tables. The system leverages FAISS indexing technology to provide efficient similarity search and retrieval across multiple modalities.

## Overview

This project implements a comprehensive RAG pipeline that enables users to extract content from various document types, generate embeddings, build searchable indexes, and perform intelligent queries against the indexed content. The system supports both multimodal and text-only interfaces to accommodate different use cases and requirements.

## Key Features

- **Multimodal Content Extraction**: Advanced processing capabilities for extracting text, images, and tables from PDF documents
- **Intelligent Document Chunking**: Sophisticated text segmentation algorithms for optimal retrieval performance
- **Cross-Modal Embeddings**: High-dimensional vector representations for text and image content
- **FAISS Indexing**: Efficient similarity search using Facebook AI Similarity Search (FAISS) technology
- **Dual Application Interfaces**: Both multimodal Streamlit UI and text-focused chat interface
- **Flexible Query Processing**: Natural language querying over indexed content with citation support

## System Architecture

The system is organized into several key components:

- **Processor Layer**: Handles document loading, content extraction, and preprocessing
- **Embedding Engine**: Generates vector representations for different content modalities  
- **Index Management**: Creates and maintains FAISS indexes for fast retrieval
- **Query Interface**: Processes user queries and retrieves relevant content
- **Response Generation**: Composes contextual answers with proper citations

## Prerequisites

- Python 3.8 or higher
- Sufficient disk space for storing indexes and extracted content
- Access to required Python packages (see requirements.txt)

## Installation

1. Clone the repository and navigate to the project directory

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Data Preparation

1. Place source PDF documents in the `data/raw_pdfs/` directory

2. The system will automatically generate:
   - Extracted images in `data/extracted_images/`
   - Extracted tables in `data/extracted_tables/` (as CSV files)

## Pipeline Execution

Execute the processing pipeline in the following order:

1. **Content Extraction and Processing**:
   ```bash
   python processor/pdf_loader.py
   python processor/img_extractor.py
   python processor/table_extractor.py
   python processor/chunker.py
   ```

2. **Embedding Generation and Index Creation**:
   ```bash
   python retriever/embed.py
   python retriever/faiss_load.py
   ```

## Application Deployment

The system offers two distinct interfaces for interacting with the indexed content:

### Multimodal Interface ([app.py](app.py))
- **Technology**: Streamlit-based web application
- **Purpose**: Full multimodal RAG capabilities with interactive UI
- **Features**: Supports various document types, rich media queries, and comprehensive visualization
- **Deployment**: `streamlit run app.py`
- **Best For**: Users requiring full system functionality with multimodal support

### Text-Only Interface ([app2.py](app2.py))
- **Technology**: Lightweight text-based chat interface
- **Purpose**: Focused querying of text content extracted from PDFs
- **Features**: Streamlined text search, rapid response times, simplified interaction
- **Deployment**: `python app2.py`
- **Best For**: Users seeking quick text-based queries without multimodal features

## Directory Structure

```
├── processor/           # Content extraction and preprocessing modules
│   ├── pdf_loader.py    # PDF document loader and parser
│   ├── img_extractor.py # Image extraction from documents
│   ├── table_extractor.py # Table extraction and conversion utilities
│   ├── chunker.py       # Text segmentation algorithms
│   └── txt_extractor.py # Plain text extraction utilities
├── retriever/          # Embedding and indexing components
│   ├── embed.py        # Vector embedding generation
│   ├── faiss_load.py   # FAISS index creation and management
│   └── cross_modal.py  # Cross-modal retrieval algorithms
├── qa/                 # Query processing and answer generation
│   └── answer.py       # Response composition and formatting
├── utils/              # Supporting utility functions
│   └── citation.py     # Citation formatting and management
├── static/             # Frontend assets for web interfaces
│   ├── index.html      # HTML templates
│   ├── styles.css      # Styling sheets
│   └── chat.js         # Client-side JavaScript
├── data/               # Input and output data directories
│   ├── raw_pdfs/       # Source PDF documents
│   ├── extracted_images/ # Extracted image files
│   └── extracted_tables/ # Extracted table data (CSV)
├── faiss_indexes/      # Generated FAISS index files
├── app.py              # Streamlit multimodal interface
├── app2.py             # Text-only chat interface
├── config.py           # System configuration settings
└── requirements.txt    # Python package dependencies
```

## Data Management

- **Input Documents**: `data/raw_pdfs/`
- **Processed Images**: `data/extracted_images/`
- **Processed Tables**: `data/extracted_tables/` (CSV format)
- **Vector Indexes**: `faiss_indexes/` (text.index, image.index)

## Best Practices

- Always re-run embedding scripts after adding new content to update indexes
- Maintain consistent document quality for optimal extraction results
- Monitor disk space usage, especially when processing large document sets
- Rebuild FAISS indexes when changing embedding models or vector dimensions
- Use [app.py](app.py) for comprehensive multimodal interactions
- Use [app2.py](app2.py) for focused text-based queries and faster responses

## Performance Considerations

- Index building time scales with document volume
- Memory requirements increase with index size
- Query response times depend on index complexity and hardware resources
- Optimal chunk sizes typically range from 200-500 tokens for best retrieval performance

## Troubleshooting

- Ensure all required dependencies are installed via requirements.txt
- Verify input documents are in the correct directory (data/raw_pdfs/)
- Check that FAISS indexes are properly generated before querying
- Confirm Python version compatibility (3.8+ required)
