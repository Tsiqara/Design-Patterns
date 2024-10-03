from __future__ import annotations

from dataclasses import dataclass, field

from Assignment1 import constants
from Assignment1.characteristics import (
    Claws,
    Health,
    Legs,
    Position,
    Stamina,
    Teeth,
    Wings,
)


@dataclass
class Creature:
    position: Position = field(default_factory=Position)
    stamina: Stamina = field(default_factory=Stamina)
    legs: Legs = field(default_factory=Legs)
    wings: Wings = field(default_factory=Wings)
    claws: Claws = field(default_factory=Claws)
    teeth: Teeth = field(default_factory=Teeth)
    health: Health = field(default_factory=Health)
    power: int = constants.DEFAULT_POWER

    def __post_init__(self):
        self.generate_power()

    def get_position(self) -> int:
        return self.position.get_position()

    def get_stamina(self) -> int:
        return self.stamina.get_stamina()

    def get_num_legs(self) -> int:
        return self.legs.get_num_legs()

    def get_num_wings(self) -> int:
        return self.wings.get_num_wings()

    def use_stamina(self, value) -> None:
        self.stamina.decrement_stamina(value)

    def increment_position(self, value) -> None:
        self.position.increment_position(value)

    def log_characteristics(self) -> None:
        self.position.log_position()
        self.stamina.log_stamina()
        self.legs.log_legs()
        self.wings.log_legs()
        self.claws.log_claws()
        self.teeth.log_teeth()
        self.health.log_health()
        print()

    def evolve(self) -> None:
        self.stamina.generate_stamina()
        self.legs.evolve_legs()
        self.wings.evolve_wings()
        self.claws.evolve_claws()
        self.teeth.evolve_teeth()
        self.health.generate_health()
        self.generate_power()

    def has_stamina(self) -> bool:
        return self.get_stamina() > 0

    def get_claws(self) -> int:
        return self.claws.get_claw_level()

    def get_teeth_sharpness(self) -> int:
        return self.teeth.get_sharpness()

    def get_health(self) -> int:
        return self.health.get_health()

    def use_health(self, value: int) -> None:
        self.health.decrement_health(value)

    def get_attack_power(self) -> int:
        return self.power

    def generate_power(self) -> None:
        self.power = (
            self.power * constants.CLAWS_POWER_MULTIPLIER[self.get_claws()]
            + constants.TEETH_POWER_BOOST[self.get_teeth_sharpness()]
        )

    def has_health(self) -> bool:
        return self.get_health() > 0

    def attack(self, prey: Creature):
        prey.use_health(self.get_attack_power())


@dataclass
class Predator(Creature):
    def evolve(self) -> None:
        self.position.set_position(0)
        super().evolve()
        self.log_characteristics()

    def log_characteristics(self) -> None:
        print("Predator:")
        super().log_characteristics()


@dataclass
class Prey(Creature):
    def evolve(self, min_pos=constants.MIN_POS, max_pos=constants.MAX_POS):
        self.position.generate_position(min_pos, max_pos)
        super().evolve()
        self.log_characteristics()

    def log_characteristics(self) -> None:
        print("Prey:")
        super().log_characteristics()


def test_predator_evolves_correct_position():
    predator = Predator()

    predator.evolve()
    predator.log_characteristics()

    assert predator.get_position() == 0


def test_prey_evolves_correct_position():
    prey = Prey()

    prey.evolve(0, 50)
    prey.log_characteristics()

    assert 0 <= prey.get_position() <= 50


def test_prey_evolves_correct_position_from_default_range():
    prey = Prey()

    prey.evolve()

    assert constants.MIN_POS <= prey.get_position() <= constants.MAX_POS


def test_generate_power_after_init():
    h = Health(30)
    creature = Creature(
        Position(5), Stamina(20), Legs(1), Wings(1), Claws(2), Teeth(1), h, 7
    )

    assert creature.get_attack_power() == (7 * 3 + 3)


def test_generate_power():
    creature = Creature()

    assert (
        creature.get_attack_power()
        == constants.DEFAULT_POWER
        * constants.CLAWS_POWER_MULTIPLIER[creature.get_claws()]
        + constants.TEETH_POWER_BOOST[creature.get_teeth_sharpness()]
    )


def test_attack():
    h = Health(30)
    s = Stamina(20)
    prey = Prey(Position(5), s, Legs(1), Wings(1), Claws(1), Teeth(1), h, 7)
    predator = Predator(
        Position(5), Stamina(30), Legs(1), Wings(2), Claws(2), Teeth(1), h, 7
    )

    predator.attack(prey)

    assert prey.get_health() == 6
