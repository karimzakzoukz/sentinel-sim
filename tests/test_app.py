"""Sentinel-Sim tests — quick smoke tests for the clean baseline."""
import os
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure required environment variables are set for tests
os.environ.setdefault("DATABASE_URL", "sqlite:///./sentinel-sim.db")
os.environ.setdefault("DB_PASSWORD", "default-password")
os.environ.setdefault("LOG_LEVEL", "INFO")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_healthz(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_readyz(client):
    r = client.get("/readyz")
    assert r.status_code == 200
    assert r.json()["status"] == "ready"


def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "sentinel-sim"
    assert body["version"] == "1.0.0"


def test_pay(client):
    r = client.get("/pay", params={"amount": 500})
    assert r.status_code == 200
    assert r.json()["status"] == "processed"
