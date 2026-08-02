# 🧠 DocuMind AI – RAG Chatbot

An intelligent document question-answering application built using **Retrieval-Augmented Generation (RAG)**.

DocuMind AI allows users to upload PDF documents, process their content, search for relevant information, and ask questions based on the uploaded documents.

## 🚀 Live Demo

👉 **https://docmind2026.streamlit.app/**

## ✨ Features

- 📄 Upload one or multiple PDF documents
- 🔍 Extract text from PDF files
- 🧩 Split documents into smaller text chunks
- 🧠 Generate semantic embeddings using Sentence Transformers
- ⚡ Store and search embeddings using FAISS
- 🤖 Generate document-grounded answers using Google Gemini
- 📚 Display document sources and page numbers
- 💬 Interactive chat interface
- 📊 Knowledge Base overview
- 🟢 Document processing status
- 🎨 Modern and responsive Streamlit interface

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **PyPDF**
- **FAISS**
- **Sentence Transformers**
- **Google Gemini API**
- **NumPy**
- **Retrieval-Augmented Generation (RAG)**

## 🏗️ Project Architecture

```text
PDF Documents
     ↓
PDF Text Extraction
     ↓
Text Chunking
     ↓
Sentence Transformer Embeddings
     ↓
FAISS Vector Database
     ↓
Semantic Search
     ↓
Relevant Document Chunks
     ↓
Google Gemini
     ↓
Grounded Answer
