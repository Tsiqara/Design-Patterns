import random
from dataclasses import dataclass, field
from typing import Iterator, Protocol

from store.constansts import PAYMENT


class PaymentGenerator(Protocol):
    def get_payment_method(self) -> str:
        pass


@dataclass
class RandomGeneratorFromList:
    options: list[str] = field(default_factory=lambda: PAYMENT)

    def get_payment_method(self) -> str:
        return random.choice(self.options)


@dataclass
class GeneratorFromSequence:
    sequence: Iterator[str]

    def get_payment_method(self) -> str:
        return self.sequence.__next__()
