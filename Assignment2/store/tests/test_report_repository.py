from store.report_repository import InMemoCountRepo, InMemoRevenueRepo


def test_count_repository_should_persist() -> None:
    repository = InMemoCountRepo()

    repository.add("Milk", 1)

    assert repository.read("Milk") == ("Milk", 1)


def test_count_repository_add_twice() -> None:
    repository = InMemoCountRepo()

    repository.add("Milk", 1)
    repository.add("Milk", 1)

    assert repository.read("Milk") == ("Milk", 2)


def test_count_repository_should_delete() -> None:
    repository = InMemoCountRepo()

    repository.add("Milk", 1)
    repository.add("Milk", 1)
    repository.delete("Milk", 1)

    assert repository.read("Milk") == ("Milk", 1)


def test_count_repository_get_all() -> None:
    repository = InMemoCountRepo()

    repository.add("Milk", 1)
    repository.add("Bread", 6)
    repository.add("Diapers", 2)

    assert repository.get_all() == [("Milk", 1), ("Bread", 6), ("Diapers", 2)]


def test_revenue_repository_should_persist() -> None:
    repository = InMemoRevenueRepo()

    repository.add("Cash", 10.00)

    assert repository.read("Cash") == ("Cash", 10.00)


def test_revenue_repository_should_not_duplicate() -> None:
    repository = InMemoRevenueRepo()

    repository.add("Cash", 10.00)
    repository.add("Card", 5.00)
    repository.add("Cash", 7.50)

    assert repository.read("Cash") == ("Cash", 17.50)


def test_revenue_repository_should_delete() -> None:
    repository = InMemoRevenueRepo()

    repository.add("Cash", 10.00)
    repository.add("Card", 5.00)
    repository.add("Cash", 7.50)
    repository.delete("Cash", 7.50)

    assert repository.read("Cash") == ("Cash", 10.00)


def test_revenue_repository_get_all() -> None:
    repository = InMemoRevenueRepo()

    repository.add("Cash", 10.00)
    repository.add("Card", 5.00)
    repository.add("Cash", 7.50)

    assert repository.get_all() == [("Cash", 17.5), ("Card", 5.00)]
