from dataclasses import dataclass, field
from sqlite3 import Connection, Cursor
from typing import Protocol

from store.item import Item, StoreItem


class CrudItemRepository(Protocol):
    def create(self, item: Item) -> None:
        pass

    def read(self, item_id: int) -> Item:
        pass

    def update(self, item: Item) -> None:
        pass

    def delete(self, item_id: int) -> None:
        pass

    def get_all(self) -> list[Item]:
        pass


class ItemExistsError(Exception):
    def __init__(self):
        print("Item already exists")


class ItemDoesNotExistError(Exception):
    def __init__(self):
        print("Item does not exist")


@dataclass
class InMemoryItemRepository:
    items: dict[int, Item] = field(default_factory=dict)

    def create(self, item: Item) -> None:
        if item.get_id() in self.items:
            raise ItemExistsError

        self.items[item.get_id()] = item

    def read(self, item_id: int) -> Item:
        try:
            return self.items[item_id]
        except KeyError:
            raise ItemDoesNotExistError

    def update(self, item: Item) -> None:
        if item.get_id() not in self.items:
            raise ItemDoesNotExistError

        self.items[item.get_id()] = item

    def delete(self, item_id: int) -> None:
        try:
            del self.items[item_id]
        except KeyError:
            raise ItemDoesNotExistError

    def get_all(self) -> list[Item]:
        return list(self.items.values())


@dataclass
class SQLItemRepository:
    con: Connection
    cur: Cursor

    def create(self, item: Item) -> None:
        self.cur.execute(
            "INSERT INTO items VALUES (?, ?, ?, ?, ?)",
            (
                item.get_id(),
                item.get_name(),
                item.get_price(),
                item.get_discount(),
                item.get_quantity(),
            ),
        )

        self.con.commit()

    def read(self, item_id: int) -> Item:
        self.cur.execute("SELECT * FROM items WHERE ID = :id", {"id": item_id})
        res = list(self.cur.fetchone())
        return StoreItem(res[0], res[1], res[2], res[3], res[4])

    def update(self, item: Item) -> None:
        self.cur.execute(
            "UPDATE items SET ID = ?, Product = ?, Price = ?, Discount = ?, "
            "Unit = ? WHERE ID = ?",
            (
                item.get_id(),
                item.get_name(),
                item.get_price(),
                item.get_discount(),
                item.get_quantity(),
                item.get_id(),
            ),
        )

        self.con.commit()

    def delete(self, item_id: int) -> None:
        self.cur.execute("DELETE FROM items WHERE ID = :id", {"id": item_id})
        self.con.commit()

    def get_all(self) -> list[Item]:
        self.cur.execute("SELECT * FROM items")
        result = self.cur.fetchall()
        return [StoreItem(r[0], r[1], r[2], r[3], r[4]) for r in result]

    def close(self) -> None:
        self.con.close()
