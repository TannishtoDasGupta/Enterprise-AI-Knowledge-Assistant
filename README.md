# Enterprise AI Knowledge Assistant

Citation-first internal knowledge search built with FastAPI. Ingest text documents, split them into passages, rank passages with transparent lexical scoring, and return source excerpts. The demo runs without paid APIs or external services.

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open /docs. API: POST /documents, POST /ask, GET /documents, GET /health.

## Scope and production notes
This is a retrieval demonstrator, not a complete enterprise RAG deployment. It uses in-memory storage and lexical retrieval. A production version should add durable storage, embeddings/vector search, SSO, tenant-level authorization, audit logs, rate limits, evaluation datasets, and model-grounded synthesis. Treat retrieved documents as untrusted input.
