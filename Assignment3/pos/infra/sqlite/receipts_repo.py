from __future__ import annotations

from dataclasses import dataclass
from sqlite3 import Connection, Cursor
from uuid import UUID

from pos.core.errors import ClosedError, DoesNotExistError
from pos.core.receipts import Receipt
from pos.core.sales import Sales


@dataclass
class SQLReceiptRepository:
    con: Connection
    cur: Cursor

    def create(self, receipt: Receipt) -> None:
        self.cur.execute(
            "INSERT INTO receipts VALUES (?, ?, ?)",
            (str(receipt.get_id()), receipt.get_status(), receipt.get_total()),
        )
        products = receipt.get_products()
        for i in range(len(products)):
            self.cur.execute(
                "INSERT INTO receipt_product VALUES (?, ?, ?, ?, ?)",
                (
                    str(products[i]["id"]),
                    products[i]["quantity"],
                    products[i]["price"],
                    products[i]["total"],
                    str(receipt.get_id()),
                ),
            )

        self.con.commit()

    def add_product(
        self,
        receipt_id: UUID,
        product_id: UUID,
        quantity: int,
        price: float,
        total: float,
    ) -> None:
        self._check_exists_and_open(receipt_id)
        self.cur.execute(
            "SELECT quantity FROM receipt_product "
            "WHERE receipt_id = :id AND product_id = :pid",
            {"id": str(receipt_id), "pid": str(product_id)},
        )
        res = self.cur.fetchall()
        if len(res) != 0:
            old_quan = res[0][0]
            self.cur.execute(
                "UPDATE receipt_product SET quantity =:q, total = :total WHERE product_id=:id",
                {
                    "q": old_quan + quantity,
                    "id": str(product_id),
                    "total": (old_quan + quantity) * price,
                },
            )
        else:
            self.cur.execute(
                "INSERT INTO receipt_product VALUES (?, ?, ?, ?, ?)",
                (str(product_id), quantity, price, total, str(receipt_id)),
            )
            self.con.commit()
        self.cur.execute(
            "SELECT total FROM receipts WHERE ID = :id",
            {"id": str(receipt_id)},
        )
        old_total = self.cur.fetchone()[0]
        self.cur.execute(
            "UPDATE receipts SET total = :total WHERE ID = :id",
            {"total": old_total + total, "id": str(receipt_id)},
        )
        self.con.commit()

    def _check_exists_and_open(self, receipt_id: UUID) -> None:
        res = self._check_exists(receipt_id)
        if res[1] != "open":
            raise ClosedError(receipt_id)

    def read_by_id(self, receipt_id: UUID) -> Receipt:
        res = self._check_exists(receipt_id)
        self.cur.execute(
            "SELECT * FROM receipt_product WHERE receipt_id = :id",
            {"id": str(receipt_id)},
        )
        res2 = list(self.cur.fetchall())
        products = [
            {
                "id": r[0],
                "quantity": r[1],
                "price": r[2],
                "total": r[3],
            }
            for r in res2
        ]
        total = sum(r[3] for r in res2)
        return Receipt(
            id=UUID(res[0]),
            status=res[1],
            products=products,
            total=total,
        )

    def _check_exists(self, receipt_id: UUID) -> list[str]:
        id = str(receipt_id)
        self.cur.execute("SELECT * FROM receipts WHERE ID = :id", {"id": id})
        res = list(self.cur.fetchall())
        if len(res) == 0:
            raise DoesNotExistError(receipt_id)
        return list(res[0])

    def close(self, receipt_id: UUID) -> None:
        self._check_exists(receipt_id)
        id = str(receipt_id)
        self.cur.execute(
            "UPDATE receipts SET status = :status WHERE ID = :id",
            {"status": "closed", "id": id},
        )
        self.con.commit()

    def delete(self, receipt_id: UUID) -> None:
        self._check_exists_and_open(receipt_id)
        id = str(receipt_id)
        self.cur.execute("DELETE FROM receipts WHERE ID = :id", {"id": id})
        self.con.commit()
        self.cur.execute(
            "DELETE FROM receipt_product WHERE receipt_id = :id", {"id": id}
        )
        self.con.commit()

    def sales_report(self) -> Sales:
        self.cur.execute(
            "SELECT COUNT(*) FROM receipts WHERE status = :status",
            {"status": "closed"},
        )
        count = self.cur.fetchone()[0]
        self.cur.execute(
            "SELECT SUM(receipt_product.total) FROM receipt_product "
            "JOIN receipts ON receipts.id = receipt_product.receipt_id WHERE "
            "status = :status",
            {"status": "closed"},
        )
        rev = self.cur.fetchone()[0]
        if rev is None:
            revenue = 0
        else:
            revenue = rev
        return Sales(count, float(revenue))
