from store.customer import CustomerBuilder
from store.discount import PrimeDiscount


def test_prime_discount_on_prime() -> None:
    customer = CustomerBuilder().with_id(13).build()
    assert PrimeDiscount(discount=0.17).get_discount(customer) == 0.17


def test_prime_discount_on_not_prime() -> None:
    customer = CustomerBuilder().with_id(4).build()
    assert PrimeDiscount(discount=0.17).get_discount(customer) == 0
