import random
from dataclasses import dataclass, field
from typing import Protocol, Self

from store.constansts import CUSTOMER_ID_SEQUENCE, MAX_ITEMS, MIN_ITEMS
from store.item import Item
from store.payment import RandomGeneratorFromList
from store.receipt import Receipt, StoreReceipt


class ItemsGenerator(Protocol):
    def choose_items(self, options: list[Item]) -> list[Item]:
        pass


@dataclass
class RandomItemsGenerator:
    def choose_items(self, options: list[Item]) -> list[Item]:
        return random.choices(options, k=random.randint(MIN_ITEMS, MAX_ITEMS))


class PaymentLogger(Protocol):
    def log_payment(self) -> None:
        pass


@dataclass
class TestPaymentLogger:
    def log_payment(self) -> str:
        return "logged payment"


@dataclass
class ConsolePaymentLogger:
    payment: str = ""

    def log_payment(self) -> None:
        print("Customer paid with", self.payment)


class CustomerProtocol(Protocol):
    def get_id(self) -> int:
        pass

    def get_items(self) -> list[Item]:
        pass

    def get_my_receipt(self) -> Receipt:
        pass

    def see_my_receipt(self) -> None:
        pass

    def pay(self, revenue_list) -> None:
        pass


@dataclass
class Customer:
    id: int
    payment: str
    items: list[Item]
    logger: PaymentLogger

    def get_id(self) -> int:
        return self.id

    def get_items(self) -> list[Item]:
        return self.items

    def get_my_receipt(self) -> Receipt:
        return StoreReceipt(self.items)

    def see_my_receipt(self) -> None:
        StoreReceipt(self.items).see_receipt()

    def pay(self, revenue_list) -> None:
        revenue_list.add(self.payment, self.get_my_receipt().calculate_cost())
        self.logger.log_payment()


@dataclass
class CustomerBuilder:
    id: int = CUSTOMER_ID_SEQUENCE.__next__()
    payment: str = RandomGeneratorFromList().get_payment_method()
    items: list[Item] = field(default_factory=list)
    logger: PaymentLogger = field(default_factory=ConsolePaymentLogger)

    def with_id(self, value: int) -> Self:
        self.id = value

        return self

    def and_id(self, value: int) -> Self:
        return self.with_id(value)

    def with_payment(self, value: str) -> Self:
        self.payment = value
        self.logger = ConsolePaymentLogger(self.payment)

        return self

    def and_payment(self, value: str) -> Self:
        return self.with_payment(value)

    def with_items(self, value: list[Item]) -> Self:
        self.items = value

        return self

    def and_items(self, value: list[Item]) -> Self:
        return self.with_items(value)

    def with_logger(self, value: PaymentLogger) -> Self:
        self.logger = value

        return self

    def and_logger(self, value: PaymentLogger) -> Self:
        return self.with_logger(value)

    def build(self) -> Customer:
        if self.logger is None:
            self.logger = ConsolePaymentLogger(self.payment)
        return Customer(self.id, self.payment, self.items, self.logger)
