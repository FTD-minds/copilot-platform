# Enterprise AI Copilot Platform

> A modular, model-agnostic platform for enterprise AI copilots. Each module is an independently deployable, evaluated AI system sharing common platform services (auth, AI orchestration, retrieval, evaluation, observability, deployment).

[![CI](https://github.com/USER/copilot-platform/actions/workflows/ci.yml/badge.svg)](./.github/workflows/ci.yml)

## Why this exists
Enterprise teams adopt AI fastest when copilots are **trustworthy, evaluated, and deployable into real workflows**. This platform demonstrates that pattern, starting with a module drawn from a real, high-friction enterprise problem: **ERP sync & reconciliation failures**.

## Modules
| Module | Status | What it does |
|---|---|---|
| **ERP Sync Reconciliation Copilot** | 🚧 in progress (Module 1) | Diagnoses why an ERP/accounting sync or reconciliation failed; explains root cause with citations; suggests a fix. Every answer is scored by the eval framework. |
| _Platform core_ | ✅ Phase 1 | Model-agnostic provider router + FastAPI gateway (`/health`, `/providers`, `/chat`) + Docker + Postgres/pgvector. |
| _Retrieval (RAG)_ | ✅ Phase 2 | Pluggable embedder + vector store; `/modules/erp-sync/diagnose` grounds answers in a knowledge base **with citations**. |
| Integration Health Monitor | planned | Detects sync drift, generates plain-language incident explanations |
| Customer Onboarding Copilot | planned | Guides + live-validates a customer's integration setup |
| AI Support Engineer | planned | Ticket triage, deflection, runbook answers |
| AP Invoice Intelligence | planned | Extracts/validates invoices, flags anomalies, routes approvals |
| Evaluation Dashboard | planned | Visualizes eval scores across modules over time |
| Admin Console | planned | Tenant/config/observability administration |

## Platform services (shared)
Auth (OIDC/JWT) · AI Orchestration (multi-agent) · Retrieval (RAG) · Evaluation framework · Model-agnostic provider router (Anthropic / OpenAI / Bedrock / Vertex) · MCP server · Observability (OpenTelemetry) · Persistence (Postgres + pgvector).

## Quickstart

**Run the API (no API keys needed — uses the built-in mock provider):**
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn core.api.main:app --reload
# open http://localhost:8000/docs
```

**With Docker + Postgres/pgvector:**
```bash
cp .env.example .env        # optionally add a provider key
docker compose up           # api on :8000, db on :5432
```

**Try it:**
```bash
curl localhost:8000/health
curl localhost:8000/providers
curl -X POST localhost:8000/chat -H 'content-type: application/json' \
  -d '{"messages":[{"role":"user","content":"Why did my QBO deposit fail to reconcile?"}]}'
```
Set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` in `.env` and pass `"provider":"anthropic"` (or `"openai"`) to use a real model — the API is identical (see [ADR-002](./docs/adr/ADR-002-model-agnostic-provider-abstraction.md)).

## Architecture
See **[ARCHITECTURE.md](./ARCHITECTURE.md)** and **[docs/adr/](./docs/adr/)** for decision records.

## Engineering principles
- **If it isn't evaluated, it isn't shipped** — every module ships with an eval suite gated in CI.
- **Model-agnostic** — providers are swapped by config, never by code change.
- **Modular** — modules depend on platform services, never on each other.
- **Every phase ships a public artifact** — see [docs/BUILD_PRINCIPLES.md](./docs/BUILD_PRINCIPLES.md).

## License
MIT
