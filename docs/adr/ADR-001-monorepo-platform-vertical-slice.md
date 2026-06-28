# ADR-001: Monorepo platform with vertical-slice delivery

- Status: Accepted
- Date: (Phase 0)
- Deciders: Engineering (Senay Mesfin)

## Context
The goal is multiple flagship-quality enterprise AI modules that, together, demonstrate competence across the Enterprise AI Engineering role family. Two structural options:
1. Separate standalone applications per project.
2. One modular monorepo ("platform") with shared services and pluggable modules.

A separate question is sequencing: build shared platform first, or build a thin vertical slice of the first module end-to-end first.

## Decision
Adopt a **modular monorepo platform**. Build with a **vertical-slice-first** sequence: implement a thin, working Module 1 (ERP Sync Reconciliation Copilot) end-to-end, then refactor reusable concerns (provider routing, retrieval, evaluation, observability) into shared `platform/` services.

## Rationale
- A platform demonstrates AI Platform / Enterprise AI Engineer competencies that isolated apps do not.
- Shared services (auth, providers, retrieval, evaluation, observability, deployment) are reused by every future module — ~70% reuse.
- Vertical-slice-first yields a demoable artifact and real usage sooner; the shared abstraction is then extracted from evidence rather than guessed, reducing over-engineering risk.
- Every phase still produces a public artifact (see BUILD_PRINCIPLES.md), maximizing continuous employability.

## Consequences
- Positive: coherent architecture story; fast first demo; reusable core; strong interview narrative ("I extracted the platform from a working slice").
- Negative: monorepo needs disciplined module boundaries (enforced by the plugin contract; modules never import each other).
- Follow-ups: ADR-002 provider abstraction, ADR-003 pgvector choice, ADR-004 orchestration, ADR-005 eval-gate in CI, ADR-006 MCP exposure, ADR-007 synthetic-data/security.
