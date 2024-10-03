from dataclasses import dataclass
from typing import Protocol

import sympy

from store.customer import CustomerProtocol


class Discount(Protocol):
    def get_discount(self, customer: CustomerProtocol) -> float:
        pass

    def get_text(self) -> str:
        pass


@dataclass
class PrimeDiscount(Discount):
    text: str = "Customer with prime number gets -17% off the receipt price"
    discount: float = 0.17

    def get_discount(self, customer: CustomerProtocol) -> float:
        if sympy.isprime(customer.get_id()):
            return self.discount
        return 0

    def get_text(self) -> str:
        return self.text
