from __future__ import annotations

from collections import deque

from core_game.directions import Direction
from core_game.ghost import Ghost
from core_game.position import Position, RelativePosition
from core_game.actions import Action
from environment.metrics import *


class ShortRangeRadar:
    @property
    def north(self) -> bool:
        return self.__north

    @property
    def south(self) -> bool:
        return self.__south

    @property
    def west(self) -> bool:
        return self.__west

    @property
    def east(self) -> bool:
        return self.__east

    def __init__(self, north: bool, south: bool, west: bool, east: bool) -> None:
        self.__north = north
        self.__south = south
        self.__west = west
        self.__east = east

    @staticmethod
    def compute_radar(position: Position, targets: list[Position]) -> ShortRangeRadar:
        north_position = position.apply_action(Action.UP)
        south_position = position.apply_action(Action.DOWN)
        west_position = position.apply_action(Action.LEFT)
        east_position = position.apply_action(Action.RIGHT)

        return ShortRangeRadar(
            north_position in targets,
            south_position in targets,
            west_position in targets,
            east_position in targets
        )

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, ShortRangeRadar) \
               and self.__north == __o.north \
               and self.__south == __o.south \
               and self.__west == __o.west \
               and self.__east == __o.east

    def __hash__(self) -> int:
        return hash((self.__north, self.__south, self.__west, self.__east))


class LongRangeRadar:
    """
        Directions
            NE  | NO
                |
        ----------------
            SE  | SO
                |
    """

    @property
    def north(self) -> bool:
        return self.__north

    @property
    def south(self) -> bool:
        return self.__south

    @property
    def west(self) -> bool:
        return self.__west

    @property
    def east(self) -> bool:
        return self.__east

    @property
    def distance(self) -> Distance:
        return self.__distance

    def __init__(self, north, south, west, east, distance: Distance) -> None:
        self.__north = north
        self.__south = south
        self.__west = west
        self.__east = east
        self.__distance = distance

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, LongRangeRadar) \
               and self.__north == __o.north \
               and self.__south == __o.south \
               and self.__west == __o.west \
               and self.__east == __o.east \
               and self.__distance == __o.distance

    def __hash__(self) -> int:
        return hash((self.__north, self.__south, self.__west, self.__east, self.__distance))

    @staticmethod
    def compute_radar(pakman_position: Position, targets: list[Position]) -> LongRangeRadar:
        closest_target_position = list(sorted(
            targets,
            key=lambda gp: gp.get_distance(pakman_position)
        ))[0]
        dist = closest_target_position.get_distance(pakman_position)

        return LongRangeRadar(
            closest_target_position.row < pakman_position.row,
            closest_target_position.row > pakman_position.row,
            closest_target_position.column < pakman_position.column,
            closest_target_position.column > pakman_position.column,
            Distance.int_to_distance(dist)
        )


