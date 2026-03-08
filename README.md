<h1 align="center">HireSense AI 🤖📄</h1>

<p align="center"><strong>World-Class Intelligent Resume Analyzer & ATS Simulator</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-18.2-61dafb.svg" alt="React">
  <img src="https://img.shields.io/badge/NLP-Spacy%20|%20Transformers-ff69b4.svg" alt="NLP">
  <img src="https://img.shields.io/badge/Vector%20Search-FAISS-red.svg" alt="FAISS">
</p>

## Overview

HireSense AI is a production-grade AI platform that goes beyond simple keyword matching. Built with **Semantic Vector Embeddings** and **Knowledge Graphs**, it understands the *intent* and *context* of a candidate's resume, predicting job-fit, predicting ideal roles, and simulating legacy Applicant Tracking Systems (ATS) to provide actionable career advice.

### Features
* 🧠 **Semantic Skill Graph**: Normalizes resume skills into structured taxonomies (e.g., `PyTorch` -> `Machine Learning Framework`) using `FAISS` and `SentenceTransformers`.
* 🎯 **Job Fit Scorer**: Calculates Euclidean cosine similarity between your resume and a real Job Description.
* 🔮 **Role Predictor**: Uses dense embeddings to predict the Top 3 roles you are actually suited for.
* 🔍 **ATS X-Ray Simulator**: Checks structural integrity, actionable verbs, and quantified impact percentages.
* ✨ **Explainable AI**: Translates mathematical scores into human-readable suggestions on what exactly you need to improve.
* 🎨 **Premium Glassmorphism UI**: Beautiful, dark-mode optimized React dashboard built with Tailwind and Framer Motion.

---

## 🏗️ Architecture

Read the full [Architecture & System Design Document](docs/architecture.md)

---

## 🚀 Quick Start (Local Setup)

### Option 1: Docker (Recommended)
```bash
docker-compose up --build
```

### Option 2: Manual Setup

**1. Backend setup**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Download Spacy Model
python -m spacy download en_core_web_sm

# Build the FAISS Vector Indexes
python scripts/build_index.py

# Run FastAPI Server
uvicorn main:app --reload
```
*API will run on http://localhost:8000*


**2. Frontend setup**
```bash
cd frontend
npm install
npm run dev
```
*Dashboard will run on http://localhost:5173*

---

## 📸 Demo

*(Add screenshots to the `demo/screenshots` folder)*

* **Dynamic Radar Charts** for multi-dimensional competency analysis.
* **Score breakdown** comparing Technical Skills vs Semantic Experience.
* **Explainable Feedback UI** showing exact keyword mismatches.

---

## 🛠️ Tech Stack

* **Backend**: Python, FastAPI, PyMuPDF, Spacy, Sentence-Transformers, FAISS
* **Frontend**: React, Vite, Tailwind CSS, Recharts, Framer Motion
* **Deployment**: Docker, Docker Compose

---

*Designed as a portfolio benchmark for advanced AI/NLP Engineering.*
