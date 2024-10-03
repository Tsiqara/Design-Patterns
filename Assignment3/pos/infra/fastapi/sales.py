from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from pos.infra.fastapi import ReceiptRepoDependable

sales_api = APIRouter(tags=["Sales"])


class SalesItem(BaseModel):
    n_receipts: int = Field(examples=[23])
    revenue: float = Field(examples=[456890])


class SalesItemEnvelope(BaseModel):
    sales: SalesItem


@sales_api.get("/sales", response_model=SalesItemEnvelope)
def report(receipts: ReceiptRepoDependable) -> dict[str, Any]:
    return {"sales": receipts.sales_report()}
