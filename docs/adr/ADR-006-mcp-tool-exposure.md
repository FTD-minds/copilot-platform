# ADR-006: Expose diagnostic tools over the Model Context Protocol (MCP)

- Status: Accepted
- Date: (Phase 3)
- Deciders: Engineering (Senay Mesfin)

## Context
The reconciliation tools (reconciliation_calculator, mapping_validator) are useful beyond this module's own agent — any MCP-compatible client (Claude Desktop, IDEs, other agents) could call them. We want to expose them via a standard protocol without making the SDK a hard dependency.

## Decision
Provide an MCP server (`core/mcp/server.py`) exposing the tools. The MCP SDK is imported lazily inside `main()`; a vendor-neutral `build_tool_specs()` documents the tool contract and `call_tool()` dispatches by name — both usable (and tested) without the SDK installed. The SDK is an optional extra (`pip install ".[mcp]"`).

## Rationale
- Interoperability: MCP is the emerging standard for tool/context exposure; supporting it is a current, high-signal capability.
- Optional dependency: lazy import keeps the platform installable and CI hermetic; the tool contract and dispatch are testable without the SDK.
- Reuse: the same tools power the in-process agent (ADR-004) and external MCP clients — one implementation, two consumers.

## Consequences
- Positive: external agents/clients can use the tools; demonstrates MCP fluency; no forced dependency.
- Negative: the stdio server entrypoint (`main()`) requires the SDK and is excluded from unit coverage; integration verified manually when the SDK is present.
- Follow-ups: additional modules can register their tools with the same server.
