from core_game.core_agent import CoreAgent
from creatures.chase_behaviour import ChaseBehaviour
from core_game.position import Position
from creatures.scared_behaviour import ScaredBehaviour
from core_game.actions import Action
from environment.environment import Environment

# Inky = Ghost(env, env.ghosts[INKY])
class Ghost(CoreAgent):
    @property
    def is_scared(self) -> bool:
        return self.__is_scared

    def __init__(
        self, 
        env: Environment,
        initial_position: Position,
        chase_behaviour: ChaseBehaviour,
        scared_behaviour: ScaredBehaviour,
        is_scared: bool = False
    ):
        super().__init__(initial_position)
        self.__env = env
        self.__chase_behaviour = chase_behaviour
        self.__scared_behaviour = scared_behaviour
        self.__is_scared = is_scared

    def step(self) -> tuple[Action, float]:
        optimum_action = self._best_action()
        self._position = self._position.apply_action(optimum_action)
        return (optimum_action, -1.0)

    def _best_action(self) -> Action:
        legal_actions = list(filter(
            lambda action: (not self.__env.is_wall(self._position.apply_action(action))),
            Action.as_list()
        ))

        if (self.__is_scared):
            return self.__scared_behaviour.calculate_best_move(
                self.__env.pakman_position,
                self._position,
                legal_actions
            )

        return self.__chase_behaviour.calculate_best_move(
            self.__env.pakman_position,
            self._position,
            legal_actions
        )