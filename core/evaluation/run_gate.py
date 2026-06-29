"""Evaluation gate — ENFORCING as of Phase 4.

Runs the module evaluation harness, prints a metrics report, and exits non-zero
if any metric is below its threshold. Wired into CI so a quality regression
blocks the merge ("if it isn't evaluated, it isn't shipped").

    python -m core.evaluation.run_gate            # enforcing (CI default)
    python -m core.evaluation.run_gate --report-only   # print, never fail
"""
from __future__ import annotations

import argparse
import json
import sys

from modules.erp_sync_reconciliation.evals.harness import THRESHOLDS, run_eval


def run_gate(report_only: bool = False) -> int:
    report = run_eval()
    print("[eval-gate] metrics:", json.dumps(report.metrics))
    print("[eval-gate] thresholds:", json.dumps(THRESHOLDS))

    failures = [
        f"{k}={report.metrics.get(k, 0.0):.2f} < {v:.2f}"
        for k, v in THRESHOLDS.items()
        if report.metrics.get(k, 0.0) < v
    ]
    if failures:
        print("[eval-gate] FAIL:", "; ".join(failures))
        if report_only:
            print("[eval-gate] (report-only: not failing CI)")
            return 0
        return 1

    print(f"[eval-gate] PASS — all {len(THRESHOLDS)} metrics meet thresholds across "
          f"{len(report.cases)} golden cases.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the LLM evaluation gate.")
    parser.add_argument("--report-only", action="store_true", help="Print report, never fail CI.")
    args = parser.parse_args()
    return run_gate(report_only=args.report_only)


if __name__ == "__main__":
    sys.exit(main())
