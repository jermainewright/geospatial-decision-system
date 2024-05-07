from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analysis_returns_top_five() -> None:
    payload = {
        "state": "TX",
        "grid_size": 1000,
        "competition_buffer_km": 5,
        "seed": 13,
        "weights": {"population": 0.5, "roads": 0.3, "competition": 0.2},
    }

    response = client.post("/api/v1/analysis/run", json=payload)
    body = response.json()

    assert response.status_code == 200
    assert body["candidates_analyzed"] == 1000
    assert len(body["top_locations"]) == 5
    assert body["top_locations"][0]["suitability_index"] >= body["top_locations"][4]["suitability_index"]