class TargetDirectionRadar:
    """
    This radar gives the best direction to follow taking into account. To do so,
    it chooses among the direction where there are no ghosts, the one which leads
    the fastest to a gum.
    """

    @property
    def north(self) -> bool:
        return self.__north

    @property
    def south(self) -> bool:
        return self.__south

    @property
    def west(self) -> bool:
        return self.__west

    @property
    def east(self) -> bool:
        return self.__east

    def __init__(self, north: bool, south: bool, west: bool, east: bool) -> None:
        self.__north = north
        self.__south = south
        self.__west = west
        self.__east = east

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, TargetDirectionRadar) \
               and self.__north == __o.north \
               and self.__south == __o.south \
               and self.__west == __o.west \
               and self.__east == __o.east

    def __hash__(self) -> int:
        return hash((self.__north, self.__south, self.__west, self.__east))

    def _check_threat(
            start: tuple(int, int),
            max_steps: int, discovered: set(),
            threats: list[tuple[int, int]],
            walls: list[tuple[int, int]]
    ) -> bool:
        dist = 1
        starting_point = (start[0], start[1], dist)

        search_field = deque()
        search_field.push(starting_point)

        while len(search_field) > 0 and dist < max_steps:
            row, col, dist = search_field.pop(0)
            pos = (row, col)

            if pos in discovered or dist > max_steps:
                continue

            if pos in threats:
                return True

            discovered.add(pos)

            for action in [Actions.NORTH, Actions.SOUTH, Actions.WEST, Actions.EAST]:
                next_pos = apply_action(pos, action)
                if next_pos in walls:
                    continue
                next_x, next_y = next_pos
                search_field.append((next_x, next_y, dist + 1))

        return False

    @staticmethod
    def compute_radar(pakman: Position, gums: list[Position], ghosts: list[Ghost]) -> TargetDirectionRadar:
        candidate_directions = [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]
        for ghost in ghosts:
            relative_position = RelativePosition.get(pakman, ghost.position)
            # If ghost direction is West and relative position is NE or direction is East and position is NO
            if (ghost.direction == Direction.WEST and relative_position == RelativePosition.NE) or (
                    ghost.direction == Direction.EAST and relative_position == RelativePosition.NW
            ):
                candidate_directions.remove(Direction.NORTH)
            # If ghost direction is West and relative position is SE or direction is East and position is SO
            elif (ghost.direction == Direction.WEST and relative_position == RelativePosition.SE) or (
                    ghost.direction == Direction.EAST and relative_position == RelativePosition.SW
            ):
                candidate_directions.remove(Direction.SOUTH)
            # If ghost direction is North and relative position is NE or direction is South and position is SE
            elif (ghost.direction == Direction.NORTH and relative_position == RelativePosition.NE) or (
                    ghost.direction == Direction.SOUTH and relative_position == RelativePosition.SE
            ):
                candidate_directions.remove(Direction.WEST)
            # If ghost direction is North and relative position is NO or direction is South and position is SO
            elif (ghost.direction == Direction.NORTH and relative_position == RelativePosition.NW) or (
                    ghost.direction == Direction.SOUTH and relative_position == RelativePosition.SW):
                candidate_directions.remove(Direction.EAST)

        if len(candidate_directions) <= 1:
            return TargetDirectionRadar(
                Direction.NORTH in candidate_directions,
                Direction.SOUTH in candidate_directions,
                Direction.WEST in candidate_directions,
                Direction.EAST in candidate_directions
            )
        relative_position_candidates = [rel_dir for rel_dir in RelativePosition.list() if
                                        [rel_dir.is_in_direction(direction) for direction in Direction.as_list()]]
        gum_candidates = [gum for gum in gums if RelativePosition.get(pakman, gum) in relative_position_candidates]

        min_distance = 9999
        direction = None
        for gum in gum_candidates:
            distance = pakman.get_distance(gum)
            if distance < min_distance:
                min_distance = distance
                direction = Direction.from_element_to(pakman, gum)

        return TargetDirectionRadar(
            direction == Direction.NORTH,
            direction == Direction.SOUTH,
            direction == Direction.WEST,
            direction == Direction.EAST
        )


class State:
    STATE_VAL_SEPARATOR = ""

    @property
    def ghost_radar(self) -> LongRangeRadar:
        return self.__ghost_radar

    @property
    def gum_radar(self) -> ShortRangeRadar:
        return self.__gum_radar

    @property
    def wall_radar(self) -> ShortRangeRadar:
        return self.__wall_radar

    def __init__(
            self,
            ghost_radar: LongRangeRadar,
            gum_radar: ShortRangeRadar,
            wall_radar: ShortRangeRadar,
            target_radar: TargetDirectionRadar
    ) -> None:
        self.__ghost_radar = ghost_radar
        self.__gum_radar = gum_radar
        self.__wall_radar = wall_radar
        self.__target_radar = target_radar

    @staticmethod
    def compute_state(
            ghost_positions: list[Position],
            pakman_position: Position,
            gum_positions: list[Position],
            wall_positions: list[Position]
    ) -> State:
        return State(
            LongRangeRadar.compute_radar(pakman_position, ghost_positions),
            ShortRangeRadar.compute_radar(pakman_position, gum_positions),
            ShortRangeRadar.compute_radar(pakman_position, wall_positions),
            TargetDirectionRadar.compute_radar(pakman_position, gum_positions, ghost_positions)
        )

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, State) \
               and self.__ghost_radar == __o.ghost_radar \
               and self.__gum_radar == __o.gum_radar \
               and self.__wall_radar == __o.wall_radar \
               and self.__target_radar == __o.target_radar

    def __hash__(self) -> int:
        return hash((
            hash(self.__gum_radar),
            hash(self.__wall_radar),
            hash(self.__ghost_radar),
            hash(self.__target_radar)
        ))

    def __repr__(self) -> str:
        ghost_state = self.__state_str(self.__ghost_radar)
        gum_state = self.__state_str(self.__gum_radar)
        wall_state = self.__state_str(self.__wall_radar)
        target_state = self.__state_str(self.__target_radar)

        return f'ghost: {ghost_state}, gums: {gum_state}, walls: {wall_state}'
