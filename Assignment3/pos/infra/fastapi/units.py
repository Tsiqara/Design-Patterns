from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

from pos.core.errors import DoesNotExistError, ExistsError
from pos.core.units import Unit
from pos.infra.fastapi.dependables import UnitRepositoryDependable

unit_api = APIRouter(tags=["Units"])


class CreateUnitRequest(BaseModel):
    name: str = Field(examples=["კგ"])


class UnitItem(BaseModel):
    id: UUID
    name: str = Field(examples=["კგ"])


class UnitItemEnvelope(BaseModel):
    unit: UnitItem


class UnitListEnvelope(BaseModel):
    units: list[UnitItem]


class UnitExistsResponse(BaseModel):
    error: dict[str, Any] = Field(
        default_factory=dict,
        example={"message": "Unit with name<კგ> already exists."},
    )


class UnitDoesNotExistResponse(BaseModel):
    _ex_id = "27b4f218-1cc2-4694-b131-ad481dc08901"
    error: dict[str, Any] = Field(
        default_factory=dict,
        example={"message": ("Unit with id<%s> does not exist." % _ex_id)},
    )


@unit_api.post(
    "/units",
    status_code=201,
    response_model=UnitItemEnvelope,
    responses={
        409: {
            "model": UnitExistsResponse,
            "description": "Unit already exists",
        }
    },
)
def create_unit(
    request: CreateUnitRequest, units: UnitRepositoryDependable
) -> dict[str, Unit] | JSONResponse:
    unit = Unit(**request.dict())
    name = unit.get_name()
    try:
        units.create(unit)
        return {"unit": unit}
    except ExistsError:
        return JSONResponse(
            status_code=409,
            content={
                "error": {
                    "message": f"Unit with name<{name}> already exists.",
                },
            },
        )


@unit_api.get(
    "/units/{unit_id}",
    status_code=200,
    response_model=UnitItemEnvelope,
    responses={
        404: {
            "model": UnitDoesNotExistResponse,
            "description": "Unit does not exist",
        }
    },
)
def read_one(
    unit_id: UUID, units: UnitRepositoryDependable
) -> dict[str, Any] | JSONResponse:
    try:
        return {"unit": units.read_one(unit_id)}
    except DoesNotExistError:
        _id = unit_id
        return JSONResponse(
            status_code=404,
            content={
                "error": {"message": f"Unit with id<{_id}> does not exist."},
            },
        )


@unit_api.get("/units", response_model=UnitListEnvelope)
def list(units: UnitRepositoryDependable) -> dict[str, Any] | JSONResponse:
    return {"units": units.list()}
