from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


def test_dashboard_renders_all_six_panels() -> None:
    response = TestClient(app).get("/dashboard")

    assert response.status_code == 200
    for title in ("Latency &amp; TTFT", "Traffic", "Errors &amp; retrieval", "Cost", "Tokens", "Quality"):
        assert title in response.text
