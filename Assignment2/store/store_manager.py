from dataclasses import dataclass
from typing import Protocol

from store.cashier import Discount
from store.item import Item
from store.item_repository import CrudItemRepository
from store.logger import CountConsoleLogger, RevenueConsoleLogger
from store.report_repository import CountRepository, RevenueRepository


class StoreManagerProtocol(Protocol):
    def get_discounts(self) -> list[Discount]:
        pass

    def make_x_report(self) -> None:
        pass

    def add_product(self, item: Item) -> None:
        pass

    def change_price(self, item: Item) -> None:
        pass

    def change_discount(self, item: Item) -> None:
        pass

    def add_customer_discount(self, discount: Discount) -> None:
        pass


@dataclass
class StoreManager:
    discounts: list[Discount]
    items: CrudItemRepository
    count: CountRepository
    revenue: RevenueRepository
    count_list: CountRepository
    revenue_list: RevenueRepository

    def set_count_list(self, count_list: CountRepository) -> None:
        self.count_list = count_list

    def get_count_list(self) -> CountRepository:
        return self.count_list

    def set_revenue_list(self, revenue_list: RevenueRepository) -> None:
        self.revenue_list = revenue_list

    def get_revenue_list(self) -> RevenueRepository:
        return self.revenue_list

    def get_discounts(self) -> list[Discount]:
        return self.discounts

    def save_report(
        self,
        count_rep: CountRepository,
        revenue_rep: RevenueRepository,
    ):
        for product, unit in self.count_list.get_all():
            count_rep.add(product, unit)
        for payment, revenue in self.revenue_list.get_all():
            revenue_rep.add(payment, revenue)

    def make_x_report(self) -> None:
        CountConsoleLogger().log(self.count_list.get_all())
        RevenueConsoleLogger().log(self.revenue_list.get_all())
        self.save_report(self.count, self.revenue)

    def add_product(self, item: Item) -> None:
        self.items.create(item)

    def change_price(self, item: Item) -> None:
        self.items.update(item)

    def change_discount(self, item: Item) -> None:
        self.items.update(item)

    def add_customer_discount(self, discount: Discount) -> None:
        self.discounts.append(discount)
