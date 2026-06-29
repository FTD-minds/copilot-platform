from modules.erp_sync_reconciliation.tools import mapping_validator, reconciliation_calculator


def test_reconciliation_calculator_detects_unrecorded_fee():
    # gross 1000, fee 30, but bank deposit only 970 -> reconciles
    r = reconciliation_calculator([600.0, 400.0], processor_fees=30.0, bank_deposit=970.0)
    assert r.reconciles
    assert r.expected_net == 970.0


def test_reconciliation_calculator_flags_discrepancy():
    # forgot to record the 30 fee: deposit 970 but books expect 1000
    r = reconciliation_calculator([600.0, 400.0], processor_fees=0.0, bank_deposit=970.0)
    assert not r.reconciles
    assert r.discrepancy == -30.0
    assert "does not reconcile" in r.explanation.lower()


def test_mapping_validator_detects_mismatch():
    r = mapping_validator("item", "coa")
    assert not r.valid
    assert "mismatch" in r.issue.lower()
    assert "align" in r.fix.lower()


def test_mapping_validator_accepts_match():
    r = mapping_validator("coa", "coa")
    assert r.valid


def test_agent_uses_tools_and_retrieval():
    from core.retrieval.store import InMemoryVectorStore
    from modules.erp_sync_reconciliation.agents.diagnostic_agent import DiagnosticAgent
    from modules.erp_sync_reconciliation.service import load_kb

    store = InMemoryVectorStore()
    store.add(load_kb())
    agent = DiagnosticAgent(store)
    result = agent.run(
        "my stripe payout does not match my bank deposit",
        inputs={"gross_payments": [600, 400], "processor_fees": 0, "bank_deposit": 970},
    )
    assert result.citations                                  # retrieved
    assert "reconciliation_calculator" in result.tool_outputs  # tool ran
    assert result.tool_outputs["reconciliation_calculator"]["discrepancy"] == -30.0
    assert any(s.name == "plan" for s in result.steps)        # multi-step


def test_mcp_tool_specs_and_dispatch():
    from core.mcp.server import build_tool_specs, call_tool
    specs = build_tool_specs()
    names = {s["name"] for s in specs}
    assert {"reconciliation_calculator", "mapping_validator"} == names
    out = call_tool("reconciliation_calculator",
                    {"gross_payments": [100, 100], "processor_fees": 5, "bank_deposit": 195})
    assert out["reconciles"] is True


def test_agent_diagnose_endpoint():
    from fastapi.testclient import TestClient
    from core.api.main import app
    client = TestClient(app)
    r = client.post("/modules/erp-sync/agent-diagnose", json={
        "query": "items posting to wrong account after sync",
        "inputs": {"item_mapping_mode": "item", "integration_mode": "coa"},
    })
    assert r.status_code == 200
    body = r.json()
    assert "mapping_validator" in body["tool_outputs"]
    assert body["tool_outputs"]["mapping_validator"]["valid"] is False
