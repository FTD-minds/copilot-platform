"""Evaluation harness for the ERP Sync Reconciliation Copilot (ADR-005).

Runs the diagnostic agent over a golden dataset and scores:
  - retrieval_accuracy: did the expected KB entry appear in citations?
  - tool_selection_accuracy: was the expected tool invoked (or correctly none)?
  - tool_correctness: did the tool produce the expected result (reconciles/discrepancy/validity)?
  - groundedness: does the answer cite at least one retrieved source?

Aggregate metrics are compared against thresholds; `meets_thresholds()` drives
the CI eval-gate (Phase 4 makes the gate enforcing).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from core.retrieval.store import InMemoryVectorStore
from modules.erp_sync_reconciliation.agents.diagnostic_agent import DiagnosticAgent
from modules.erp_sync_reconciliation.service import load_kb

_GOLDEN = Path(__file__).parent / "golden.json"

THRESHOLDS = {
    "retrieval_accuracy": 0.85,
    "tool_selection_accuracy": 0.90,
    "tool_correctness": 1.00,
    "groundedness": 0.95,
}


@dataclass
class CaseScore:
    id: str
    retrieval_ok: bool
    tool_selection_ok: bool
    tool_correct: bool
    grounded: bool


@dataclass
class EvalReport:
    metrics: dict[str, float]
    cases: list[CaseScore] = field(default_factory=list)

    def meets_thresholds(self) -> bool:
        return all(self.metrics.get(k, 0.0) >= v for k, v in THRESHOLDS.items())


def _build_agent() -> DiagnosticAgent:
    store = InMemoryVectorStore()
    store.add(load_kb())
    return DiagnosticAgent(store)


def run_eval(golden_path: Path = _GOLDEN) -> EvalReport:
    agent = _build_agent()
    cases = json.loads(golden_path.read_text())
    scores: list[CaseScore] = []

    for c in cases:
        result = agent.run(c["query"], inputs=c.get("inputs", {}))

        retrieval_ok = c["expected_citation"] in result.citations

        expect_tool = c.get("expect_tool")
        ran_tools = set(result.tool_outputs.keys())
        tool_selection_ok = (expect_tool in ran_tools) if expect_tool else (len(ran_tools) == 0)

        tool_correct = True
        if expect_tool == "reconciliation_calculator":
            out = result.tool_outputs.get("reconciliation_calculator", {})
            if "expect_reconciles" in c:
                tool_correct &= out.get("reconciles") == c["expect_reconciles"]
            if "expected_discrepancy" in c:
                tool_correct &= out.get("discrepancy") == c["expected_discrepancy"]
        elif expect_tool == "mapping_validator":
            out = result.tool_outputs.get("mapping_validator", {})
            if "expect_mapping_valid" in c:
                tool_correct &= out.get("valid") == c["expect_mapping_valid"]

        grounded = any(cit in result.answer for cit in result.citations) or bool(result.tool_outputs)

        scores.append(CaseScore(c["id"], retrieval_ok, tool_selection_ok, tool_correct, grounded))

    n = len(scores) or 1
    metrics = {
        "retrieval_accuracy": round(sum(s.retrieval_ok for s in scores) / n, 4),
        "tool_selection_accuracy": round(sum(s.tool_selection_ok for s in scores) / n, 4),
        "tool_correctness": round(sum(s.tool_correct for s in scores) / n, 4),
        "groundedness": round(sum(s.grounded for s in scores) / n, 4),
    }
    return EvalReport(metrics=metrics, cases=scores)
