def test_eval_harness_meets_thresholds():
    from modules.erp_sync_reconciliation.evals.harness import run_eval
    report = run_eval()
    assert report.metrics["retrieval_accuracy"] >= 0.85
    assert report.metrics["tool_correctness"] == 1.0
    assert report.meets_thresholds(), report.metrics


def test_eval_gate_enforcing_passes():
    from core.evaluation.run_gate import run_gate
    assert run_gate(report_only=False) == 0


def test_eval_report_has_all_cases():
    from modules.erp_sync_reconciliation.evals.harness import run_eval
    report = run_eval()
    assert len(report.cases) == 8          # golden dataset size
    assert all(hasattr(c, "retrieval_ok") for c in report.cases)
