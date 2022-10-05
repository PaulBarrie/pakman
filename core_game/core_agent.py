from actions import Action
from position import Position

class CoreAgent:
    @property
    def position(self) -> Position:
        return self._position

    def __init__(self, initial_position: Position):
        self._position = initial_position

    def move_to_position(self, position: Position) -> None:
        self._position = position

    def _best_action(self) -> Action:
        raise NotImplemented()

    def step(self) -> tuple[Action, float]:
        raise NotImplemented()