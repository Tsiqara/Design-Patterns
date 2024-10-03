from store.payment import GeneratorFromSequence


def test_get_payment_from_sequence() -> None:
    sequence = (p for p in ["Cash", "Cash", "Card", "Other"])
    generator = GeneratorFromSequence(sequence)
    assert (
        generator.get_payment_method() == "Cash"
        and generator.get_payment_method() == "Cash"
        and generator.get_payment_method() == "Card"
        and generator.get_payment_method() == "Other"
    )
