from game.actions import Action
from game.agent import IAgent
from game.position import Position


class ScaredBehaviour:
    def calculate_best_move(
        self, 
        target: IAgent, 
        current_position: Position, 
        actions: list[Action]
    ) -> Action:
        raise NotImplementedError()

class DefaultScaredBehaviour(ScaredBehaviour):
    def calculate_best_move(
        self, 
        target: IAgent, 
        current_position: Position, 
        actions: list[Action]
    ) -> Action:
        return sorted(
            actions,
            key = lambda action: \
                current_position.apply_action(action)
                    .get_distance(target.position),
            reverse = True
        )[0]