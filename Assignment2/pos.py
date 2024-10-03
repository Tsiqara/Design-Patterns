import sqlite3

import typer

from store.cashier import Cashier
from store.customer import CustomerBuilder, RandomItemsGenerator
from store.discount import PrimeDiscount
from store.item import StoreItemBuilder
from store.item_repository import SQLItemRepository
from store.logger import (
    CountConsoleLogger,
    ItemsConsoleLogger,
    RealConsole,
    RevenueConsoleLogger,
)
from store.payment import RandomGeneratorFromList
from store.receipt import StoreReceipt
from store.report_repository import (
    CountRepository,
    InMemoCountRepo,
    InMemoRevenueRepo,
    RevenueRepository,
    SQLCountRepository,
    SQLRevenueRepository,
)
from store.store_manager import StoreManager

app = typer.Typer()


@app.command()
def list():
    ItemsConsoleLogger().log(items_rep.get_all())
    for discount in store_manager.get_discounts():
        print(discount.get_text())


@app.command()
def simulate():
    customer_number = 0
    add_item()
    global count_list, revenue_list
    for _ in range(3):
        count_list, revenue_list = shift(customer_number)


def shift(customer_number) -> tuple[CountRepository, RevenueRepository]:
    cashier = Cashier(
        discounts=discounts,
        count_list=count_list,
        revenue_list=revenue_list,
        customer=CustomerBuilder().build(),
        curr_receipt=StoreReceipt(),
    )
    options = items_rep.get_all()

    while True:
        items = RandomItemsGenerator().choose_items(options)
        customer = (
            CustomerBuilder()
            .with_items(items)
            .and_payment(RandomGeneratorFromList().get_payment_method())
            .build()
        )
        cashier.set_customer(customer)
        cashier.open_receipt()
        for item in customer.get_items():
            cashier.add_item(item)
        cashier.print_receipt()
        customer.pay(revenue_list)
        cashier.close_receipt()
        customer_number += 1

        if customer_number % 20 == 0:
            prompt_for_x_report.print_str()
            if prompt_for_x_report.read_str() == "y":
                store_manager.make_x_report()

        if customer_number % 100 == 0:
            prompt_for_end_shift.print_str()
            if prompt_for_end_shift.read_str() == "y":
                return cashier.make_z_report(store_manager, count, revenue)


@app.command()
def report():
    CountConsoleLogger().log(count.get_all())
    RevenueConsoleLogger().log(revenue.get_all())


def add_item():
    prompt_add_product.print_str()
    if prompt_add_product.read_str() == "y":
        line = prompt_add_product.read_str()
        name, price, discount, quantity = line.split()
        items_rep.create(
            StoreItemBuilder(
                name=name,
                single_price=float(price),
                discount=float(discount),
                quantity=int(quantity),
            ).build()
        )


if __name__ == "__main__":
    con = sqlite3.Connection("store/pos.db")
    cur = con.cursor()
    items_rep = SQLItemRepository(con, cur)
    count = SQLCountRepository(con, cur)
    revenue = SQLRevenueRepository(con, cur)
    count_list = InMemoCountRepo()
    revenue_list = InMemoRevenueRepo()
    discounts = [PrimeDiscount()]
    store_manager = StoreManager(
        discounts, items_rep, count, revenue, count_list, revenue_list
    )
    prompt_for_x_report = RealConsole("Do you want to make X report?")
    prompt_for_end_shift = RealConsole("Do you want to end the shift?")
    prompt_add_product = RealConsole(
        "Do you want to add Product? "
        "If y enter on one line name price discount quantity"
    )
    app()
