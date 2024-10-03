from __future__ import annotations

from dataclasses import dataclass, field
from random import randint
from typing import Protocol

from Assignment1 import constants
from Assignment1.creature import Creature, Legs, Position, Stamina, Wings
from Assignment1.movement_info import MovementInfo


class MoveInterface(Protocol):
    def move(self, movement: str = "") -> bool | None:
        pass


@dataclass
class Move:
    info: MovementInfo
    creature: Creature = field(default_factory=Creature)

    def move(self, movement: str = "") -> bool:
        if movement in constants.MOVEMENT_ORDER and self.info.can_do_movement(
            self.creature, movement
        ):
            self.creature.use_stamina(self.info.get_stamina_use(movement))
            self.creature.increment_position(self.info.get_speed(movement))
            return True

        return False

    def crawl(self) -> None:
        self.move("crawl")

    def hop(self) -> None:
        self.move("hop")

    def walk(self) -> None:
        self.move("walk")

    def run(self) -> None:
        self.move("run")

    def fly(self) -> None:
        self.move("fly")


class NoMove:
    def move(self, movement: str = "") -> bool | None:
        pass


@dataclass
class GreedyMove(Move):
    greedy_order: list[str] = field(default_factory=list)

    def move(self, movement: str = ""):
        for i in range(0, len(self.greedy_order)):
            movement = self.greedy_order[i]
            if super().move(movement):
                return


@dataclass
class RandomMove(Move):
    random_order: list[str] = field(default_factory=list)

    def move(self, movement: str = ""):
        if not self.creature.has_stamina():
            return

        while True:
            i = randint(0, len(self.random_order) - 1)
            movement = self.random_order[i]
            if super().move(movement):
                return


def test_incorrect_movement():
    creature = Creature(Position(0), Stamina(1), Legs(0), Wings(0))

    Move(MovementInfo(constants.MOVE_INFO), creature).move("a")

    assert creature.get_position() == 0 and creature.get_stamina() == 1


def test_crawl():
    creature = Creature(Position(0), Stamina(1), Legs(0), Wings(0))

    Move(MovementInfo(constants.MOVE_INFO), creature).crawl()

    assert creature.get_position() == 1 and creature.get_stamina() == 0


def test_crawl_with_zero_stamina():
    creature = Creature(Position(2), Stamina(0), Legs(0), Wings(0))

    Move(MovementInfo(constants.MOVE_INFO), creature).crawl()

    assert creature.get_position() == 2 and creature.get_stamina() == 0


def test_hop():
    creature = Creature(Position(0), Stamina(25), Legs(1), Wings(0))

    Move(MovementInfo(constants.MOVE_INFO), creature).hop()

    assert creature.get_position() == 3 and creature.get_stamina() == 23


def test_hop_without_enough_stamina():
    creature = Creature(Position(0), Stamina(10), Legs(1), Wings(0))

    Move(MovementInfo(constants.MOVE_INFO), creature).hop()

    assert creature.get_position() == 0 and creature.get_stamina() == 10


def test_hop_without_enough_legs():
    creature = Creature(Position(0), Stamina(25), Legs(0), Wings(0))

    Move(MovementInfo(constants.MOVE_INFO), creature).hop()

    assert creature.get_position() == 0 and creature.get_stamina() == 25


def test_walk():
    creature = Creature(Position(3), Stamina(40), Legs(3), Wings(0))

    Move(MovementInfo(constants.MOVE_INFO), creature).walk()

    assert creature.get_position() == 7 and creature.get_stamina() == 38


def test_walk_without_enough_stamina():
    creature = Creature(Position(0), Stamina(30), Legs(2), Wings(0))

    Move(MovementInfo(constants.MOVE_INFO), creature).walk()

    assert creature.get_position() == 0 and creature.get_stamina() == 30


def test_walk_without_enough_legs():
    creature = Creature(Position(0), Stamina(50), Legs(1), Wings(0))

    Move(MovementInfo(constants.MOVE_INFO), creature).walk()

    assert creature.get_position() == 0 and creature.get_stamina() == 50


def test_run():
    creature = Creature(Position(5), Stamina(60), Legs(3), Wings(0))

    Move(MovementInfo(constants.MOVE_INFO), creature).run()

    assert creature.get_position() == 11 and creature.get_stamina() == 56


