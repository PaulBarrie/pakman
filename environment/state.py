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

    def __repr__(self) -> str:
        return f"N: {self.__north}, W: {self.__west}, E: {self.__east}, S: {self.__south}"

class AreaRadar:
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
    def north_west(self) -> bool:
        return self.__north_west

    @property
    def north_east(self) -> bool:
        return self.__north_east
    
    @property
    def south_west(self) -> bool:
        return self.__south_west

    @property
    def south_east(self) -> bool:
        return self.__south_east

    def __init__(self, north, south, west, east, north_west, north_east, south_west, south_east) -> None:
        self.__north = north
        self.__south = south
        self.__west = west
        self.__east = east
        self.__north_west = north_west
        self.__north_east = north_east
        self.__south_west = south_west
        self.__south_east = south_east

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, AreaRadar) \
            and self.__north == __o.north \
            and self.__west == __o.west \
            and self.__east == __o.east \
            and self.__south == __o.south \
            and self.__north_west == __o.north_west \
            and self.__north_east == __o.north_east \
            and self.__south_west == __o.south_west \
            and self.__south_east == __o.south_east

    def __hash__(self) -> int:
        return hash((self.__north, self.__west, self.__east, self.__south, self.__north_west, self.__north_east, self.__south_west, self.__south_east))

    def __repr__(self) -> str:
        return f"N: {self.__north}, W: {self.__west}, E: {self.__east}, S: {self.__south}, NW: {self.__north_west}, NE: {self.__north_east}, SW: {self.__south_west}, SE: {self.__south_east}"

    @staticmethod
    def compute_radar(pakman_position: Position, targets: list[Position], max_distance: int) -> AreaRadar:
        valid_targets = list(filter(lambda t: t.get_distance(pakman_position) <= max_distance, targets))

        north = False
        west = False
        east = False
        south = False
        north_west = False
        north_east = False
        south_west = False
        south_east = False

        for v in valid_targets:
            if v.column == pakman_position.column:
                if v.row < pakman_position.row:
                    north = True
                else:
                    south = True
                continue
            
            if v.row == pakman_position.row:
                if v.column < pakman_position.column:
                    west = True
                else:
                    east = True
                continue

            if v.column < pakman_position.column:
                if v.row < pakman_position.row:
                    north_west = True
                else:
                    north_east = False
            else:
                if v.row < pakman_position.row:
                    south_west = True
                else:
                    south_east = False
        return AreaRadar(north, south, west, east, north_west, north_east, south_west, south_east)
                    


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

    def __repr__(self) -> str:
        return f"N: {self.__north}, W: {self.__west}, E: {self.__east}, S: {self.__south}, distance: {self.__distance}"

    @staticmethod
    def compute_radar(pakman_position: Position, sorted_targets: list[Position], index: int) -> LongRangeRadar:
        closest_target_position = sorted_targets[index]
        dist = closest_target_position.get_distance(pakman_position)

        return LongRangeRadar(
            closest_target_position.row < pakman_position.row,
            closest_target_position.row > pakman_position.row,
            closest_target_position.column < pakman_position.column,
            closest_target_position.column > pakman_position.column,
            Distance.int_to_distance(dist)
        )



class State:
    STATE_VAL_SEPARATOR = ""

    @property
    def ghost_radar(self) -> AreaRadar:
        return self.__ghost_radar

    @property
    def gum_radar(self) -> LongRangeRadar:
        return self.__gum_radar
    
    @property
    def wall_radar(self) -> ShortRangeRadar:
        return self.__wall_radar

    def __init__(
        self, 
        ghost_radar: AreaRadar,
        gum_radar: LongRangeRadar, 
        wall_radar: ShortRangeRadar
    ) -> None:
        self.__ghost_radar = ghost_radar
        self.__gum_radar = gum_radar
        self.__wall_radar = wall_radar

    @staticmethod
    def compute_state(
        ghost_positions: list[Position], 
        pakman_position: Position, 
        gum_positions: list[Position], 
        wall_positions: list[Position]
    ) -> State:

        sorted_gums_by_distance = list(sorted(
            gum_positions,
            key = lambda gp: gp.get_distance(pakman_position)
        ))

        return State(
            AreaRadar.compute_radar(pakman_position, ghost_positions, 5),
            LongRangeRadar.compute_radar(pakman_position, sorted_gums_by_distance, 0),
            ShortRangeRadar.compute_radar(pakman_position, wall_positions)
        )

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, State) \
            and self.__ghost_radar == __o.ghost_radar \
            and self.__gum_radar == __o.gum_radar \
            and self.__wall_radar == __o.wall_radar

    def __hash__(self) -> int:
        return hash(( 
            hash(self.__gum_radar), 
            hash(self.__wall_radar),
            hash(self.__ghost_radar)
        ))

    def __repr__(self) -> str:
        return f'ghosts: {self.__ghost_radar}, gums: {self.__gum_radar}, walls: {self.__wall_radar}'
