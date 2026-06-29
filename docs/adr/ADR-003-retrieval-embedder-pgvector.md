# ADR-003: Retrieval architecture — pluggable embedder + pgvector target, in-memory for the slice

- Status: Accepted
- Date: (Phase 2)
- Deciders: Engineering (Senay Mesfin)

## Context
Module 1 must ground answers about ERP sync/reconciliation failures in a knowledge base and return citations. We need: (a) a real RAG pipeline (chunk → embed → similarity search → grounded, cited answer), (b) hermetic CI/demos with no external embedding API or running database, and (c) a clear path to production-scale retrieval.

## Decision
- Define an `Embedder` interface (`core/retrieval/embedder.py`); default to a deterministic, dependency-free **HashingEmbedder** so retrieval runs with no keys. Real embedders (OpenAI/Voyage/Bedrock) implement the same interface and are swapped by config — mirroring the provider router (ADR-002).
- Retrieval uses an `InMemoryVectorStore` (cosine) for the vertical slice. **pgvector on Postgres is the production target** and is already provisioned in `docker-compose.yml`; it implements the same store interface.
- The module composes retrieval + provider router into a `ReconciliationCopilot.diagnose()` that returns an answer plus structured `Citation`s.

## Rationale
- Hermetic by default: CI and demos need no embedding API or DB; the pipeline is still real (embed → cosine search → cite).
- Same swap-by-config pattern as providers keeps the architecture coherent and model/vendor-agnostic.
- pgvector chosen over a dedicated vector DB to keep one datastore (vectors + app data) and reduce ops surface for an enterprise deployment; revisit if scale demands a specialized store.

## Consequences
- Positive: full RAG demonstrable offline; production path is a drop-in store/embedder swap; strong, citeable answers.
- Negative: the hashing embedder is lexical, not semantic — fine for demonstration, but real semantic recall needs a neural embedder (enabled by config when a key/DB is present).
- Follow-ups: Phase 3 adds the diagnostic agent + tools + MCP on top of this retrieval layer; Phase 4 evals score groundedness/accuracy of the cited answers.
