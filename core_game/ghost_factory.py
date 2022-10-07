from core_game.chase_behaviour import AggressiveChaseBehaviour, AmbushChaseBehaviour
from core_game.ghost import Ghost
from core_game.position import Position
from core_game.scared_behaviour import DefaultScaredBehaviour


class GhostFactory:
    @staticmethod
    def spawn_blinky(initial_position: Position) -> Ghost:
        return Ghost(initial_position, DefaultScaredBehaviour(), AggressiveChaseBehaviour())

    @staticmethod
    def spawn_inky(initial_position: Position) -> Ghost:
        return Ghost(initial_position, DefaultScaredBehaviour(), AmbushChaseBehaviour())

    @staticmethod
    def spawn_pinky(initial_position: Position) -> Ghost:
        return Ghost(initial_position, DefaultScaredBehaviour(), AggressiveChaseBehaviour())

    @staticmethod
    def spawn_clyde(initial_position: Position) -> Ghost:
        return Ghost(initial_position, DefaultScaredBehaviour(), AmbushChaseBehaviour())