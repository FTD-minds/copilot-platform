"""MCP server exposing ERP reconciliation tools (ADR-006).

Exposes the deterministic diagnostic tools (reconciliation_calculator,
mapping_validator) over the Model Context Protocol so ANY MCP-compatible client
(Claude Desktop, IDEs, other agents) can call them. The SDK is imported lazily
so the platform installs and runs without it; `build_tool_specs()` documents the
tool contract regardless of whether the SDK is present.

Run:  python -m core.mcp.server   (requires:  pip install ".[mcp]")
"""
from __future__ import annotations

from typing import Any

from modules.erp_sync_reconciliation.tools import (
    mapping_validator,
    reconciliation_calculator,
)


def build_tool_specs() -> list[dict[str, Any]]:
    """Vendor-neutral description of the exposed tools (also used in tests/docs)."""
    return [
        {
            "name": "reconciliation_calculator",
            "description": "Check whether gross payments minus processor fees match a bank deposit.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "gross_payments": {"type": "array", "items": {"type": "number"}},
                    "processor_fees": {"type": "number"},
                    "bank_deposit": {"type": "number"},
                },
                "required": ["gross_payments", "bank_deposit"],
            },
        },
        {
            "name": "mapping_validator",
            "description": "Detect an item-level vs chart-of-accounts (COA) mapping mismatch.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "item_mapping_mode": {"type": "string", "enum": ["item", "coa"]},
                    "integration_mode": {"type": "string", "enum": ["item", "coa"]},
                },
                "required": ["item_mapping_mode", "integration_mode"],
            },
        },
    ]


def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Dispatch a tool call by name (used by the MCP server and tests)."""
    if name == "reconciliation_calculator":
        recon = reconciliation_calculator(
            gross_payments=[float(x) for x in arguments["gross_payments"]],
            processor_fees=float(arguments.get("processor_fees", 0.0)),
            bank_deposit=float(arguments["bank_deposit"]),
        )
        return {"reconciles": recon.reconciles, "expected_net": recon.expected_net,
                "discrepancy": recon.discrepancy, "explanation": recon.explanation}
    if name == "mapping_validator":
        mapping = mapping_validator(arguments["item_mapping_mode"], arguments["integration_mode"])
        return {"valid": mapping.valid, "issue": mapping.issue, "fix": mapping.fix}
    raise ValueError(f"Unknown tool: {name}")


def main() -> None:  # pragma: no cover - requires MCP SDK + stdio transport
    """Start the MCP server over stdio. Requires the optional 'mcp' dependency."""
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as e:
        raise SystemExit(
            "MCP SDK not installed. Install with: pip install '.[mcp]'"
        ) from e

    server = FastMCP("erp-sync-reconciliation")

    @server.tool()
    def recon(gross_payments: list[float], bank_deposit: float, processor_fees: float = 0.0) -> dict:
        """Check whether gross payments minus fees match a bank deposit."""
        return call_tool("reconciliation_calculator", {
            "gross_payments": gross_payments, "bank_deposit": bank_deposit,
            "processor_fees": processor_fees,
        })

    @server.tool()
    def mapping(item_mapping_mode: str, integration_mode: str) -> dict:
        """Detect an item-level vs chart-of-accounts mapping mismatch."""
        return call_tool("mapping_validator", {
            "item_mapping_mode": item_mapping_mode, "integration_mode": integration_mode,
        })

    server.run()


if __name__ == "__main__":  # pragma: no cover
    main()
