# ADR-004: Lightweight, framework-agnostic agent orchestration

- Status: Accepted
- Date: (Phase 3)
- Deciders: Engineering (Senay Mesfin)

## Context
Module 1 needs to move beyond retrieve-and-summarize to genuine diagnosis: classify an issue, run computational tools (reconciliation math, mapping checks), and synthesize a grounded answer. Options: adopt a heavyweight agent framework (LangGraph/CrewAI) now, or implement a minimal plan→act→synthesize loop behind a stable interface.

## Decision
Implement a dependency-free `DiagnosticAgent` with an explicit plan→act→synthesize loop (`agents/diagnostic_agent.py`). It routes by query keywords + structured inputs to retrieval and/or tools, and returns the answer plus its reasoning steps, citations, and tool outputs. The loop is framework-agnostic so it can later be swapped for LangGraph without changing the module's API contract.

## Rationale
- Transparency: explicit steps make the agent's reasoning inspectable and testable (each step is asserted in tests) — important for enterprise trust.
- No premature dependency: avoids coupling the portfolio to a fast-moving framework; demonstrates understanding of the agent pattern itself, not just a library.
- Deterministic: runs in CI with no LLM, while a provider can be layered on for natural-language synthesis when present.

## Consequences
- Positive: testable multi-step reasoning; clean upgrade path to LangGraph; strong interview signal (can explain the agent loop from first principles).
- Negative: routing is rule-based, not LLM-planned; acceptable for a bounded diagnostic domain, and the interface allows swapping in LLM planning later.
- Follow-ups: ADR-006 exposes the tools over MCP; Phase 4 evals score the agent's diagnoses.
