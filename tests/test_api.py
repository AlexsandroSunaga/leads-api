import json

import pytest
from fastapi.testclient import TestClient

import src.services.lead_store as backend_store
from src.main import backend_app

PREFIX = "/api/v1"
LEAD = {
    "email": "jane@example.com",
    "name": "Jane Doe",
    "company": "Acme",
    "message": "Interested in a demo.",
}


@pytest.fixture
def client(tmp_path, monkeypatch):
    store = tmp_path / "leads.jsonl"
    monkeypatch.setattr(backend_store, "STORE", store)
    with TestClient(backend_app) as c:
        c.store = store
        yield c


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_create_lead_persists_jsonl_record(client):
    r = client.post(f"{PREFIX}/leads", json=LEAD)
    assert r.status_code == 200
    assert r.json()["status"] == "queued"
    rows = [json.loads(line) for line in client.store.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1
    assert rows[0]["email"] == "jane@example.com" and rows[0]["source"] == "website"
    assert rows[0]["id"] == r.json()["id"]


def test_recent_returns_newest_first_and_honours_limit(client):
    for i in range(3):
        client.post(f"{PREFIX}/leads", json={**LEAD, "name": f"Lead {i}"})
    recent = client.get(f"{PREFIX}/leads/recent", params={"limit": 2}).json()
    assert [r["name"] for r in recent] == ["Lead 2", "Lead 1"]


def test_recent_empty_and_limit_validation(client):
    assert client.get(f"{PREFIX}/leads/recent").json() == []
    assert client.get(f"{PREFIX}/leads/recent", params={"limit": 101}).status_code == 400
    assert client.get(f"{PREFIX}/leads/recent", params={"limit": 0}).status_code == 400


def test_lead_validation_errors(client):
    assert client.post(f"{PREFIX}/leads", json={**LEAD, "email": "not-an-email"}).status_code == 422
    assert client.post(f"{PREFIX}/leads", json={**LEAD, "name": ""}).status_code == 422
    assert client.post(f"{PREFIX}/leads", json={"email": "a@b.co"}).status_code == 422


def test_backend_integrations_status():
    with TestClient(backend_app) as c:
        assert set(c.get(f"{PREFIX}/integrations/status").json()) == {"hubspot", "sendgrid", "clearbit"}
