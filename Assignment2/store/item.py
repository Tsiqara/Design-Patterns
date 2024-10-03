from dataclasses import dataclass
from typing import Protocol

from typing_extensions import Self

from store.constansts import ID_SEQUENCE


# decided to have single item and bundle item classes but then realised
# that it can be done with single StoreItem class. But left both classes
# for test purposes and composite pattern
class Item(Protocol):
    def get_id(self) -> int:
        pass

    def get_name(self) -> str:
        pass

    def get_cost(self) -> float:
        pass

    def get_price(self) -> float:
        pass

    def get_quantity(self) -> int:
        pass

    def get_discount(self) -> float:
        pass

    def change_name(self, name: str) -> None:
        pass

    def change_price(self, price: float) -> None:
        pass

    def change_discount(self, discount: float) -> None:
        pass


class ItemBuilder(Protocol):
    def and_id(self, value: int) -> Self:
        pass

    def with_id(self, value: int) -> Self:
        pass

    def and_name(self, value: str) -> Self:
        pass

    def with_name(self, value: str) -> Self:
        pass

    def and_price(self, value: float) -> Self:
        pass

    def with_price(self, value: float) -> Self:
        pass

    def and_discount(self, value: float) -> Self:
        pass

    def with_discount(self, value: float) -> Self:
        pass

    def and_quantity(self, value: int) -> Self:
        pass

    def with_quantity(self, value: int) -> Self:
        pass

    def build(self) -> Item:
        pass


@dataclass
class StoreItem:
    id: int
    name: str
    single_price: float
    discount: float
    quantity: int

    def get_id(self) -> int:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> float:
        return self.single_price

    def get_cost(self) -> float:
        return (self.single_price * self.quantity) * (1 - self.discount)

    def get_quantity(self) -> int:
        return self.quantity

    def get_discount(self) -> float:
        return self.discount

    def change_name(self, name: str) -> None:
        self.name = name

    def change_price(self, price: float) -> None:
        self.single_price = price

    def change_discount(self, discount: float) -> None:
        self.discount = discount


@dataclass
class StoreItemBuilder:
    id: int = ID_SEQUENCE.__next__()
    name: str = ""
    single_price: float = 0
    discount: float = 0
    quantity: int = 1

    def and_id(self, value: int) -> Self:
        return self.with_id(value)

    def with_id(self, value: int) -> Self:
        self.id = value

        return self

    def and_name(self, value: str) -> Self:
        return self.with_name(value)

    def with_name(self, value: str) -> Self:
        self.name = value

        return self

    def and_price(self, value: float) -> Self:
        return self.with_price(value)

    def with_price(self, value: float) -> Self:
        self.single_price = value

        return self

    def and_discount(self, value: float) -> Self:
        return self.with_discount(value)

    def with_discount(self, value: float) -> Self:
        self.discount = value

        return self

    def and_quantity(self, value: int) -> Self:
        return self.with_quantity(value)

    def with_quantity(self, value: int) -> Self:
        self.quantity = value

        return self

    def build(self) -> StoreItem:
        return StoreItem(
            id=self.id,
            name=self.name,
            single_price=self.single_price,
            discount=self.discount,
            quantity=self.quantity,
        )


@dataclass
class SingleItem:
    id: int
    name: str
    price: float
    discount: float
    quantity: int

    def get_id(self) -> int:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> float:
        return self.price

    def get_cost(self) -> float:
        return self.price * (1 - self.discount)

    def get_quantity(self) -> int:
        return self.quantity

    def get_discount(self) -> float:
        return self.discount

    def change_name(self, name: str) -> None:
        self.name = name

    def change_price(self, price: float) -> None:
        self.price = price

    def change_discount(self, discount: float) -> None:
        self.discount = discount


@dataclass
class SingleItemBuilder:
    id: int = ID_SEQUENCE.__next__()
    name: str = ""
    price: float = 0
    discount: float = 0
    quantity: int = 1

    def and_id(self, value: int) -> Self:
        return self.with_id(value)

    def with_id(self, value: int) -> Self:
        self.id = value

        return self

    def and_name(self, value: str) -> Self:
        return self.with_name(value)

    def with_name(self, value: str) -> Self:
        self.name = value

        return self

    def and_price(self, value: float) -> Self:
        return self.with_price(value)

    def with_price(self, value: float) -> Self:
        self.price = value

        return self

    def and_discount(self, value: float) -> Self:
        return self.with_discount(value)

    def with_discount(self, value: float) -> Self:
        self.discount = value

        return self

    def build(self) -> SingleItem:
        return SingleItem(
            id=self.id,
            name=self.name,
            price=self.price,
            discount=self.discount,
            quantity=self.quantity,
        )


# @dataclass
# class CombineItems:
#     items: list[Item]
#
#     def get_ids(self) -> list[Callable[[], int]]:
#         return list(i.get_id for i in self.items)
#
#     def get_name(self) -> Generator[str, Any, None]:
#         return (i.get_name() for i in self.items)
#
#     def get_cost(self) -> float:
#         return sum(item.get_cost() for item in self.items)
#
#     def add_item(self, item: Item) -> None:
#         self.items.append(item)
#
#     def get_all(self) -> Iterator[Item]:
#         return iter(self.items)
#
#     def contains_item(self, item: Item) -> bool:
#         return self.items.__contains__(item)
