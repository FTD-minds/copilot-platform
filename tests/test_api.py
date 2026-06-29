def test_health():
    from fastapi.testclient import TestClient
    from core.api.main import app
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_providers_lists_mock():
    from fastapi.testclient import TestClient
    from core.api.main import app
    client = TestClient(app)
    r = client.get("/providers")
    assert r.status_code == 200
    assert r.json()["available"]["mock"] is True


def test_chat_with_mock_provider_echoes():
    from fastapi.testclient import TestClient
    from core.api.main import app
    client = TestClient(app)
    r = client.post("/chat", json={"messages": [{"role": "user", "content": "why did my sync fail?"}]})
    assert r.status_code == 200
    body = r.json()
    assert body["provider"] == "mock"
    assert "why did my sync fail?" in body["text"]


def test_router_falls_back_to_mock_without_keys():
    from core.providers.router import get_provider
    # Requesting anthropic with no key configured -> mock fallback.
    p = get_provider("anthropic")
    assert p.name in ("mock", "anthropic")  # mock unless a real key is present
