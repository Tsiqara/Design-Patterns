from store.customer import CustomerBuilder, TestPaymentLogger
from store.item import StoreItem
from store.receipt import StoreReceipt


def test_customer_get_id() -> None:
    assert CustomerBuilder().with_id(1).build().get_id() == 1


def test_customer_get_items() -> None:
    items = [StoreItem(2, "beer", 3, 0, 6)]
    customer = CustomerBuilder().with_items(items).build()
    assert customer.get_items() == [
        StoreItem(2, "beer", 3, 0, 6),
    ]


def test_customer_get_receipt() -> None:
    cb = CustomerBuilder().with_items([StoreItem(2, "beer", 3, 0, 6)])
    customer = cb.build()

    receipt = StoreReceipt([StoreItem(2, "beer", 3, 0, 6)])
    assert customer.get_my_receipt() == receipt


def test_payment_logger() -> None:
    assert TestPaymentLogger().log_payment() == "logged payment"
