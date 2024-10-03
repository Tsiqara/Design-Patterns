from dataclasses import dataclass
from typing import Protocol

from store.item import Item


class Logger(Protocol):
    def log(self, info: list) -> None:
        pass


class CountConsoleLogger:
    def log(self, info: list[tuple[str, int]]) -> None:
        print()
        print("Product        | Sales |")
        print("---------------|-------|")
        for product, sales in info:
            print(product.ljust(14, " "), "|", str(sales).ljust(5, " "), "|")
        print()


class RevenueConsoleLogger:
    def log(self, info: list[tuple[str, float]]) -> None:
        print()
        print("Payment   | Revenue |")
        print("----------|---------|")
        for payment, rev in info:
            print(payment.ljust(9, " "), "|", str(rev).ljust(8, " "), "|")
        print()


class ItemsConsoleLogger:
    def log(self, info: list[Item]):
        print()
        print("Product        | Units | Price | Discount | Final Cost |")
        print("---------------|-------|-------|----------|------------|")
        for item in info:
            print(
                item.get_name().ljust(14, " "),
                "|",
                str(item.get_quantity()).ljust(5, " "),
                "|",
                str(item.get_price()).ljust(5, " "),
                "| ",
                str(item.get_discount()).ljust(7, " "),
                "|",
                str(item.get_cost()).ljust(10, " "),
                "|",
            )
        print()


class Console(Protocol):
    def read_str(self) -> str:
        pass

    def print_str(self, value: int) -> None:
        pass


@dataclass
class RealConsole:
    message: str

    def read_str(self) -> str:
        return input()

    def print_str(self) -> None:
        print(self.message)
