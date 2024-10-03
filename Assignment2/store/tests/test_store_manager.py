from typing import Counter

from store.discount import PrimeDiscount
from store.item_repository import InMemoryItemRepository
from store.report_repository import InMemoCountRepo, InMemoRevenueRepo
from store.store_manager import StoreManager

# def test_set_count_list() -> None:
#     items_rep = InMemoryItemRepository()
#     count = InMemoCountRepo()
#     revenue = InMemoRevenueRepo()
#     count_list = InMemoCountRepo()
#     revenue_list = InMemoRevenueRepo()
#     discounts = [PrimeDiscount()]
#     store_manager = StoreManager(
#         discounts, items_rep, count, revenue, count_list, revenue_list
#     )
#
#     list = InMemoCountRepo(dict["bread":[10]])
#     store_manager.set_count_list(list)
#     assert store_manager.get_count_list() == list


# def test_set_revenue_list() -> None:
#     items_rep = InMemoryItemRepository()
#     count = InMemoCountRepo()
#     revenue = InMemoRevenueRepo()
#     count_list = InMemoCountRepo()
#     revenue_list = InMemoRevenueRepo()
#     discounts = [PrimeDiscount()]
#     store_manager = StoreManager(
#         discounts, items_rep, count, revenue, count_list, revenue_list
#     )
#
#     list = InMemoRevenueRepo(Counter["Cash":10])
#     store_manager.set_revenue_list(list)
#     assert store_manager.get_revenue_list() == list


def test_get_discount() -> None:
    items_rep = InMemoryItemRepository()
    count = InMemoCountRepo()
    revenue = InMemoRevenueRepo()
    count_list = InMemoCountRepo()
    revenue_list = InMemoRevenueRepo()
    discounts = [PrimeDiscount()]
    store_manager = StoreManager(
        discounts, items_rep, count, revenue, count_list, revenue_list
    )

    assert store_manager.get_discounts() == discounts
