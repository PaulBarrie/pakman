class Actions:
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    @classmethod
    def as_list(cls) -> list[tuple[int, int]]:
        return [cls.UP, cls.DOWN, cls.LEFT, cls.RIGHT]

