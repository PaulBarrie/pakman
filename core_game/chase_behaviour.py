from core_game.actions import Action
from core_game.position import Position

class ChaseBehaviour:
	def calculate_best_move(
		self, 
		target_position: Position, 
		current_position: Position, 
		actions: list[Action]
	) -> Action:
		raise NotImplementedError()

class AggressiveChaseBehaviour(ChaseBehaviour):
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
                .get_distance(target_position)
        )[0]

class AmbushChaseBehaviour(ChaseBehaviour):
    def calculate_best_move(
        self, 
        target_position: Position, 
        current_position: Position, 
        actions: list[Action]
    ) -> Action:
        targeted_position = target_position.follow_direction()
        return sorted(
            actions,
            key = lambda action: \
                current_position.apply_action(action)
                    .get_distance(targeted_position)
        )[0]