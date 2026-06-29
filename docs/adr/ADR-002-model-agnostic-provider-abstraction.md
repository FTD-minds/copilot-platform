# ADR-002: Model-agnostic provider abstraction

- Status: Accepted
- Date: (Phase 1)
- Deciders: Engineering (Senay Mesfin)

## Context
Enterprise customers standardize on different LLM vendors (Anthropic, OpenAI, AWS Bedrock, Google Vertex). A Forward Deployed / Enterprise AI Engineer must deploy the same solution against whichever provider a customer mandates, without rewriting application logic. We also need the system to run in CI and local demos with no API keys.

## Decision
Define a single `Provider` interface (`complete(messages) -> ChatResponse`) in `core/providers/base.py`. Concrete adapters implement it: `MockProvider` (default, deterministic, no network), `AnthropicProvider`, `OpenAIProvider` (vendor SDKs imported lazily). A `router.get_provider()` selects by config/request and **falls back to mock** when a requested provider has no key. The rest of the platform depends only on the interface, never on a vendor SDK.

## Rationale
- Portability across customer environments is the core FDE/Enterprise-AI requirement.
- Lazy imports keep vendor SDKs optional — the platform installs and runs without them.
- Mock-by-default means CI is hermetic (no secrets) and demos always work; graceful degradation instead of hard failure.
- New providers (Bedrock/Vertex) are added as adapters without touching modules.

## Consequences
- Positive: vendor-swappable by config; testable without keys; clean module boundary; strong interview/portfolio signal ("model-agnostic by design").
- Negative: a lowest-common-denominator interface initially (no streaming/tools yet); these extend the interface in later phases.
- Follow-ups: ADR-004 (orchestration) builds multi-agent flows on top of this interface; streaming/tool-calling added when a module needs them.
