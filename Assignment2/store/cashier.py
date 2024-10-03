from dataclasses import dataclass, field
from typing import Protocol

from store.customer import CustomerProtocol
from store.discount import Discount
from store.item import Item
from store.receipt import Receipt, StoreReceipt
from store.report_repository import (
    CountRepository,
    InMemoCountRepo,
    InMemoRevenueRepo,
    RevenueRepository,
)
from store.store_manager import StoreManager


class CashierProtocol(Protocol):
    def get_receipts(self) -> list[Receipt]:
        pass

    def open_receipt(self) -> None:
        pass

    def add_item(self, item: Item) -> None:
        pass

    def calculate_cost(self) -> float:
        pass

    def _save_sold_items(self) -> None:
        pass

    def close_receipt(self) -> None:
        pass

    def print_receipt(self) -> None:
        pass

    def make_z_report(
        self,
        manager: StoreManager,
        count_rep: CountRepository,
        revenue_rep: RevenueRepository,
    ) -> tuple[CountRepository, RevenueRepository]:
        pass

    def save_report(
        self,
        count_rep: CountRepository,
        revenue_rep: RevenueRepository,
    ):
        pass


@dataclass
class Cashier:
    customer: CustomerProtocol
    curr_receipt: Receipt
    closed_receipts: list[Receipt] = field(default_factory=list)
    discounts: list[Discount] = field(default_factory=list)
    count_list: CountRepository = field(default_factory=InMemoCountRepo)
    revenue_list: RevenueRepository = field(default_factory=InMemoRevenueRepo)

    def get_receipts(self) -> list[Receipt]:
        return self.closed_receipts

    def get_cur_receipt(self) -> Receipt:
        return self.curr_receipt

    def open_receipt(self) -> None:
        self.curr_receipt = StoreReceipt()

    def add_item(self, item: Item) -> None:
        self.curr_receipt.add_item(item)

    def calculate_cost(self) -> float:
        cost = self.curr_receipt.calculate_cost()
        for discount in self.discounts:
            cost *= 1 - discount.get_discount(self.customer)
        return cost

    def _save_sold_items(self) -> None:
        for item in self.curr_receipt.get_all_items():
            self.count_list.add(item.get_name(), item.get_quantity())

    def close_receipt(self) -> None:
        self._save_sold_items()
        self.curr_receipt.close()
        self.closed_receipts.append(self.curr_receipt)

    def print_receipt(self) -> None:
        self.curr_receipt.see_receipt()

    def make_z_report(
        self,
        manager: StoreManager,
        count_rep: CountRepository,
        revenue_rep: RevenueRepository,
    ) -> tuple[CountRepository, RevenueRepository]:
        self.save_report(count_rep, revenue_rep)

        self.count_list = InMemoCountRepo()
        self.revenue_list = InMemoRevenueRepo()
        manager.set_count_list(self.count_list)
        manager.set_revenue_list(self.revenue_list)
        return self.count_list, self.revenue_list

    def save_report(
        self,
        count_rep: CountRepository,
        revenue_rep: RevenueRepository,
    ):
        for product, unit in self.count_list.get_all():
            count_rep.add(product, unit)
        for payment, revenue in self.revenue_list.get_all():
            revenue_rep.add(payment, revenue)

    def print_discounts(self) -> None:
        for discount in self.discounts:
            print(discount.get_text())

    def set_customer(self, customer):
        self.customer = customer

    def get_customer(self) -> CustomerProtocol:
        return self.customer
