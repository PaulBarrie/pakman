class ScaredBehaviour:
  def __init__(self):
    pass

  def calculate_best_move(
    self, 
    target, 
    current_position: tuple[int, int], 
    actions: list[tuple[int, int]]
  ) -> tuple[int, int]:
    raise NotImplementedError()