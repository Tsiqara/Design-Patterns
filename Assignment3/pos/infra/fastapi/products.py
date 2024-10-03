from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

from pos.core.errors import DoesNotExistError, ExistsError
from pos.core.products import Product
from pos.infra.fastapi.dependables import (
    ProductRepoDependable,
    UnitRepositoryDependable,
)
from pos.infra.fastapi.units import UnitDoesNotExistResponse

product_api = APIRouter(tags=["Products"])


class CreateProductRequest(BaseModel):
    unit_id: UUID = Field(examples=["27b4f218-1cc2-4694-b131-ad481dc08901"])
    name: str = Field(examples=["Apple"])
    barcode: str = Field(examples=["1234567890"])
    price: float = Field(examples=[520])


class UpdateProductRequest(BaseModel):
    price: float = Field(examples=[530])


class ProductItem(BaseModel):
    id: UUID
    unit_id: UUID = Field(examples=["27b4f218-1cc2-4694-b131-ad481dc08901"])
    name: str = Field(examples=["Apple"])
    barcode: str = Field(examples=["1234567890"])
    price: float = Field(examples=[520])


class ProductItemEnvelope(BaseModel):
    product: ProductItem


class ProductListEnvelope(BaseModel):
    products: list[ProductItem]


class ProductExistsResponse(BaseModel):
    error: dict[str, Any] = Field(
        default_factory=dict,
        example={
            "message": "Product with barcode<1234567890> already exists.",
        },
    )


class ProductDoesNotExistResponse(BaseModel):
    _id = "7d3184ae-80cd-417f-8b14-e3de42a98031"
    error: dict[str, Any] = Field(
        default_factory=dict,
        example={"message": ("Product with id<%s> does not exist." % _id)},
    )


@product_api.post(
    "/products",
    status_code=201,
    response_model=ProductItemEnvelope,
    responses={
        409: {
            "model": ProductExistsResponse,
            "description": "Product already exists",
        },
        404: {
            "model": UnitDoesNotExistResponse,
            "description": "Unit does not exist",
        },
    },
)
def create_product(
    request: CreateProductRequest,
    products: ProductRepoDependable,
    units: UnitRepositoryDependable,
) -> dict[str, Product] | JSONResponse:
    product = Product(**request.dict())
    unit_id = product.get_unit_id()
    try:
        units.read_one(unit_id)
    except DoesNotExistError:
        _id = unit_id
        return JSONResponse(
            status_code=404,
            content={
                "error": {"message": f"Unit with id<{_id}> does not exist."},
            },
        )

    code = product.get_barcode()
    try:
        products.create(product)
        return {"product": product}
    except ExistsError:
        return JSONResponse(
            status_code=409,
            content={
                "error": {
                    "message": f"Product with barcode<{code}> already exists.",
                },
            },
        )


@product_api.get(
    "/products/{product_id}",
    status_code=200,
    response_model=ProductItemEnvelope,
    responses={
        404: {
            "model": ProductDoesNotExistResponse,
            "description": "Product does not exist",
        }
    },
)
def read_one(
    product_id: UUID, products: ProductRepoDependable
) -> dict[str, Any] | JSONResponse:
    try:
        return {"product": products.read_one(product_id)}
    except DoesNotExistError:
        _id = product_id
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "message": f"Product with id<{_id}> does not exist.",
                }
            },
        )


@product_api.get("/products", response_model=ProductListEnvelope)
def list(products: ProductRepoDependable) -> dict[str, Any]:
    return {"products": products.list()}


@product_api.patch(
    "/products/{product_id}",
    responses={
        200: {"model": BaseModel},
        404: {
            "model": ProductDoesNotExistResponse,
            "description": "Product does not exist",
        },
    },
)
def update(
    request: UpdateProductRequest,
    product_id: UUID,
    products: ProductRepoDependable,
) -> JSONResponse:
    new_price = request.price
    try:
        products.update(product_id, new_price)
        return JSONResponse(status_code=200, content={})
    except DoesNotExistError:
        _id = product_id
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "message": f"Product with id<{_id}> does not exist.",
                }
            },
        )
