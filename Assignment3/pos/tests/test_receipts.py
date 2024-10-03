from __future__ import annotations

import uuid
from typing import Tuple, Any
from unittest.mock import ANY
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.responses import JSONResponse

from pos.core.receipts import Receipt
from pos.core.sales import Sales
from pos.infra.fastapi import unit_api
from pos.infra.fastapi.products import product_api
from pos.infra.fastapi.receipts import receipt_api
from pos.infra.fastapi.sales import sales_api
from pos.infra.inmemory import UnitsInMemory
from pos.infra.inmemory.products import ProductsInMemory
from pos.infra.inmemory.receipts import ReceiptsInMemory
from pos.tests.test_products import create_product


@pytest.fixture
def client() -> TestClient:
    app = FastAPI()
    app.include_router(receipt_api)
    app.include_router(product_api)
    app.include_router(sales_api)
    app.include_router(unit_api)
    app.state.receipts = ReceiptsInMemory()
    app.state.products = ProductsInMemory()
    app.state.sales = Sales()
    app.state.units = UnitsInMemory()
    return TestClient(app)


def test_should_create(client: TestClient) -> None:
    receipt = {"status": "open", "products": [], "total": 0}

    response = client.post("/receipts", json=receipt)

    assert response.status_code == 201
    assert response.json() == {"receipt": {"id": ANY, **receipt}}


def test_should_persist(client: TestClient) -> None:
    receipt = {"status": "open", "products": [], "total": 0}

    response = client.post("/receipts", json=receipt)
    receipt_id = response.json()["receipt"]["id"]

    response = client.get(f"/receipts/{receipt_id}")

    assert response.status_code == 200
    assert response.json() == {"receipt": {"id": receipt_id, **receipt}}


def test_should_not_read_unknown(client: TestClient) -> None:
    id = uuid4()

    resp = client.get(f"/receipts/{id}")

    assert resp.status_code == 404
    assert resp.json() == {
        "error": {"message": f"Receipt with id<{id}> does not exist."},
    }


def test_add_a_product(client: TestClient) -> None:
    receipt = {"status": "open", "products": [], "total": 0}

    response = client.post("/receipts", json=receipt)
    receipt_id = response.json()["receipt"]["id"]

    res = create_product_add_try_to_add_to_receipt(
        client,
        receipt_id,
    )
    response = res[0]
    product_id = res[1]
    products = [{"id": product_id, "quantity": 1, "price": 10, "total": 10}]

    assert response.status_code == 201
    assert response.json() == {
        "receipt": {
            "id": receipt_id,
            "status": "open",
            "products": products,
            "total": 10,
        }
    }


def test_should_not_add_product_to_closed_receipt(client: TestClient) -> None:
    receipt = {"status": "closed", "products": [], "total": 0}

    response = client.post("/receipts", json=receipt)
    receipt_id = response.json()["receipt"]["id"]

    response = create_product_add_try_to_add_to_receipt(
        client,
        receipt_id,
    )[0]
    assert response.status_code == 403
    assert response.json() == {
        "error": {
            "message": f"Receipt with id<{receipt_id}> is closed.",
        }
    }


def create_product_add_try_to_add_to_receipt(client: TestClient, receipt_id: str) -> tuple[Any, int]:
    product = create_product(client, 10)
    response2 = client.post("/products", json=product)
    product_id = response2.json()["product"]["id"]
    request = {
        "receipt_id": receipt_id,
        "product_id": product_id,
        "quantity": 1,
        "price": 10,
        "total": 10,
    }
    response = client.post(f"/receipts/{receipt_id}/products", json=request)
    return response, product_id


def test_should_not_add_product_to_unknown_receipt(client: TestClient) -> None:
    receipt_id = str(uuid4())

    response = create_product_add_try_to_add_to_receipt(
        client,
        receipt_id,
    )[0]
    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "message": f"Receipt with id<{receipt_id}> does not exist.",
        }
    }


def test_close_open_receipt(client: TestClient) -> None:
    receipt = {"status": "open", "products": [], "total": 0}

    response = client.post("/receipts", json=receipt)
    receipt_id = response.json()["receipt"]["id"]

    request = {"status": "closed"}
    response = client.patch(f"/receipts/{receipt_id}", json=request)

    assert response.status_code == 200
    assert response.json() == {}

    response = client.get(f"/receipts/{receipt_id}")
    assert response.json()["receipt"]["status"] == "closed"


def test_should_not_close_unknown_receipt(client: TestClient) -> None:
    receipt_id = str(uuid4())

    request = {"status": "closed"}
    response = client.patch(f"/receipts/{receipt_id}", json=request)

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "message": f"Receipt with id<{receipt_id}> does not exist.",
        }
    }


def test_does_not_close_request_status_not_closed(client: TestClient) -> None:
    receipt = {"status": "open", "products": [], "total": 0}

    response = client.post("/receipts", json=receipt)
    receipt_id = response.json()["receipt"]["id"]

    request = {"status": "clo"}
    response = client.patch(f"/receipts/{receipt_id}", json=request)

    assert response.status_code == 200
    assert response.json() == {}

    response = client.get(f"/receipts/{receipt_id}")
    assert response.json()["receipt"]["status"] == "open"


def test_delete_open_receipt(client: TestClient) -> None:
    receipt = {"status": "open", "products": [], "total": 0}

    response = client.post("/receipts", json=receipt)
    receipt_id = response.json()["receipt"]["id"]

    response = client.delete(f"/receipts/{receipt_id}")
    assert response.status_code == 200
    assert response.json() == {}

    response = client.get(f"/receipts/{receipt_id}")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "message": f"Receipt with id<{receipt_id}> does not exist.",
        }
    }


def test_should_not_delete_closed_receipt(client: TestClient) -> None:
    receipt = {"status": "closed", "products": [], "total": 0}

    response = client.post("/receipts", json=receipt)
    receipt_id = response.json()["receipt"]["id"]

    response = client.delete(f"/receipts/{receipt_id}")
    assert response.status_code == 403
    assert response.json() == {
        "error": {
            "message": f"Receipt with id<{receipt_id}> is closed.",
        }
    }


def test_should_not_delete_unknown_receipt(client: TestClient) -> None:
    receipt_id = str(uuid.uuid4())

    response = client.delete(f"/receipts/{receipt_id}")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "message": f"Receipt with id<{receipt_id}> does not exist.",
        }
    }


def test_sales_report_empty(client: TestClient) -> None:
    response = client.get("/sales")

    assert response.status_code == 200
    assert response.json() == {"sales": {"n_receipts": 0, "revenue": 0}}


def test_sales_report_empty_because_open_receipts(client: TestClient) -> None:
    receipt = {"status": "open", "products": [], "total": 0}

    response = client.post("/receipts", json=receipt)
    response = client.get("/sales")

    assert response.status_code == 200
    assert response.json() == {"sales": {"n_receipts": 0, "revenue": 0}}


def test_sales_report(client: TestClient) -> None:
    receipt = {
        "status": "closed",
        "products": [
            {
                "id": "7d3184ae-80cd-417f-8b14-e3de42a98031",
                "quantity": 12,
                "price": 10,
                "total": 120,
            }
        ],
        "total": 120,
    }

    response = client.post("/receipts", json=receipt)
    response = client.get("/sales")

    assert response.status_code == 200
    assert response.json() == {
        "sales": {"n_receipts": 1, "revenue": float(120)},
    }
