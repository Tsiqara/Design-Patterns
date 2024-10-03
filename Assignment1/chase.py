from dataclasses import dataclass, field

from Assignment1 import constants
from Assignment1.characteristics import Legs, Position, Stamina, Wings
from Assignment1.creature import Predator, Prey
from Assignment1.fight import Fight
from Assignment1.move import GreedyMove, MoveInterface, NoMove
from Assignment1.movement_info import MovementInfo


@dataclass
class Chase:
    predator: Predator = field(default_factory=Predator)
    prey: Prey = field(default_factory=Prey)
    predator_move: MoveInterface = field(default_factory=NoMove)
    prey_move: MoveInterface = field(default_factory=NoMove)

    def chase(self) -> None:
        while 1:
            if self.predator.has_stamina():
                self.predator_move.move()
                self.prey_move.move()
                if self.predator_caught_prey():
                    Fight(self.prey, self.predator).fight()
                    break
            else:
                print("Pray ran into infinity")
                return

    def predator_caught_prey(self) -> bool:
        return self.predator.get_position() >= self.prey.get_position()


def test_chase_predator_caught_prey():
    predator = Predator(Position(0), Stamina(25), Legs(2), Wings(2))
    prey = Prey(Position(5), Stamina(15), Legs(1), Wings(0))
    predator_move = GreedyMove(
        MovementInfo(constants.MOVE_INFO), predator, constants.MOVEMENT_ORDER
    )
    prey_move = GreedyMove(
        MovementInfo(constants.MOVE_INFO), prey, constants.MOVEMENT_ORDER
    )
    Chase(
        predator,
        prey,
        predator_move,
        prey_move,
    ).chase()


def test_chase_prey_ran_into_infinity():
    predator = Predator(Position(0), Stamina(15), Legs(1), Wings(1))
    prey = Prey(Position(3), Stamina(25), Legs(1), Wings(2))
    predator_move = GreedyMove(
        MovementInfo(constants.MOVE_INFO), predator, constants.MOVEMENT_ORDER
    )
    prey_move = GreedyMove(
        MovementInfo(constants.MOVE_INFO), prey, constants.MOVEMENT_ORDER
    )
    chase = Chase(
        predator,
        prey,
        predator_move,
        prey_move,
    )
    chase.chase()

    assert not predator.has_stamina() and not chase.predator_caught_prey()
