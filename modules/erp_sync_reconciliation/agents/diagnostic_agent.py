"""Lightweight diagnostic agent orchestration (ADR-004).

A dependency-free, deterministic plan→act→synthesize loop that combines
retrieval (RAG) with computational tools. Kept framework-agnostic so it can be
swapped for LangGraph without changing the module contract. Multi-step:
  1. PLAN   — classify the issue and decide which tools/retrieval to use
  2. ACT    — run retrieval + any applicable tools
  3._SYNTH  — produce a grounded, cited, tool-supported diagnosis
"""
from __future__ import annotations

from dataclasses import dataclass, field

from core.retrieval.store import InMemoryVectorStore
from modules.erp_sync_reconciliation.tools import (
    mapping_validator,
    reconciliation_calculator,
)


@dataclass
class AgentStep:
    name: str
    detail: str


@dataclass
class AgentResult:
    answer: str
    steps: list[AgentStep] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)
    tool_outputs: dict = field(default_factory=dict)


class DiagnosticAgent:
    """Plans which tools/retrieval to use based on the query and structured inputs."""

    def __init__(self, store: InMemoryVectorStore) -> None:
        self._store = store

    def run(self, query: str, inputs: dict | None = None) -> AgentResult:
        inputs = inputs or {}
        steps: list[AgentStep] = []

        # 1. PLAN — keyword + input-driven routing.
        q = query.lower()
        plan: list[str] = ["retrieve"]
        if {"gross_payments", "bank_deposit"} <= inputs.keys() or "reconcile" in q or "payout" in q or "deposit" in q:
            plan.append("reconciliation_calculator")
        if {"item_mapping_mode", "integration_mode"} <= inputs.keys() or "mapping" in q or "account" in q:
            plan.append("mapping_validator")
        steps.append(AgentStep("plan", f"selected: {', '.join(plan)}"))

        # 2. ACT — retrieval.
        hits = self._store.search(query, k=3)
        citations = [h.doc.id for h in hits]
        steps.append(AgentStep("retrieve", f"top: {citations}"))
        context_doc = hits[0].doc if hits else None

        tool_outputs: dict = {}

        if "reconciliation_calculator" in plan and {"gross_payments", "bank_deposit"} <= inputs.keys():
            recon = reconciliation_calculator(
                gross_payments=[float(x) for x in inputs["gross_payments"]],
                processor_fees=float(inputs.get("processor_fees", 0.0)),
                bank_deposit=float(inputs["bank_deposit"]),
            )
            tool_outputs["reconciliation_calculator"] = {
                "reconciles": recon.reconciles,
                "expected_net": recon.expected_net,
                "discrepancy": recon.discrepancy,
                "explanation": recon.explanation,
            }
            steps.append(AgentStep("reconciliation_calculator", recon.explanation))

        if "mapping_validator" in plan and {"item_mapping_mode", "integration_mode"} <= inputs.keys():
            mapping = mapping_validator(inputs["item_mapping_mode"], inputs["integration_mode"])
            tool_outputs["mapping_validator"] = {
                "valid": mapping.valid, "issue": mapping.issue, "fix": mapping.fix,
            }
            steps.append(AgentStep("mapping_validator", mapping.issue or "modes match"))

        # 3. SYNTHESIZE — grounded answer + tool findings.
        parts: list[str] = []
        if context_doc is not None:
            parts.append(f"Likely area: {context_doc.title}. {context_doc.text} [{context_doc.id}]")
        for name, out in tool_outputs.items():
            if name == "reconciliation_calculator":
                parts.append(f"Tool check — {out['explanation']}")
            elif name == "mapping_validator":
                parts.append(
                    out["fix"] if not out["valid"] else "Mapping modes are consistent."
                )
        answer = " ".join(parts) if parts else "No relevant knowledge or tool result for this issue."

        return AgentResult(answer=answer, steps=steps, citations=citations, tool_outputs=tool_outputs)
