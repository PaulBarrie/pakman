from game.actions import Action
from game.position import Position


class ScaredBehaviour:
	def __init__(self):
		pass

	def calculate_best_move(
		self, 
		target, 
		current_position: Position, 
		actions: list[Action]
	) -> Action:
		raise NotImplementedError()