from position import Position

class IAgent:
    @property
    def position(self):
        return self.__position

    def __init__(self, initial_position: Position):
        self.__position = initial_position

    def step(self) -> None:
        raise NotImplemented()