FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Build Vector db for skills during build (for production readiness)
COPY data /app/data
COPY backend /app/backend
RUN python backend/scripts/build_index.py || true

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
