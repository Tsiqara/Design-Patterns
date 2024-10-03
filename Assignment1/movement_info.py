from dataclasses import dataclass

from Assignment1 import constants
from Assignment1.characteristics import Legs, Position, Stamina, Wings
from Assignment1.creature import Creature


@dataclass
class MovementInfo:
    move_info: dict[str, tuple[int, int, int, int, int]]

    def get_required_stamina(self, movement: str) -> int:
        return self.move_info[movement][0]

    def get_stamina_use(self, movement: str) -> int:
        return self.move_info[movement][1]

    def get_speed(self, movement: str) -> int:
        return self.move_info[movement][2]

    def get_num_legs_required(self, movement: str) -> int:
        return self.move_info[movement][3]

    def get_num_wing_required(self, movement: str) -> int:
        return self.move_info[movement][4]

    def enough_wings(self, creature: Creature, movement: str) -> bool:
        return creature.get_num_wings() >= self.get_num_wing_required(movement)

    def enough_legs(self, creature: Creature, movement: str) -> bool:
        return creature.get_num_legs() >= self.get_num_legs_required(movement)

    def enough_stamina(self, creature: Creature, movement: str) -> bool:
        return creature.get_stamina() >= self.get_required_stamina(movement)

    def can_do_movement(self, creature: Creature, movement: str) -> bool:
        return (
            self.enough_stamina(creature, movement)
            and self.enough_legs(creature, movement)
            and self.enough_wings(creature, movement)
        )


def test_get_required_stamina():
    assert MovementInfo(constants.MOVE_INFO).get_required_stamina("fly") == 80


def test_get_stamina_use():
    assert MovementInfo(constants.MOVE_INFO).get_stamina_use("walk") == 2


def test_get_speed():
    assert MovementInfo(constants.MOVE_INFO).get_speed("run") == 6


def test_get_num_legs_required():
    info = constants.MOVE_INFO
    assert MovementInfo(info).get_num_legs_required("crawl") == 0


def test_get_num_wings_required():
    assert MovementInfo(constants.MOVE_INFO).get_num_wing_required("fly") == 2


def test_enough_wings():
    c = Creature(Position(0), Stamina(10), Legs(1), Wings(1))
    assert MovementInfo(constants.MOVE_INFO).enough_wings(c, "run") is True


def test_enough_legs():
    c = Creature(Position(10), Stamina(20), Legs(1), Wings(0))
    assert MovementInfo(constants.MOVE_INFO).enough_legs(c, "walk") is False


def test_enough_stamina():
    c = Creature(Position(10), Stamina(20), Legs(1), Wings(0))
    assert MovementInfo(constants.MOVE_INFO).enough_stamina(c, "hop") is True
