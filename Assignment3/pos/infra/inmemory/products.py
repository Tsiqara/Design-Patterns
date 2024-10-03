from dataclasses import dataclass, field
from uuid import UUID

from pos.core.errors import DoesNotExistError, ExistsError
from pos.core.products import Product


@dataclass
class ProductsInMemory:
    products: dict[UUID, Product] = field(default_factory=dict)

    def create(self, product: Product) -> None:
        for p in self.products.values():
            if product.get_barcode() == p.get_barcode():
                raise ExistsError(product.get_barcode())
        self.products[product.get_id()] = product

    def read_one(self, product_id: UUID) -> Product:
        try:
            return self.products[product_id]
        except KeyError:
            raise DoesNotExistError(product_id)

    def list(self) -> list[Product]:
        return list(self.products.values())

    def update(self, product_id: UUID, new_price: float) -> None:
        try:
            self.products[product_id].set_price(new_price)
        except KeyError:
            raise DoesNotExistError(product_id)