def test_run_without_enough_stamina():
    creature = Creature(Position(0), Stamina(50), Legs(1), Wings(0))

    Move(MovementInfo(constants.MOVE_INFO), creature).run()

    assert creature.get_position() == 0 and creature.get_stamina() == 50


def test_run_without_enough_legs():
    creature = Creature(Position(0), Stamina(65), Legs(1), Wings(0))

    Move(MovementInfo(constants.MOVE_INFO), creature).run()

    assert creature.get_position() == 0 and creature.get_stamina() == 65


def test_fly():
    creature = Creature(Position(2), Stamina(100), Legs(0), Wings(2))

    Move(MovementInfo(constants.MOVE_INFO), creature).fly()

    assert creature.get_position() == 10 and creature.get_stamina() == 96


def test_fly_without_enough_stamina():
    creature = Creature(Position(0), Stamina(70), Legs(5), Wings(2))

    Move(MovementInfo(constants.MOVE_INFO), creature).fly()

    assert creature.get_position() == 0 and creature.get_stamina() == 70


def test_fly_without_enough_wings():
    creature = Creature(Position(0), Stamina(90), Legs(1), Wings(1))

    Move(MovementInfo(constants.MOVE_INFO), creature).fly()

    assert creature.get_position() == 0 and creature.get_stamina() == 90


def test_greedy_move_fly():
    creature = Creature(Position(2), Stamina(100), Legs(0), Wings(2))

    GreedyMove(
        MovementInfo(constants.MOVE_INFO), creature, constants.MOVEMENT_ORDER
    ).move()

    assert creature.get_position() == 10 and creature.get_stamina() == 96


def test_greedy_move_run():
    creature = Creature(Position(5), Stamina(60), Legs(3), Wings(0))

    GreedyMove(
        MovementInfo(constants.MOVE_INFO), creature, constants.MOVEMENT_ORDER
    ).move()

    assert creature.get_position() == 11 and creature.get_stamina() == 56


def test_greedy_move_walk():
    creature = Creature(Position(3), Stamina(40), Legs(3), Wings(0))

    GreedyMove(
        MovementInfo(constants.MOVE_INFO), creature, constants.MOVEMENT_ORDER
    ).move()

    assert creature.get_position() == 7 and creature.get_stamina() == 38


def test_greedy_move_hop():
    creature = Creature(Position(0), Stamina(25), Legs(1), Wings(0))

    GreedyMove(
        MovementInfo(constants.MOVE_INFO), creature, constants.MOVEMENT_ORDER
    ).move()

    assert creature.get_position() == 3 and creature.get_stamina() == 23


def test_greedy_move_crawl():
    creature = Creature(Position(0), Stamina(1), Legs(0), Wings(0))

    GreedyMove(
        MovementInfo(constants.MOVE_INFO), creature, constants.MOVEMENT_ORDER
    ).move()

    assert creature.get_position() == 1 and creature.get_stamina() == 0


def test_greedy_move_does_nothing():
    creature = Creature(Position(0), Stamina(0), Legs(0), Wings(0))

    GreedyMove(
        MovementInfo(constants.MOVE_INFO), creature, constants.MOVEMENT_ORDER
    ).move()

    assert creature.get_position() == 0 and creature.get_stamina() == 0


def test_random_move():
    creature = Creature(Position(5), Stamina(100), Legs(1), Wings(2))

    RandomMove(
        MovementInfo(constants.MOVE_INFO), creature, constants.MOVEMENT_ORDER
    ).move()

    creature.log_characteristics()

    assert creature.get_position() >= 5 and creature.get_stamina() <= 100


def test_random_does_crawl():
    creature = Creature(Position(10), Stamina(15), Legs(1), Wings(2))

    RandomMove(
        MovementInfo(constants.MOVE_INFO), creature, constants.MOVEMENT_ORDER
    ).move()

    creature.log_characteristics()

    assert creature.get_position() == 11 and creature.get_stamina() == 14


def test_random_does_nothing():
    creature = Creature(Position(10), Stamina(0), Legs(1), Wings(2))

    RandomMove(
        MovementInfo(constants.MOVE_INFO), creature, constants.MOVEMENT_ORDER
    ).move()

    assert creature.get_position() == 10 and creature.get_stamina() == 0
