from store.cashier import Cashier
from store.customer import CustomerBuilder
from store.item import StoreItem
from store.receipt import StoreReceipt


def test_get_receipts() -> None:
    customer = CustomerBuilder().build()
    receipt = StoreReceipt()
    cashier = Cashier(customer, receipt, [receipt])
    assert cashier.get_receipts() == [receipt]


def test_add_item() -> None:
    customer = CustomerBuilder().build()
    receipt = StoreReceipt()
    cashier = Cashier(customer, receipt, [])
    item = StoreItem(2, "beer", 3, 0, 6)
    cashier.add_item(item)
    assert cashier.get_cur_receipt() == StoreReceipt([item])


def test_calculate_cost() -> None:
    customer = CustomerBuilder().build()
    item = StoreItem(2, "beer", 3, 0, 6)
    receipt = StoreReceipt([item])
    cashier = Cashier(customer, receipt, [])
    assert cashier.calculate_cost() == 18


def test_set_customer() -> None:
    customer = CustomerBuilder().with_id(1).build()
    receipt = StoreReceipt()
    cashier = Cashier(customer, receipt, [])
    customer2 = CustomerBuilder().with_id(2).build()
    cashier.set_customer(customer2)

    assert cashier.get_customer() == customer2
