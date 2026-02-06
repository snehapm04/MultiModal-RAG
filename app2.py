"""
Multimodal RAG Chatbot - Flask Web Server
Serves a beautiful HTML/CSS/JS frontend for document Q&A
"""

from flask import Flask, render_template, request, jsonify
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_classic.chains import RetrievalQA
import tempfile
import os
import traceback
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, static_folder='static', template_folder='static')

# Global state
qa_chain = None
embeddings = None

@app.route('/')
def index():
    """Serve the main chatbot UI"""
    return app.send_static_file('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_pdfs():
    """Upload and index PDFs"""
    global qa_chain, embeddings
    
    try:
        files = request.files.getlist('files')
        if not files:
            return jsonify({'error': 'No files provided'}), 400

        docs = []
        temp_files = []
        
        # Load and parse PDFs
        for file in files:
            if file.filename.endswith('.pdf'):
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                    file.save(tmp.name)
                    temp_files.append(tmp.name)
                    loader = PyPDFLoader(tmp.name)
                    docs.extend(loader.load())

        if not docs:
            return jsonify({'error': 'No valid PDFs uploaded'}), 400

        # Clean up temp files
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass  # File may be locked, ignore on Windows

        # Split documents
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )
        splits = splitter.split_documents(docs)

        # Create embeddings if not exists
        if embeddings is None:
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

        # Create FAISS index
        vectordb = FAISS.from_documents(splits, embeddings)

        # Create LLM chain
        llm = Ollama(model="llama3")
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vectordb.as_retriever()
        )

        return jsonify({'success': True, 'message': f'Indexed {len(files)} PDF(s)'})

    except Exception as e:
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        logging.error(error_msg)
        return jsonify({'error': str(e), 'details': error_msg}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Answer a query using the indexed documents"""
    global qa_chain
    
    try:
        if qa_chain is None:
            return jsonify({'error': 'No documents loaded. Please upload PDFs first.'}), 400

        data = request.json
        query = data.get('query', '').strip()

        if not query:
            return jsonify({'error': 'Empty query'}), 400

        # Get answer
        result = qa_chain.run(query)

        return jsonify({'answer': result})

    except Exception as e:
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        logging.error(error_msg)
        return jsonify({'error': str(e), 'details': error_msg}), 500

# Override send_static_file to handle index.html
@app.route('/<path:filename>')
def serve_static(filename):
    return app.send_static_file(filename)

if __name__ == '__main__':
    print("🚀 Multimodal RAG Chatbot running on http://localhost:5000")
    app.run(debug=True, port=5000, use_reloader=False)
