from sys import platlibdir
from core_game.chase_behaviour import ChaseBehaviour
from core_game.pakman import Pakman
from core_game.position import Position
from core_game.scared_behaviour import ScaredBehaviour
from core_game.actions import Action


# Inky = Ghost(env, env.ghosts[INKY])
class Ghost:
    @property
    def position(self) -> Position:
        return self.__position

    @property
    def is_scared(self) -> bool:
        return self.__is_scared

    def __init__(
        self, 
        initial_position: Position,
        chase_behaviour: ChaseBehaviour,
        scared_behaviour: ScaredBehaviour,
        is_scared: bool = False
    ):
        self.__position = initial_position
        self.__chase_behaviour = chase_behaviour
        self.__scared_behaviour = scared_behaviour
        self.__is_scared = is_scared

    def step(self, walls: list[Position], pakman: Pakman) -> tuple[Action, float]:
        optimum_action = self._best_action(walls, pakman.position)
        self.__position = self._position.apply_action(optimum_action)

        if self.__position == pakman.position:
            pakman.die()

        return (optimum_action, -1.0)

    def _best_action(self, walls: list[Position], pakman_position: Position) -> Action:
        legal_actions = list(filter(
            lambda action: not self._position.apply_action(action) in walls,
            Action.as_list()
        ))

        if (self.__is_scared):
            return self.__scared_behaviour.calculate_best_move(
                pakman_position,
                self.__position,
                legal_actions
            )

        return self.__chase_behaviour.calculate_best_move(
            pakman_position,
            self.__position,
            legal_actions
        )