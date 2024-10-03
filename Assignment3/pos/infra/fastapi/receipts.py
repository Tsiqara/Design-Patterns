from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

from pos.core.errors import DoesNotExistError
from pos.core.receipts import Receipt
from pos.infra.fastapi import ProductRepoDependable, ReceiptRepoDependable
from pos.infra.fastapi.products import ProductDoesNotExistResponse

receipt_api = APIRouter(tags=["Receipts"])


class ReceiptProduct(BaseModel):
    id: UUID = Field(examples=["7d3184ae-80cd-417f-8b14-e3de42a98031"])
    quantity: float = Field(examples=[123])
    price: float = Field(examples=[520])
    total: float = Field(examples=[63960])


class CreateReceipt(BaseModel):
    status: str = Field(examples=["open"])
    products: list[ReceiptProduct] = Field(examples=[list()])
    total: float = Field(examples=[0])


class ReceiptEmptyItem(BaseModel):
    id: UUID = Field(examples=["25f13441-5fab-4b12-aefe-3fa0089fb63a"])
    status: str = Field(examples=["open"])
    products: list[ReceiptProduct] = Field(examples=[list()])
    total: float = Field(examples=[0])


class ReceiptEmptyItemEnvelope(BaseModel):
    receipt: ReceiptEmptyItem


class ReceiptItem(BaseModel):
    id: UUID = Field(examples=["25f13441-5fab-4b12-aefe-3fa0089fb63a"])
    status: str = Field(examples=["open"])
    products: list[ReceiptProduct] = Field(examples=[])
    total: float = Field(examples=[63960])


class ReceiptItemEnvelope(BaseModel):
    receipt: ReceiptItem


class AddProductRequest(BaseModel):
    product_id: UUID = Field(examples=["7d3184ae-80cd-417f-8b14-e3de42a98031"])
    quantity: int = Field(examples=[123])


class ReceiptClosedRequest(BaseModel):
    status: str = Field(examples=["closed"])


class ReceiptDoesNotExistResponse(BaseModel):
    _id = "25f13441-5fab-4b12-aefe-3fa0089fb63a"
    error: dict[str, Any] = Field(
        default_factory=dict,
        example={"message": ("Receipt with id<%s> does not exist." % _id)},
    )


class ReceiptClosedResponse(BaseModel):
    _id = "25f13441-5fab-4b12-aefe-3fa0089fb63a"
    error: dict[str, Any] = Field(
        default_factory=dict,
        example={"message": ("Receipt with id<%s> is closed." % _id)},
    )


@receipt_api.post(
    "/receipts",
    status_code=201,
    response_model=ReceiptEmptyItemEnvelope,
)
def create_receipt(
    request: CreateReceipt, receipts: ReceiptRepoDependable
) -> dict[str, Receipt]:
    receipt = Receipt(**request.dict())
    receipts.create(receipt)
    return {"receipt": receipt}


@receipt_api.post(
    "/receipts/{receipt_id}/products",
    status_code=201,
    response_model=ReceiptItemEnvelope,
    responses={
        403: {
            "model": ReceiptClosedResponse,
            "description": "Receipt is closed",
        },
        404: {
            "model": ReceiptDoesNotExistResponse,
            "description": "Receipt does not exist",
        },
        405: {
            "model": ProductDoesNotExistResponse,
            "description": "Product does not exist",
        },
    },
)
def add_a_product(
    request: AddProductRequest,
    receipt_id: UUID,
    receipts: ReceiptRepoDependable,
    products: ProductRepoDependable,
) -> JSONResponse | dict[str, Receipt]:
    product_id = request.product_id
    quantity = request.quantity
    try:
        product = products.read_one(product_id)
    except DoesNotExistError:
        _id = product_id
        return JSONResponse(
            status_code=405,
            content={
                "error": {
                    "message": f"Product with id<{_id}> does not exist.",
                }
            },
        )
    price = product.get_price()
    total = quantity * price
    try:
        receipt = receipts.read_by_id(receipt_id)
    except DoesNotExistError:
        _id = receipt_id
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "message": f"Receipt with id<{_id}> does not exist.",
                }
            },
        )
    if not receipt.is_open():
        return JSONResponse(
            status_code=403,
            content={
                "error": {
                    "message": f"Receipt with id<{receipt_id}> is closed.",
                }
            },
        )
    old_total = receipt.get_total()
    receipts.add_product(receipt_id, product_id, quantity, price, total)
    return {
        "receipt": Receipt(
            id=receipt_id,
            status="open",
            total=old_total + total,
            products=receipts.read_by_id(receipt_id).get_products(),
        )
    }


@receipt_api.get(
    "/receipts/{receipt_id}",
    status_code=200,
    response_model=ReceiptItemEnvelope,
    responses={
        404: {
            "model": ReceiptDoesNotExistResponse,
            "description": "Receipt does not exist",
        }
    },
)
def read_by_id(
    receipt_id: UUID, receipts: ReceiptRepoDependable
) -> dict[str, Any] | JSONResponse:
    try:
        return {"receipt": receipts.read_by_id(receipt_id)}
    except DoesNotExistError:
        _id = receipt_id
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "message": f"Receipt with id<{_id}> does not exist.",
                }
            },
        )


@receipt_api.patch(
    "/receipts/{receipt_id}",
    responses={
        200: {"model": BaseModel},
        404: {
            "model": ReceiptDoesNotExistResponse,
            "description": "Receipt does not exist",
        },
    },
)
def close(
    request: ReceiptClosedRequest,
    receipt_id: UUID,
    receipts: ReceiptRepoDependable,
) -> JSONResponse:
    try:
        if request.status == "closed":
            receipts.close(receipt_id)
        return JSONResponse(status_code=200, content={})
    except DoesNotExistError:
        _id = receipt_id
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "message": f"Receipt with id<{_id}> does not exist.",
                }
            },
        )


@receipt_api.delete(
    "/receipts/{receipt_id}",
    status_code=200,
    responses={
        200: {"model": BaseModel},
        403: {
            "model": ReceiptClosedResponse,
            "description": "Receipt is closed",
        },
        404: {
            "model": ReceiptDoesNotExistResponse,
            "description": "Receipt does not exist",
        },
    },
)
def delete(receipt_id: UUID, receipts: ReceiptRepoDependable) -> JSONResponse:
    try:
        receipt = receipts.read_by_id(receipt_id)
        if not receipt.is_open():
            return JSONResponse(
                status_code=403,
                content={
                    "error": {
                        "message": f"Receipt with id<{receipt_id}> is closed.",
                    }
                },
            )
        receipts.delete(receipt_id)
        return JSONResponse(status_code=200, content={})
    except DoesNotExistError:
        _id = receipt_id
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "message": f"Receipt with id<{_id}> does not exist.",
                }
            },
        )
