from position import Position

class CoreAgent:
    @property
    def position(self) -> Position:
        return self._position

    def __init__(self, initial_position: Position):
        self._position = initial_position

    def step(self) -> None:
        raise NotImplemented()