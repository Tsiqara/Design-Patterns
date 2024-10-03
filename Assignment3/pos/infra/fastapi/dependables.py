from typing import Annotated

from fastapi import Depends
from fastapi.requests import Request

from pos.core.products import ProductRepository
from pos.core.receipts import ReceiptRepository
from pos.core.units import UnitRepository


def get_unit_repo(request: Request) -> UnitRepository:
    return request.app.state.units  # type: ignore


def get_product_repo(request: Request) -> ProductRepository:
    return request.app.state.products  # type: ignore


def get_receipt_repo(request: Request) -> ReceiptRepository:
    return request.app.state.receipts  # type: ignore


UnitRepositoryDependable = Annotated[UnitRepository, Depends(get_unit_repo)]
ProductRepoDependable = Annotated[ProductRepository, Depends(get_product_repo)]
ReceiptRepoDependable = Annotated[ReceiptRepository, Depends(get_receipt_repo)]
