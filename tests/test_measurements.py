from datetime import datetime

from fastapi.testclient import TestClient


def test_list_sites(client: TestClient) -> None:
    response = client.get("/sites")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_create_measurement(client: TestClient) -> None:
    payload = {
        "site_id": 1,
        "sampled_at": datetime(2026, 4, 12, 8, 30).isoformat(),
        "ph_value": 6.8,
        "chlorine_value": 3.0,
        "area": "Tanque 1",
        "observation": "Muestreo de rutina",
    }
    response = client.post("/measurements", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["site_id"] == 1
    assert data["ph_value"] == 6.8
    assert data["chlorine_value"] == 3.0
