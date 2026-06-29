"""Eval metrics endpoint — powers the dashboard UI."""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/api/evals")
def evals() -> dict:
    from modules.erp_sync_reconciliation.evals.harness import THRESHOLDS, run_eval
    report = run_eval()
    return {
        "metrics": report.metrics,
        "thresholds": THRESHOLDS,
        "cases": [
            {
                "id": c.id,
                "retrieval_ok": c.retrieval_ok,
                "tool_selection_ok": c.tool_selection_ok,
                "tool_correct": c.tool_correct,
                "grounded": c.grounded,
            }
            for c in report.cases
        ],
        "passing": report.meets_thresholds(),
    }
