from __future__ import annotations
from core_game.position import Position
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
        closest_target_position = LongRangeRadar.sort_by_distance(pakman_position, targets)[0]
        dist = closest_target_position.get_distance(pakman_position)

        return LongRangeRadar(
            closest_target_position.row < pakman_position.row,
            closest_target_position.row > pakman_position.row,
            closest_target_position.column < pakman_position.column,
            closest_target_position.column > pakman_position.column,
            Distance.int_to_distance(dist)
        )

    @staticmethod
    def sort_by_distance(pakman_position: Position, targets: list[Position]):
        return list(sorted(
            targets,
            key = lambda gp: gp.get_distance(pakman_position)
        ))



class State:
    STATE_VAL_SEPARATOR = ""

    @property
    def closest_ghost_radar(self) -> LongRangeRadar:
        return self.__closest_ghost_radar

    @property
    def second_closest_ghost_radar(self) -> LongRangeRadar:
        return self.__second_closest_ghost_radar

    @property
    def gum_radar(self) -> ShortRangeRadar:
        return self.__gum_radar
    
    @property
    def wall_radar(self) -> ShortRangeRadar:
        return self.__wall_radar

    def __init__(
        self, 
        closest_ghost_radar: LongRangeRadar,
        second_closest_ghost_radar: LongRangeRadar,
        gum_radar: ShortRangeRadar, 
        wall_radar: ShortRangeRadar
    ) -> None:
        self.__closest_ghost_radar = closest_ghost_radar
        self.__second_closest_ghost_radar = second_closest_ghost_radar
        self.__gum_radar = gum_radar
        self.__wall_radar = wall_radar

    @staticmethod
    def compute_state(
        ghost_positions: list[Position], 
        pakman_position: Position, 
        gum_positions: list[Position], 
        wall_positions: list[Position]
    ) -> State:

        return State(
            LongRangeRadar.compute_radar(pakman_position, ghost_positions),
            LongRangeRadar.compute_radar(pakman_position, LongRangeRadar.sort_by_distance(pakman_position, ghost_positions[1:])),
            ShortRangeRadar.compute_radar(pakman_position, gum_positions),
            ShortRangeRadar.compute_radar(pakman_position, wall_positions)
        )

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, State) \
            and self.__closest_ghost_radar == __o.closest_ghost_radar \
            and self.__second_closest_ghost_radar == __o.second_closest_ghost_radar \
            and self.__gum_radar == __o.gum_radar \
            and self.__wall_radar == __o.wall_radar

    def __hash__(self) -> int:
        return hash(( 
            hash(self.__gum_radar), 
            hash(self.__wall_radar), 
            hash(self.__closest_ghost_radar),
            hash(self.__second_closest_ghost_radar)
        ))

    def __repr__(self) -> str:
        closest_ghost_state = self.__state_str(self.__closest_ghost_radar)
        second_closest_ghost_state = self.__state_str(self.__second_closest_ghost_radar)
        gum_state = self.__state_str(self.__gum_radar)
        wall_state = self.__state_str(self.__wall_radar)

        return f'closest ghost: {closest_ghost_state}, second closest ghost: {second_closest_ghost_state}, gums: {gum_state}, walls: {wall_state}'
