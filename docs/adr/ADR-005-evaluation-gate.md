# ADR-005: Evaluation framework with an enforcing CI gate

- Status: Accepted
- Date: (Phase 4)
- Deciders: Engineering (Senay Mesfin)

## Context
An enterprise AI copilot is only trustworthy if its quality is measured and protected against regression. We need: a golden dataset of known-answer cases, objective metrics, and a mechanism that prevents shipping a change that degrades quality.

## Decision
Add an evaluation harness (`modules/.../evals/harness.py`) that runs the diagnostic agent over a golden dataset (`evals/golden.json`) and scores four metrics:
- **retrieval_accuracy** — expected KB entry appears in citations
- **tool_selection_accuracy** — the correct tool (or none) is invoked
- **tool_correctness** — the tool returns the expected result (reconciles / discrepancy / validity)
- **groundedness** — the answer is supported by retrieved sources or tool output

Thresholds are defined in code. The CI **eval-gate job is now ENFORCING**: `python -m core.evaluation.run_gate` exits non-zero if any metric is below threshold, blocking the merge.

## Rationale
- "If it isn't evaluated, it isn't shipped" — quality becomes a build constraint, not a hope.
- Deterministic scoring (no LLM judge required) keeps the gate hermetic and fast in CI; an LLM-as-judge metric can be added later behind the same interface.
- A golden dataset doubles as regression protection and as living documentation of expected behavior.

## Consequences
- Positive: measurable, regression-protected quality; the single strongest enterprise-AI credibility signal; thresholds are explicit and reviewable.
- Negative: the golden set is small (8 cases) and deterministic; expanding coverage and adding semantic/groundedness LLM metrics is future work.
- Follow-ups: Phase 5 surfaces these metrics in an eval dashboard; new modules ship with their own golden sets gated the same way.
