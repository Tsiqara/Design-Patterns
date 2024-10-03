from unittest.mock import ANY
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from pos.infra.fastapi import unit_api
from pos.infra.inmemory import UnitsInMemory


@pytest.fixture
def client() -> TestClient:
    app = FastAPI()
    app.include_router(unit_api)
    app.state.units = UnitsInMemory()
    return TestClient(app)


def test_should_not_read_unknown(client: TestClient) -> None:
    id = uuid4()

    resp = client.get(f"/units/{id}")

    assert resp.status_code == 404
    assert resp.json() == {
        "error": {"message": f"Unit with id<{id}> does not exist."},
    }


def test_should_create(client: TestClient) -> None:
    unit = {"name": "kg"}

    response = client.post("/units", json=unit)

    assert response.status_code == 201
    assert response.json() == {"unit": {"id": ANY, **unit}}


def test_should_persist(client: TestClient) -> None:
    unit = {"name": "kg"}

    response = client.post("/units", json=unit)
    unit_id = response.json()["unit"]["id"]

    response = client.get(f"/units/{unit_id}")

    assert response.status_code == 200
    assert response.json() == {"unit": {"id": unit_id, **unit}}


def test_should_not_create_duplicate(client: TestClient) -> None:
    unit = {"name": "kg"}

    response = client.post("/units", json=unit)
    name = response.json()["unit"]["name"]

    response = client.post("/units", json=unit)
    assert response.status_code == 409
    assert response.json() == {
        "error": {"message": f"Unit with name<{name}> already exists."}
    }


def test_get_all_units_on_empty(client: TestClient) -> None:
    response = client.get("/units")

    assert response.status_code == 200
    assert response.json() == {"units": []}


def test_get_all_units(client: TestClient) -> None:
    unit = {"name": "kg"}

    response = client.post("/units", json=unit)
    unit_id = response.json()["unit"]["id"]

    response = client.get("/units")

    assert response.status_code == 200
    assert response.json() == {"units": [{"id": unit_id, **unit}]}
