# Enterprise AI Copilot Platform

> A modular, model-agnostic platform for enterprise AI copilots. Each module is an independently deployable, evaluated AI system sharing common platform services (auth, AI orchestration, retrieval, evaluation, observability, deployment).

[![CI](https://github.com/USER/copilot-platform/actions/workflows/ci.yml/badge.svg)](./.github/workflows/ci.yml)

## Why this exists
Enterprise teams adopt AI fastest when copilots are **trustworthy, evaluated, and deployable into real workflows**. This platform demonstrates that pattern, starting with a module drawn from a real, high-friction enterprise problem: **ERP sync & reconciliation failures**.

## Modules
| Module | Status | What it does |
|---|---|---|
| **ERP Sync Reconciliation Copilot** | 🚧 in progress (Module 1) | Diagnoses why an ERP/accounting sync or reconciliation failed; explains root cause with citations; suggests a fix. Every answer is scored by the eval framework. |
| Integration Health Monitor | planned | Detects sync drift, generates plain-language incident explanations |
| Customer Onboarding Copilot | planned | Guides + live-validates a customer's integration setup |
| AI Support Engineer | planned | Ticket triage, deflection, runbook answers |
| AP Invoice Intelligence | planned | Extracts/validates invoices, flags anomalies, routes approvals |
| Evaluation Dashboard | planned | Visualizes eval scores across modules over time |
| Admin Console | planned | Tenant/config/observability administration |

## Platform services (shared)
Auth (OIDC/JWT) · AI Orchestration (multi-agent) · Retrieval (RAG) · Evaluation framework · Model-agnostic provider router (Anthropic / OpenAI / Bedrock / Vertex) · MCP server · Observability (OpenTelemetry) · Persistence (Postgres + pgvector).

## Quickstart (will be runnable from Phase 1)
```bash
cp .env.example .env        # add a provider key
docker compose up           # starts api + postgres
# open http://localhost:8000/docs  (API)  and  http://localhost:3000 (frontend, Phase 5)
```

## Architecture
See **[ARCHITECTURE.md](./ARCHITECTURE.md)** and **[docs/adr/](./docs/adr/)** for decision records.

## Engineering principles
- **If it isn't evaluated, it isn't shipped** — every module ships with an eval suite gated in CI.
- **Model-agnostic** — providers are swapped by config, never by code change.
- **Modular** — modules depend on platform services, never on each other.
- **Every phase ships a public artifact** — see [docs/BUILD_PRINCIPLES.md](./docs/BUILD_PRINCIPLES.md).

## License
MIT
