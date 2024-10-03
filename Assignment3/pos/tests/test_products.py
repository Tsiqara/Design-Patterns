from dataclasses import dataclass, field
from typing import Any, Dict
from unittest.mock import ANY
from uuid import UUID, uuid4

import pytest
from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient

from pos.core.products import Product
from pos.infra.fastapi import unit_api
from pos.infra.fastapi.products import product_api
from pos.infra.inmemory import UnitsInMemory
from pos.infra.inmemory.products import ProductsInMemory


@pytest.fixture
def client() -> TestClient:
    app = FastAPI()
    app.include_router(product_api)
    app.include_router(unit_api)
    app.state.products = ProductsInMemory()
    app.state.units = UnitsInMemory()
    return TestClient(app)


@dataclass
class Fake:
    faker: Faker = field(default_factory=Faker)

    def product(
        self, id: UUID = uuid4(), barcode: str = "", price: float = 0
    ) -> dict[str, Any]:
        return {
            "unit_id": id,
            "name": "Apple",
            "barcode": barcode or self.faker.ean13(),
            "price": price,
        }


def test_should_create(client: TestClient) -> None:
    product = create_product(client)

    response = client.post("/products", json=product)

    assert response.status_code == 201
    assert response.json() == {"product": {"id": ANY, **product}}


def test_should_persist(client: TestClient) -> None:
    product = create_product(client)

    response = client.post("/products", json=product)
    product_id = response.json()["product"]["id"]

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200
    assert response.json() == {"product": {"id": product_id, **product}}


def test_should_not_create_duplicate(client: TestClient) -> None:
    product = create_product(client)

    response = client.post("/products", json=product)
    barcode = response.json()["product"]["barcode"]

    response = client.post("/products", json=product)
    assert response.status_code == 409
    assert response.json() == {
        "error": {
            "message": f"Product with barcode<{barcode}> already exists.",
        }
    }


def test_should_not_read_unknown(client: TestClient) -> None:
    id = uuid4()

    resp = client.get(f"/products/{id}")

    assert resp.status_code == 404
    assert resp.json() == {
        "error": {"message": f"Product with id<{id}> does not exist."}
    }


def test_get_all_products_on_empty(client: TestClient) -> None:
    response = client.get("/products")

    assert response.status_code == 200
    assert response.json() == {"products": []}


def test_get_all_products(client: TestClient) -> None:
    product = create_product(client)

    response = client.post("/products", json=product)
    product_id = response.json()["product"]["id"]

    response = client.get("/products")

    assert response.status_code == 200
    assert response.json() == {"products": [{"id": product_id, **product}]}


def create_product(client: TestClient, price: float = 0) -> dict[str, Any]:
    unit = {"name": "kg"}
    response = client.post("/units", json=unit)
    unit_id = response.json()["unit"]["id"]
    product = Fake().product(id=unit_id, price=price)
    return product


def test_does_not_update_unknown(client: TestClient) -> None:
    id = uuid4()
    price = {"price": 100}

    resp = client.patch(f"/products/{id}", json=price)

    assert resp.status_code == 404
    assert resp.json() == {
        "error": {"message": f"Product with id<{id}> does not exist."}
    }


def test_update(client: TestClient) -> None:
    product = create_product(client)
    price = {"price": 100}

    response = client.post("/products", json=product)
    product_id = response.json()["product"]["id"]

    response = client.patch(f"/products/{product_id}", json=price)

    assert response.status_code == 200

    response = client.get(f"/products/{product_id}")
    assert response.json()["product"]["price"] == 100
