from dataclasses import dataclass
from random import randint

from Assignment1 import constants


@dataclass
class Position:
    position: int = constants.DEFAULT_POSITION

    def get_position(self) -> int:
        return self.position

    def generate_position(self, min_pos, max_pos) -> None:
        self.position = randint(min_pos, max_pos)

    def log_position(self) -> None:
        print("Position: " + str(self.position))

    def increment_position(self, value) -> None:
        self.position += value

    def set_position(self, value) -> None:
        self.position = value


def test_get_position():
    assert Position(5).get_position() == 5


def test_generate_position():
    position = Position(25)

    position.generate_position(0, 20)

    assert position.get_position() in range(0, 21)


def test_increment_position():
    position = Position(10)

    position.increment_position(3)

    assert position.get_position() == 13


def test_set_position():
    position = Position()

    position.set_position(3)

    assert position.get_position() == 3


@dataclass
class Stamina:
    stamina: int = constants.DEFAULT_STAMINA

    def get_stamina(self) -> int:
        return self.stamina

    def generate_stamina(self) -> None:
        self.stamina = randint(constants.MIN_STAMINA, constants.MAX_STAMINA)

    def log_stamina(self) -> None:
        print("Stamina: " + str(self.stamina))

    def decrement_stamina(self, value) -> None:
        self.stamina -= value


def test_get_stamina():
    assert Stamina(10).get_stamina() == 10


def test_generate_stamina():
    stamina = Stamina()

    stamina.generate_stamina()

    assert stamina.get_stamina() in range(
        constants.MIN_STAMINA, constants.MAX_STAMINA + 1
    )


def test_decrement_stamina():
    stamina = Stamina(20)

    stamina.decrement_stamina(5)

    assert stamina.get_stamina() == 15


@dataclass
class Legs:
    legs: int = constants.DEFAULT_LEGS

    def get_num_legs(self) -> int:
        return self.legs

    def evolve_legs(self) -> None:
        self.legs = randint(constants.MIN_LEGS, constants.MAX_LEGS)

    def log_legs(self) -> None:
        print("Legs: " + str(self.legs))


def test_get_num_legs():
    assert Legs(2).get_num_legs() == 2


def test_evolve_legs():
    legs = Legs()

    legs.evolve_legs()

    assert constants.MIN_LEGS <= legs.get_num_legs() <= constants.MAX_LEGS


@dataclass
class Wings:
    wings: int = constants.DEFAULT_WINGS

    def get_num_wings(self) -> int:
        return self.wings

    def evolve_wings(self) -> None:
        self.wings = randint(constants.MIN_WINGS, constants.MAX_WINGS)

    def log_legs(self) -> None:
        print("Wings: " + str(self.wings))


def test_get_num_wings():
    assert Wings(4).get_num_wings() == 4


def test_evolve_wings():
    wings = Wings(1)

    wings.evolve_wings()

    assert constants.MIN_WINGS <= wings.get_num_wings() <= constants.MAX_WINGS


@dataclass
class Claws:
    claw_level: int = constants.DEFAULT_CLAW_LEVEL

    def get_claw_level(self) -> int:
        return self.claw_level

    def get_claw_size(self) -> str:
        return constants.CLAWS[self.claw_level]

    def evolve_claws(self) -> None:
        self.claw_level = randint(constants.MIN_CLAW, constants.MAX_CLAW)

    def log_claws(self) -> None:
        print("Claws: " + self.get_claw_size())


def test_get_claw_level():
    assert Claws(2).get_claw_level() == 2


def test_get_claw_size():
    assert Claws(3).get_claw_size() == "big claws"


def test_generate_claws():
    claws = Claws()

    claws.evolve_claws()

    assert constants.MIN_CLAW <= claws.get_claw_level() <= constants.MAX_CLAW


@dataclass
class Teeth:
    sharpness: int = constants.DEFAULT_TEETH_SHARPNESS

    def get_sharpness(self) -> int:
        return self.sharpness

    def evolve_teeth(self) -> None:
        self.sharpness = randint(constants.MIN_TEETH, constants.MAX_TEETH)

    def log_teeth(self) -> None:
        print("Teeth sharpness: " + str(self.get_sharpness()))


def test_get_teeth_sharpness():
    assert Teeth(1).get_sharpness() == 1


def test_generate_teeth_sharpness():
    teeth = Teeth()

    teeth.evolve_teeth()

    assert constants.MIN_TEETH <= teeth.get_sharpness() <= constants.MAX_TEETH


@dataclass
class Health:
    health: int = constants.DEFAULT_HEALTH

    def get_health(self) -> int:
        return self.health

    def generate_health(self) -> None:
        self.health = randint(constants.MIN_HEALTH, constants.MAX_HEALTH)

    def log_health(self) -> None:
        print("Health: " + str(self.health))

    def decrement_health(self, value) -> None:
        self.health -= value


def test_get_health():
    assert Health(60).get_health() == 60


def test_generate_health():
    health = Health()

    health.generate_health()

    assert constants.MIN_HEALTH <= health.get_health() <= constants.MAX_HEALTH


def test_decrement_health():
    health = Health(70)

    health.decrement_health(5)

    assert health.get_health() == 65
