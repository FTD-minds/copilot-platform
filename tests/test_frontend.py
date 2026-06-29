def test_ui_served_at_root():
    from fastapi.testclient import TestClient
    from core.api.main import app
    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200
    assert "Enterprise AI Copilot Platform" in r.text


def test_evals_api_returns_metrics():
    from fastapi.testclient import TestClient
    from core.api.main import app
    client = TestClient(app)
    r = client.get("/api/evals")
    assert r.status_code == 200
    body = r.json()
    assert "retrieval_accuracy" in body["metrics"]
    assert body["passing"] is True
    assert len(body["cases"]) == 8
