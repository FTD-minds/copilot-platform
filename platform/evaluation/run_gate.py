"""Evaluation gate (Phase 0 stub).

Phase 4 makes this enforcing: it will load the golden dataset, run the module
under test, score accuracy/groundedness/helpfulness, and exit non-zero if any
metric regresses below threshold — blocking the CI merge.

For Phase 0 it runs in report-only mode so CI is green while the harness is built.
"""
from __future__ import annotations

import argparse
import sys


def run_gate(report_only: bool = True) -> int:
    # Phase 4 will replace this with real golden-dataset scoring.
    results = {
        "status": "report-only",
        "phase": 0,
        "note": "Eval harness not yet implemented; enforcing gate arrives in Phase 4.",
    }
    print(f"[eval-gate] {results}")
    if report_only:
        return 0
    # Future: return 1 if metrics below threshold.
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the LLM evaluation gate.")
    parser.add_argument("--report-only", action="store_true", help="Do not fail CI; print report.")
    args = parser.parse_args()
    return run_gate(report_only=args.report_only)


if __name__ == "__main__":
    sys.exit(main())
