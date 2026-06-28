# Build Principles & Per-Phase Employability Ledger

Core rule (Chief Architect directive): **every phase must produce a publicly demonstrable artifact and advance employability.** Success = a working enterprise AI module Senay can confidently discuss in interviews — not merely completed code.

For every phase we track: Resume bullets · LinkedIn updates · GitHub milestones · Portfolio additions · Interview stories · Technical competencies · Role-family coverage.

---

## Phase 0 — Foundation (THIS PHASE) ✅
**Public artifact:** Initialized public repo with README, ARCHITECTURE, ADR-001, CI skeleton, project scaffold.
- **Resume bullets enabled:**
  - "Architected a modular, model-agnostic enterprise AI platform (multi-module monorepo) with CI/CD and an evaluation-gated delivery pipeline."
  - "Authored Architecture Decision Records (ADRs) documenting platform and sequencing trade-offs."
- **LinkedIn update:** "Building an Enterprise AI Copilot Platform — open-sourcing the journey. Phase 0: architecture + ADRs live." + repo link.
- **GitHub milestone:** initial commit; repo public; README badge; ADR-001.
- **Portfolio addition:** ARCHITECTURE.md + C4 diagrams + ADR folder.
- **Interview story:** "Why I chose a platform + vertical-slice approach over standalone apps" (ADR-001).
- **Competencies:** system design, ADRs, CI/CD setup, monorepo structure, technical writing.
- **Role-family coverage:** AI Platform Engineer, Enterprise AI Engineer, Solutions Architect (AI).

## Phase 1 — Platform core (provider router + API + auth + Postgres/pgvector)
**Public artifact:** `docker compose up` runs a model-agnostic API; `/health` + `/docs` live.
- Resume: "Implemented a model-agnostic provider router (Anthropic/OpenAI/Bedrock/Vertex) behind a typed FastAPI service."
- LinkedIn: demo gif of swapping providers via config.
- GitHub: tagged `v0.1-platform-core`. Portfolio: OpenAPI spec. 
- Interview story: provider abstraction trade-offs (ADR-002).
- Competencies: Python, FastAPI, API design, Docker, abstraction design.
- Roles: Enterprise AI Eng, AI Platform Eng, AI Integration Eng.

## Phase 2 — Retrieval + knowledge base (RAG)
**Public artifact:** endpoint answering ERP-sync questions with citations.
- Resume: "Built a RAG pipeline (pgvector) grounding answers in enterprise sync/runbook knowledge with citations."
- Competencies: embeddings, vector search, RAG, grounding. Roles: AI Solutions Eng, Applied AI Eng.

## Phase 3 — Diagnostic agent + tools + MCP
**Public artifact:** multi-agent copilot diagnosing seeded sync failures; MCP server exposes tools.
- Resume: "Designed a multi-agent diagnostic copilot with tool use, exposed via Model Context Protocol (MCP)."
- Interview story: agent design + MCP (ADR-006). Competencies: multi-agent, tool-calling, MCP. Roles: Applied AI Eng, AI Platform Eng.

## Phase 4 — Eval harness + golden dataset + CI eval-gate
**Public artifact:** eval report + CI badge showing eval-gated merges.
- Resume: "Engineered an LLM evaluation framework (accuracy/groundedness/helpfulness) enforced as a CI merge gate."
- This is the credibility centerpiece. Competencies: evals, test design, CI gating. Roles: Enterprise AI Eng, AI Solutions Eng.

## Phase 5 — Frontend (chat + eval dashboard)
**Public artifact:** deployed demo UI.
- Resume: "Built a demo UI + live evaluation dashboard for an enterprise AI copilot."
- Competencies: Next.js, UX, demo craft. Roles: Customer Engineer, AI Solutions Eng.

## Phase 6 — Deploy + docs + demo video (M-01: 0 → 1)
**Public artifact:** public live URL + 3–5 min demo video + full writeup.
- Resume: promote ERP Sync Reconciliation Copilot to a featured Projects entry; Master Resume → v1.0.
- Interview story: end-to-end FDE deployment + last-mile constraints. Competencies: deployment, observability, docs. Roles: FDE, AI Platform Eng, Customer Engineer.
- **Definition of done:** deployed + evaluated + documented + demoable + interview-ready.
