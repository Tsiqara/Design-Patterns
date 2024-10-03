from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator, Protocol

from store.item import Item


class ReceiptLogger(Protocol):
    def log_receipt(self, receipt: Receipt) -> None:
        pass


class TestReceiptLogger:
    res: str = "bla"

    def log_receipt(self, receipt: Receipt) -> None:
        self.res = str((receipt.get_all_items()).__next__().get_name())

    def get_result(self) -> str:
        return self.res


@dataclass
class ConsoleReceiptLogger:
    def log_receipt(self, receipt: Receipt) -> None:
        print()
        print("Product        | Units | Price |  Total  |")
        print("---------------|-------|-------|---------|")
        for item in receipt.get_all_items():
            print(
                item.get_name().ljust(14, " "),
                "|",
                str(item.get_quantity()).ljust(5, " "),
                "|",
                str(item.get_price()).ljust(5, " "),
                "| ",
                str(item.get_cost()).ljust(6, " "),
                "|",
            )
        print()


class Receipt(Protocol):
    def add_item(self, item: Item) -> None:
        pass

    def calculate_cost(self) -> float:
        pass

    def close(self) -> None:
        pass

    def see_receipt(self) -> None:
        pass

    def get_all_items(self) -> Iterator[Item]:
        pass


@dataclass
class StoreReceipt:
    items: list[Item] = field(default_factory=list)
    logger: ReceiptLogger = field(default_factory=ConsoleReceiptLogger)
    open: bool = True
    paid: bool = False

    def add_item(self, item: Item) -> None:
        if not self.open:
            raise ReceiptClosed

        self.items.append(item)

    def calculate_cost(self) -> float:
        return sum(item.get_cost() for item in self.items)

    def close(self) -> None:
        self.open = False

    def see_receipt(self) -> None:
        self.logger.log_receipt(self)

    def get_all_items(self) -> Iterator[Item]:
        return iter(self.items)

    def is_paid(self) -> bool:
        return self.paid


class ReceiptClosed(Exception):
    def __init__(self):
        print("Receipt is closed")
