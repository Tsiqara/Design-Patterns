from dataclasses import dataclass, field
from typing import Protocol, Union
from uuid import UUID, uuid4

from pos.core.sales import Sales


@dataclass
class Receipt:
    id: UUID = field(default_factory=uuid4)
    status: str = field(default="open")
    products: list[dict[str, Union[float, UUID]]] = field(default_factory=list)
    total: float = field(default=0)

    def get_products(self) -> list[dict[str, Union[float, UUID]]]:
        return self.products

    def get_total(self) -> float:
        return self.total

    def get_id(self) -> UUID:
        return self.id

    def get_status(self) -> str:
        return self.status

    def close(self) -> None:
        self.status = "closed"

    def is_open(self) -> bool:
        return self.status == "open"

    def add_product(
        self, product_id: UUID, quantity: int, price: float, total: float
    ) -> None:
        self.products.append(
            {
                "id": product_id,
                "quantity": quantity,
                "price": price,
                "total": total,
            }
        )


class ReceiptRepository(Protocol):
    def create(self, receipt: Receipt) -> None:
        pass

    def add_product(
        self,
        receipt_id: UUID,
        product_id: UUID,
        quantity: int,
        price: float,
        total: float,
    ) -> None:
        pass

    def read_by_id(self, receipt_id: UUID) -> Receipt:
        pass

    def close(self, receipt_id: UUID) -> None:
        pass

    def delete(self, receipt_id: UUID) -> None:
        pass

    def sales_report(self) -> Sales:
        pass
