from collections import Counter
from dataclasses import dataclass, field
from sqlite3 import Connection, Cursor
from typing import Protocol


class CountRepository(Protocol):
    def add(self, product: str, sales: int) -> None:
        pass

    def read(self, product: str) -> tuple[str, int]:
        pass

    def delete(self, product: str, num: int) -> None:
        pass

    def get_all(self) -> list[tuple[str, int]]:
        pass


@dataclass
class InMemoCountRepo:
    info: dict[str, list[int]] = field(default_factory=dict)

    def add(self, product: str, sales: int) -> None:
        if not self.info.keys().__contains__(product):
            self.info[product] = []
        self.info[product].append(sales)

    def read(self, product: str) -> tuple[str, int]:
        return product, sum(self.info[product])

    def delete(self, product: str, num: int) -> None:
        self.info[product].remove(num)

    def get_all(self) -> list[tuple[str, int]]:
        res = []
        for product in self.info.keys():
            for num in self.info[product]:
                res.append((product, num))
        return res


@dataclass
class SQLCountRepository:
    con: Connection
    cur: Cursor

    def add(self, product: str, sales: int) -> None:
        self.cur.execute("INSERT INTO count VALUES (?, ?)", (product, sales))
        self.con.commit()

    def read(self, product: str) -> tuple[str, int]:
        return self.cur.execute(
            "SELECT Product, SUM(sales) FROM count WHERE Product = ?", product
        ).fetchone()

    def delete(self, product: str, num: int) -> None:
        self.cur.execute(
            "DELETE FROM count WHERE Product = ? AND Sales = ?", (product, num)
        )
        self.con.commit()

    def get_all(self) -> list[tuple[str, int]]:
        res = self.cur.execute("SELECT * FROM count").fetchall()
        ans = []
        for product, sales in res:
            ans.append((product, sales))
        return res


class RevenueRepository(Protocol):
    def add(self, payment: str, amount: float) -> None:
        pass

    def read(self, payment: str) -> tuple[str, float]:
        pass

    def delete(self, payment: str, amount: float) -> None:
        pass

    def get_all(self) -> list[tuple[str, float]]:
        pass


@dataclass
class InMemoRevenueRepo:
    info: Counter[str] = field(default_factory=Counter)

    def add(self, payment: str, amount: float) -> None:
        self.info[payment] += amount

    def read(self, payment: str) -> tuple[str, float]:
        return payment, self.info[payment]

    def delete(self, payment: str, amount: float) -> None:
        self.info[payment] -= amount

    def get_all(self) -> list[tuple[str, float]]:
        res: list[tuple[str, float]] = []

        for payment in self.info.keys():
            res.append((payment, self.info[payment]))
        return res


@dataclass
class SQLRevenueRepository:
    con: Connection
    cur: Cursor

    def add(self, payment: str, amount: float) -> None:
        values = (payment, amount)
        self.cur.execute("INSERT INTO revenue VALUES (?, ?)", values)
        self.con.commit()

    def read(self, payment: str) -> tuple[str, float]:
        p = payment
        return self.cur.execute(
            "SELECT payment, SUM(revenue) FROM revenue WHERE Payment = ?", p
        ).fetchone()

    def delete(self, payment: str, amount: float) -> None:
        val = (payment, amount)
        row_id = self.cur.execute(
            "SELECT ROWID FROM revenue WHERE Payment = ? AND Revenue = ?", val
        ).fetchone()
        self.cur.execute("DELETE FROM revenue WHERE ROWID = ?", row_id)
        self.con.commit()

    def get_all(self) -> list[tuple[str, float]]:
        res = self.cur.execute(
            "SELECT Payment, SUM(Revenue) FROM revenue GROUP BY Payment"
        )
        return res.fetchall()
