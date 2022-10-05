from core_game.actions import Action
from core_game.position import Position


class ScaredBehaviour:
    def calculate_best_move(
        self, 
        target_position: Position, 
        current_position: Position, 
        actions: list[Action]
    ) -> Action:
        raise NotImplementedError()

class DefaultScaredBehaviour(ScaredBehaviour):
    def calculate_best_move(
        self, 
        target_position: Position, 
        current_position: Position, 
        actions: list[Action]
    ) -> Action:
        return sorted(
            actions,
            key = lambda action: \
                current_position.apply_action(action)
                    .get_distance(target_position),
            reverse = True
        )[0]