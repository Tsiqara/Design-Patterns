from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4


@dataclass
class Product:
    unit_id: UUID
    name: str
    barcode: str
    price: float
    id: UUID = field(default_factory=uuid4)

    def get_id(self) -> UUID:
        return self.id

    def get_unit_id(self) -> UUID:
        return self.unit_id

    def get_name(self) -> str:
        return self.name

    def get_barcode(self) -> str:
        return self.barcode

    def get_price(self) -> float:
        return self.price

    def set_price(self, price: float) -> None:
        self.price = price


class ProductRepository(Protocol):
    def create(self, product: Product) -> None:
        pass

    def read_one(self, product_id: UUID) -> Product:
        pass

    def list(self) -> list[Product]:
        pass

    def update(self, product_id: UUID, new_price: float) -> None:
        pass
