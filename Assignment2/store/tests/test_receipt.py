import pytest

from store.item import StoreItem, StoreItemBuilder
from store.receipt import ReceiptClosed, StoreReceipt, TestReceiptLogger


def test_logger() -> None:
    logger = TestReceiptLogger()
    receipt = StoreReceipt([StoreItemBuilder().with_name("T").build()], logger)
    receipt.see_receipt()
    assert logger.get_result() == "T"


def test_calculate_cost() -> None:
    assert (
        StoreReceipt(
            [
                StoreItem(1, "bread", 1, 0, 1),
                StoreItem(2, "beer 6 pack", 3, 0, 6),
                StoreItem(3, "water 6 pack", 0.8, 0.1, 6),
            ]
        ).calculate_cost()
        == 23.32
    )


def test_get_all_items() -> None:
    items = StoreReceipt(
        [
            StoreItem(1, "bread", 1, 0, 1),
            StoreItem(2, "beer 6 pack", 3, 0, 6),
            StoreItem(3, "water 6 pack", 0.8, 0.1, 6),
        ]
    ).get_all_items()
    assert [items.__next__(), items.__next__(), items.__next__()] == [
        StoreItem(1, "bread", 1, 0, 1),
        StoreItem(2, "beer 6 pack", 3, 0, 6),
        StoreItem(3, "water 6 pack", 0.8, 0.1, 6),
    ]


def test_add_item() -> None:
    receipt = StoreReceipt()
    item = StoreItem(1, "bread", 1, 0, 1)
    receipt.add_item(item)
    assert list(receipt.get_all_items()).__contains__(item)


def test_should_not_add_on_closed() -> None:
    receipt = StoreReceipt()
    receipt.close()
    with pytest.raises(ReceiptClosed):
        receipt.add_item(StoreItem(1, "bread", 1, 0, 1))


def test_is_paid() -> None:
    receipt = StoreReceipt()
    assert receipt.is_paid() is False
