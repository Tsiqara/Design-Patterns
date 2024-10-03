from Assignment1 import constants
from Assignment1.chase import Chase
from Assignment1.creature import Predator, Prey
from Assignment1.move import GreedyMove
from Assignment1.movement_info import MovementInfo

if __name__ == "__main__":
    for i in range(0, constants.NUM_SIMULATIONS):
        predator = Predator()
        predator.evolve()

        prey = Prey()
        prey.evolve()

        info = MovementInfo(constants.MOVE_INFO)
        order = constants.MOVEMENT_ORDER
        predator_move = GreedyMove(info, predator, order)
        prey_move = GreedyMove(info, prey, order)

        Chase(predator, prey, predator_move, prey_move).chase()
        print()
