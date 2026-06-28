def test_eval_gate_report_only_passes():
    from core.evaluation.run_gate import run_gate
    assert run_gate(report_only=True) == 0
