# HireSense AI Architecture

## Overview
HireSense AI is designed using a modern micro-core architecture with a decoupled React frontend and a Python FastAPI backend acting as the AI orchestration layer. The system is built to parse unstructured resumes, extract semantic meaning using Dense Vector Embeddings, and simulate Applicant Tracking Systems (ATS).

## System Components

### 1. Frontend Client (React + Vite + Tailwind)
- **Framework**: React 18, Vite (for rapid HMR and optimized builds).
- **Styling**: Tailwind CSS (Glassmorphism, dark mode default for premium UI/UX).
- **Data Visualization**: Recharts (for multi-dimensional Radar charts and circular progress rings).
- **Role**: Handles document upload formatting, JD matching input, and asynchronous rendering of Explainable AI (XAI) insights.

### 2. API Gateway (FastAPI)
- **Framework**: FastAPI (Pydantic v2, Async native).
- **Role**: Validates incoming file blobs, assigns parsed data to the right NLP modules, and enforces strict type contracts (`schemas.py`).

### 3. AI Pipeline Layer
- **Document Parsers**: Abstracted via a Factory (`factory.py`) utilizing `PyMuPDF` for PDF layout-aware parsing and `python-docx` for Office parsing.
- **Entity Extractor**: Spacy `en_core_web_sm` model for standard NER (Named Entity Recognition - Names, Links).
- **Semantic Skill Graph**: 
  - Uses `SentenceTransformers` (`all-MiniLM-L6-v2`) to encode resume tokens densely.
  - Caches an index of normalized skills in `FAISS` (Facebook AI Similarity Search).
  - Normalizes ad-hoc skills (e.g., "PyTorch") to their domain nodes (e.g., "Machine Learning Framework").
- **Job Match Scorer**: Computes the exact cosine similarity distance between the Resume Embeddings and Job Description Embeddings to define the "Experience Match".
- **ATS Simulator**: Emulates older ATS systems by parsing for standard structural integrity, action verb frequencies, and keyword density.
- **Explainable AI (XAI) Engine**: Converts numeric Euclidean distances into natural language justifications so candidates understand *why* they scored a 78/100.

## Infrastructure & Scalability
- **Vector Search**: Local `FAISS` index.
- **Deployment**: containerized via `Docker` and `Docker Compose`, allowing for 1-click execution.
