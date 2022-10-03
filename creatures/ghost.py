from creatures.chase_behaviour import ChaseBehaviour
from creatures.scared_behaviour import ScaredBehaviour
from environment.environment import ACTION_MOVE, Environment
from environment.metrics import ActionMoves


class Ghost:
    @property
    def position(self) -> tuple[int, int]:
        return self.__position

    @property
    def is_scared(self) -> bool:
        return self.__is_scared

    def __init__(
        self, 
        env: Environment,
        initial_position: tuple[int, int],
        chase_behaviour: ChaseBehaviour,
        scared_behaviour: ScaredBehaviour,
        is_scared: bool = False
    ):
        self.__env = env
        self.__position = initial_position
        self.__chase_behaviour = chase_behaviour
        self.__scared_behaviour = scared_behaviour
        self.__is_scared = is_scared

    def step(self) -> None:
        optimum_action = self._best_action()
        self.__position = self._apply_action(optimum_action)

        # TODO handle collision with Pacman
        pass

    def _best_action(self) -> tuple[int, int]:
        available_actions = [
            ACTION_MOVE[ActionMoves.N],
            ACTION_MOVE[ActionMoves.W],
            ACTION_MOVE[ActionMoves.E],
            ACTION_MOVE[ActionMoves.S],
        ]

        legal_actions: tuple[int, int] = list(filter(
            lambda action: (not self.__env.is_wall(self._apply_action(action))),
            available_actions
        ))
        if (self.__is_scared):
            return self.__scared_behaviour.calculate_best_move(
                self.__env.pacman,
                self.__position,
                legal_actions
            )

        return self.__chase_behaviour.calculate_best_move(
            self.__env.pacman,
            self.__position,
            legal_actions
        )

    def _apply_action(self, action: tuple[int, int]) -> tuple[int, int]:
        return [self.__position[0] + action[0], self.__position[1] + action[1]]