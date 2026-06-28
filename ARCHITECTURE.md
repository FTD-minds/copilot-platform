# Architecture — Enterprise AI Copilot Platform

## 1. Goals
Build a production-shaped, modular platform that hosts multiple enterprise AI copilot modules over shared services, demonstrating skills across the Enterprise AI Engineering role family (AI Solutions Engineer, Forward Deployed Engineer, Customer Engineer, Enterprise AI Engineer, AI Integration Engineer, AI Platform Engineer, Applied AI Engineer).

## 2. Principles
1. Model-agnostic (Anthropic/OpenAI/Bedrock/Vertex) via a provider router.
2. Evaluation-gated delivery — CI blocks merges that regress eval scores.
3. Modular — module↔platform plugin contract; modules never import each other.
4. Observable — OpenTelemetry traces + structured logs + LLM trace viewer.
5. Secure by default — env secrets, input validation, synthetic PII-free data, authz.
6. Every phase produces a publicly demonstrable artifact.

## 3. C4 Context
User (Customer Engineer / Ops / Finance) ⟷ Platform ⟷ LLM providers; Platform ⟷ ERP sample data + vector knowledge base.

## 4. C4 Containers
Frontend (Next.js) → API Gateway (FastAPI) → shared platform services
(Auth, Orchestration, Retrieval, Evaluation, Provider Router, Observability, Persistence: Postgres+pgvector, MCP server)
→ Modules (Module 1: ERP Sync Reconciliation; future modules plug in via contract).

## 5. Module 1 — ERP Sync Reconciliation Copilot — data flow
Ingest synthetic ERP sync/recon records → normalize → user query →
Orchestrator plans → Retrieval fetches relevant sync rules/runbooks →
Diagnostic agent reasons over root cause using tools (mapping_validator, reconciliation_calculator, kb_search, rule_lookup) →
Grounded explanation + citations + suggested fix → Eval harness scores (accuracy/groundedness/helpfulness/latency/cost) → logged + dashboard.

## 6. Tech stack
Backend: Python 3.12, FastAPI, Pydantic. Frontend: TypeScript, Next.js, Tailwind.
Orchestration: LangGraph (behind provider-agnostic interface). Retrieval: pgvector on Postgres.
Evals: custom harness (promptfoo/ragas-style metrics). Observability: OpenTelemetry + Langfuse/Phoenix.
Packaging: Docker + docker-compose. CI/CD: GitHub Actions with eval-gate. Deploy: container (Render/Fly.io/AWS).

## 7. Vertical-slice sequencing (per approved directive)
Build a thin end-to-end Module 1 first, then refactor shared platform services beneath it.
The platform abstraction emerges from real use (basis of ADR-001).

## 8. Test strategy
Unit (tools/services) → Integration (API) → Eval suite (LLM quality, gated in CI) → Smoke (post-deploy).

## 9. Security
Secrets via env/secret store; Pydantic input validation; synthetic, PII-free sample data only;
authz on endpoints; dependency scanning in CI; retrieval prompt-injection mitigations.

## 10. ADRs
See docs/adr/. ADR-001 establishes the monorepo-platform + vertical-slice approach.
