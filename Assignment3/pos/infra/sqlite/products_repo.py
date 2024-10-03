import uuid
from dataclasses import dataclass
from sqlite3 import Connection, Cursor
from uuid import UUID

from pos.core.errors import DoesNotExistError, ExistsError
from pos.core.products import Product


@dataclass
class SQLProductRepository:
    con: Connection
    cur: Cursor

    def create(self, product: Product) -> None:
        self.cur.execute(
            "SELECT * FROM products WHERE barcode = :code",
            {"code": product.get_barcode()},
        )
        if len(list(self.cur.fetchall())) != 0:
            raise ExistsError(product.get_barcode())
        self.cur.execute(
            "INSERT INTO products VALUES (?, ?, ?, ?, ?)",
            (
                str(product.get_id()),
                str(product.get_unit_id()),
                product.get_name(),
                product.get_barcode(),
                product.get_price(),
            ),
        )

        self.con.commit()

    def read_one(self, product_id: UUID) -> Product:
        r = self._check_exists(product_id)
        res = r[0]
        return Product(
            id=uuid.UUID(res[0]),
            unit_id=uuid.UUID(res[1]),
            name=res[2],
            barcode=res[3],
            price=float(res[4]),
        )

    def _check_exists(self, product_id: UUID) -> list[str]:
        id = str(product_id)
        self.cur.execute("SELECT * FROM products WHERE ID = :id", {"id": id})
        res = list(self.cur.fetchall())
        if len(res) == 0:
            raise DoesNotExistError(product_id)
        return res

    def list(self) -> list[Product]:
        self.cur.execute("SELECT * FROM products")
        res = list(self.cur.fetchall())
        return [
            Product(
                id=uuid.UUID(r[0]),
                unit_id=uuid.UUID(r[1]),
                name=r[2],
                barcode=r[3],
                price=r[4],
            )
            for r in res
        ]

    def update(self, product_id: UUID, new_price: float) -> None:
        self._check_exists(product_id)
        id = str(product_id)
        self.cur.execute(
            "UPDATE products SET price = :price WHERE ID = :id",
            {"price": new_price, "id": id},
        )
        self.con.commit()
