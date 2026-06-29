def test_eval_gate_runs_and_passes():
    from core.evaluation.run_gate import run_gate
    assert run_gate(report_only=True) == 0
