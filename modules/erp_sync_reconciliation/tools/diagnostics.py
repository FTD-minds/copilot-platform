"""Diagnostic tools for the ERP Sync Reconciliation Copilot.

These are deterministic, testable functions an agent can call to reason about a
concrete reconciliation problem (not just retrieve docs). Pure Python, no
network — they make the copilot genuinely useful and are exposed over MCP.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ReconResult:
    reconciles: bool
    expected_net: float
    discrepancy: float
    explanation: str


def reconciliation_calculator(
    gross_payments: list[float],
    processor_fees: float,
    bank_deposit: float,
    tolerance: float = 0.01,
) -> ReconResult:
    """Check whether a set of gross payments minus fees matches the bank deposit.

    Mirrors the real Stripe/ACH payout problem: a processor aggregates charges
    and deducts fees, so gross != deposited. Returns the expected net and the
    discrepancy so the agent can explain exactly what is off.
    """
    expected_net = round(sum(gross_payments) - processor_fees, 2)
    discrepancy = round(bank_deposit - expected_net, 2)
    reconciles = abs(discrepancy) <= tolerance
    if reconciles:
        explanation = (
            f"Reconciles: gross {sum(gross_payments):.2f} - fees {processor_fees:.2f} "
            f"= net {expected_net:.2f}, matching the bank deposit {bank_deposit:.2f}."
        )
    else:
        direction = "more" if discrepancy > 0 else "less"
        explanation = (
            f"Does NOT reconcile: expected net {expected_net:.2f} "
            f"(gross {sum(gross_payments):.2f} - fees {processor_fees:.2f}), "
            f"but bank deposit is {bank_deposit:.2f} — {abs(discrepancy):.2f} {direction} than expected. "
            f"Common causes: an unrecorded processor fee, a missing/extra charge in the payout batch, "
            f"or undeposited funds not grouped into this deposit."
        )
    return ReconResult(reconciles, expected_net, discrepancy, explanation)


@dataclass
class MappingResult:
    valid: bool
    issue: str
    fix: str


def mapping_validator(item_mapping_mode: str, integration_mode: str) -> MappingResult:
    """Detect the classic item-level vs chart-of-accounts (COA) mapping mismatch.

    Modes: 'item' (each product maps to a specific income account) or
    'coa' (products inherit a chart-of-accounts default).
    """
    a = item_mapping_mode.strip().lower()
    b = integration_mode.strip().lower()
    valid = a == b
    if valid:
        return MappingResult(True, "", f"Mapping modes match ('{a}'). No mismatch.")
    return MappingResult(
        False,
        f"Mapping mismatch: items configured as '{a}' but integration set to '{b}'.",
        f"Align the integration mapping mode to '{a}' (or remap items to '{b}'), then re-run the failed sync batch.",
    )
