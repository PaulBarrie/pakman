from creatures.agent import IAgent
from creatures.position import Position

class ChaseBehaviour:
	def calculate_best_move(
		self, 
		target: IAgent, 
		current_position: Position, 
		actions: list[tuple[int, int]]
	) -> tuple[int, int]:
		raise NotImplementedError()

class AggressiveChaseBehaviour(ChaseBehaviour):
    def calculate_best_move(
        self, 
        target: IAgent, 
        current_position: Position, 
        actions: list[tuple[int, int]]
    ) -> tuple[int, int]:
        return sorted(
            actions,
            key = lambda action: \
                current_position.apply_action(action)
                .get_distance(target.position)
        )[0]

class AmbushChaseBehaviour(ChaseBehaviour):
    def calculate_best_move(
        self, 
        target: IAgent, 
        current_position: Position, 
        actions: list[tuple[int, int]]
    ) -> tuple[int, int]:
        targeted_position = target.position.follow_direction()
        return sorted(
            actions,
            key = lambda action: \
                current_position.apply_action(action)
                .get_distance(targeted_position)
        )[0]