def test_retrieval_finds_relevant_kb_entry():
    from core.retrieval.store import InMemoryVectorStore
    from modules.erp_sync_reconciliation.service import load_kb
    store = InMemoryVectorStore()
    store.add(load_kb())
    hits = store.search("stripe payout does not match my bank deposit amount", k=3)
    assert hits
    # The Stripe/ACH payout entry should surface in the top results.
    assert any(h.doc.id == "kb-003" for h in hits)


def test_diagnose_returns_grounded_answer_with_citations():
    from modules.erp_sync_reconciliation.service import ReconciliationCopilot
    copilot = ReconciliationCopilot()
    result = copilot.diagnose("undeposited funds are not clearing in QBO", k=3)
    assert result.citations                      # has citations
    assert result.provider == "mock"             # hermetic default
    assert any(c.id.startswith("kb-") for c in result.citations)
    assert "kb-" in result.answer                # answer cites a source


def test_diagnose_endpoint():
    from fastapi.testclient import TestClient
    from core.api.main import app
    client = TestClient(app)
    r = client.post("/modules/erp-sync/diagnose",
                    json={"query": "canada sales tax synced to the wrong agency"})
    assert r.status_code == 200
    body = r.json()
    assert body["citations"]
    assert any(c["id"] == "kb-005" for c in body["citations"])
