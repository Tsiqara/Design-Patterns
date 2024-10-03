from store.item import SingleItemBuilder, StoreItemBuilder


def test_single_item_price() -> None:
    item = SingleItemBuilder().with_price(1).build()
    assert item.get_price() == 1


def test_single_item_name() -> None:
    assert SingleItemBuilder().with_name("bread").build().get_name() == "bread"


def test_single_item_cost_with_discount() -> None:
    item = SingleItemBuilder().with_price(5).and_discount(0.2).build()
    assert item.get_cost() == 4


def test_single_item_quantity() -> None:
    assert SingleItemBuilder().build().get_quantity() == 1


def test_single_item_change_price() -> None:
    item = SingleItemBuilder().with_price(5).build()
    item.change_price(4)
    assert item.get_price() == 4


def test_single_item_change_discount() -> None:
    item = SingleItemBuilder().with_discount(0.2).build()
    item.change_discount(0.25)
    assert item.get_discount() == 0.25


def test_single_item_change_name() -> None:
    item = SingleItemBuilder().with_name("Smo").build()
    item.change_name("Sno")
    assert item.get_name() == "Sno"


def test_single_item_discount() -> None:
    assert SingleItemBuilder().with_discount(0.3).build().get_discount() == 0.3


def test_store_item_name() -> None:
    assert StoreItemBuilder().with_name("beers").build().get_name() == "beers"


def test_store_item_cost() -> None:
    item = StoreItemBuilder().with_price(3).and_quantity(6).build()
    assert item.get_cost() == 18


def test_store_item_price() -> None:
    item = StoreItemBuilder().with_price(3).and_quantity(6).build()
    assert item.get_price() == 3


def test_store_item_discount() -> None:
    assert StoreItemBuilder().with_discount(0.5).build().get_discount() == 0.5


def test_store_item_price_with_discount() -> None:
    assert (
        StoreItemBuilder()
        .with_price(3)
        .and_discount(0.1)
        .and_quantity(6)
        .build()
        .get_cost()
        == 16.2
    )


def test_store_item_get_quantity() -> None:
    assert StoreItemBuilder().with_quantity(4).build().get_quantity() == 4


def test_store_item_change_name() -> None:
    item = StoreItemBuilder().with_name("beer 6 pack").build()
    item.change_name("Beer")
    assert item.get_name() == "Beer"


def test_store_item_change_price() -> None:
    item = StoreItemBuilder().with_price(2).with_quantity(2).build()
    item.change_price(1.5)
    assert item.get_price() == 1.5


def test_store_item_change_discount() -> None:
    item = StoreItemBuilder().with_discount(0.2).build()
    item.change_discount(0.5)
    assert item.get_discount() == 0.5


# def test_combine_items_name() -> None:
#     names = CombineItems(
#         [
#             SingleItem(1, "bread", 1, 0, 1),
#             StoreItem(2, "beer 6 pack", 3, 0, 6),
#             StoreItem(3, "water 6 pack", 0.8, 0.1, 6),
#         ]
#     ).get_name()
#     assert (
#         names.__next__() == "bread"
#         and names.__next__() == "beer 6 pack"
#         and names.__next__() == "water 6 pack"
#     )


# def test_combine_items_price() -> None:
#     assert (
#         CombineItems(
#             [
#                 SingleItemBuilder(name="bread", price=1, discount=0).build(),
#                 StoreItem(2, "beer 6 pack", 3, 0, 6),
#                 StoreItem(3, "water 6 pack", 0.8, 0.1, 6),
#             ]
#         ).get_cost()
#         == 23.32
#     )


# def test_combine_items_get_all() -> None:
#     items = CombineItems(
#         [
#             SingleItem(1, "bread", 1, 0, 1),
#             StoreItem(2, "beer 6 pack", 3, 0, 6),
#             StoreItem(3, "water 6 pack", 0.8, 0.1, 6),
#         ]
#     ).get_all()
#     assert [items.__next__(), items.__next__(), items.__next__()] == [
#         SingleItem(1, "bread", 1, 0, 1),
#         StoreItem(2, "beer 6 pack", 3, 0, 6),
#         StoreItem(3, "water 6 pack", 0.8, 0.1, 6),
#     ]
#
#
# def test_combine_items_contains() -> None:
#     assert CombineItems(
#         [SingleItem(1, "bread", 1, 0, 1), StoreItem(2, "beer", 3, 0, 6)]
#     ).contains_item(SingleItem(1, "bread", 1, 0, 1))
