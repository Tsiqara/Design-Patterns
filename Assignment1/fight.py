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
from Assignment1.creature import Predator, Prey


@dataclass
class Fight:
    prey: Prey = field(default_factory=Prey)
    predator: Predator = field(default_factory=Predator)

    def fight(self) -> str:
        while True:
            if not self.predator.has_health():
                print(constants.PREY_WIN_MESSAGE)
                return constants.PREY_WIN_MESSAGE
            self.predator.attack(self.prey)

            if not self.prey.has_health():
                print(constants.PREDATOR_WIN_MESSAGE)
                return constants.PREDATOR_WIN_MESSAGE
            self.prey.attack(self.predator)


def test_fight_predator_win():
    h = Health(50)
    s = Stamina(20)
    prey = Prey(Position(5), s, Legs(1), Wings(1), Claws(1), Teeth(1), h, 7)
    h = Health(40)
    predator = Predator(
        Position(5), Stamina(30), Legs(1), Wings(2), Claws(2), Teeth(1), h, 7
    )
    assert Fight(prey, predator).fight() == constants.PREDATOR_WIN_MESSAGE


def test_fight_prey_win():
    h = Health(50)
    s = Stamina(20)
    prey = Prey(Position(5), s, Legs(1), Wings(1), Claws(1), Teeth(1), h, 7)
    h = Health(20)
    predator = Predator(
        Position(5), Stamina(30), Legs(1), Wings(2), Claws(2), Teeth(1), h, 7
    )
    assert Fight(prey, predator).fight() == constants.PREY_WIN_MESSAGE
