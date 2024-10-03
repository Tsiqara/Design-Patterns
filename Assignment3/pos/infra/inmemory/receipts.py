from dataclasses import dataclass, field
from uuid import UUID

from pos.core.errors import ClosedError, DoesNotExistError
from pos.core.receipts import Receipt
from pos.core.sales import Sales


@dataclass
class ReceiptsInMemory:
    receipts: dict[UUID, Receipt] = field(default_factory=dict)

    def create(self, receipt: Receipt) -> None:
        self.receipts[receipt.get_id()] = receipt

    def add_product(
        self,
        receipt_id: UUID,
        product_id: UUID,
        quantity: int,
        price: float,
        total: float,
    ) -> None:
        id = receipt_id
        try:
            receipt = self.receipts[receipt_id]
            if not receipt.is_open():
                raise ClosedError(receipt_id)
            (self.receipts[id].add_product(product_id, quantity, price, total))
        except KeyError:
            raise DoesNotExistError(receipt_id)

    def read_by_id(self, receipt_id: UUID) -> Receipt:
        try:
            return self.receipts[receipt_id]
        except KeyError:
            raise DoesNotExistError(receipt_id)

    def close(self, receipt_id: UUID) -> None:
        try:
            self.receipts[receipt_id].close()
        except KeyError:
            raise DoesNotExistError(receipt_id)

    def delete(self, receipt_id: UUID) -> None:
        try:
            receipt = self.receipts[receipt_id]
            if not receipt.is_open():
                raise ClosedError(receipt_id)
            del self.receipts[receipt_id]
        except KeyError:
            raise DoesNotExistError(receipt_id)

    def sales_report(self) -> Sales:
        n_rec = 0
        revenue = 0.0
        for receipt in self.receipts.values():
            if not receipt.is_open():
                n_rec += 1
            revenue += receipt.get_total()
        return Sales(n_rec, revenue)
