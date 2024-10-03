import pytest

from store.item import SingleItem, StoreItem
from store.item_repository import (
    InMemoryItemRepository,
    ItemDoesNotExistError,
    ItemExistsError,
)


def test_should_not_read_unknown() -> None:
    repository = InMemoryItemRepository()

    with pytest.raises(ItemDoesNotExistError):
        repository.read(1)


def test_should_persist() -> None:
    item = SingleItem(1, "bread", 1, 0, 1)
    repository = InMemoryItemRepository()

    repository.create(item)

    assert repository.read(item.get_id()) == item


def test_should_not_duplicate() -> None:
    item = SingleItem(1, "bread", 1, 0, 1)
    repository = InMemoryItemRepository()

    repository.create(item)

    with pytest.raises(ItemExistsError):
        repository.create(item)


def test_should_not_update_unknown() -> None:
    item = SingleItem(1, "bread", 1, 0, 1)
    repository = InMemoryItemRepository()

    with pytest.raises(ItemDoesNotExistError):
        repository.update(item)


def test_should_persist_update() -> None:
    item = SingleItem(1, "bread", 1, 0, 1)
    repository = InMemoryItemRepository()

    repository.create(item)
    item.change_price(2)

    repository.update(item)

    assert repository.read(item.get_id()) == item


def test_should_persist_update_bundle_item() -> None:
    item = StoreItem(2, "beer 6 pack", 3, 0, 6)
    repository = InMemoryItemRepository()

    repository.create(item)
    item.change_price(2)

    repository.update(item)

    assert repository.read(item.get_id()) == item


def test_should_not_delete_unknown() -> None:
    repository = InMemoryItemRepository()

    with pytest.raises(ItemDoesNotExistError):
        repository.delete(2)


def test_should_delete() -> None:
    item = SingleItem(1, "bread", 1, 0, 1)
    repository = InMemoryItemRepository()

    repository.create(item)

    repository.delete(item.get_id())

    with pytest.raises(ItemDoesNotExistError):
        repository.read(item.get_id())


def test_get_all() -> None:
    repository = InMemoryItemRepository()
    repository.create(SingleItem(1, "bread", 1, 0, 1))
    repository.create(StoreItem(2, "beer 6 pack", 3, 0, 6))

    assert repository.get_all() == [
        SingleItem(1, "bread", 1, 0, 1),
        StoreItem(2, "beer 6 pack", 3, 0, 6),
    ]
