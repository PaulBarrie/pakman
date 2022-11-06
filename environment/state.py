from __future__ import annotations
from core_game.position import Position, RelativePosition
from core_game.directions import Direction
from core_game.actions import Action
from environment.metrics import *
from collections import deque


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
        return hash((self.__north, self.__west, self.__east, self.__south, self.__north_west, self.__north_east,
                     self.__south_west, self.__south_east))

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

    def __str__(self):
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

    # @staticmethod
    # def sort_by_distance(pakman_position: Position, targets: list[Position]):
    #     return list(sorted(
    #         targets,
    #         key = lambda gp: gp.get_distance(pakman_position)
    #     ))

    @staticmethod
    def check_threat(
            start: Position,
            discovered: list[Position],
            threats: list[tuple[int, int]],
            walls: list[tuple[int, int]],
            max_steps: int = 8
    ) -> bool:
        """
        Returns true if there is a threat in the given direction
        """
        dist = 1
        starting_point = (start, dist)

        search_field = deque()
        search_field.push(starting_point)

        while len(search_field) > 0 and dist < max_steps:
            pos, dist = search_field.pop()
            if pos in discovered or dist > max_steps:
                continue
            if pos in threats:
                return True
            discovered.append(pos)
            discovered = list(set(discovered))

            for action in Action.as_list():
                next_pos = pos.apply_action(action)
                if next_pos in walls:
                    continue
                next_x, next_y = next_pos
                search_field.append((next_x, next_y, dist + 1))

        return False


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

    def __repr__(self):
        return f"N: {self.__north}, S: {self.__south}, W: {self.__south}, E: {self.__east}"
    @staticmethod
    def check_threat(
            start: Position,
            discovered: list[Position],
            threats: list[Position],
            walls: list[Position],
            max_steps=8
    ) -> bool:
        """
        Returns true if there is a threat in the given direction
        """
        dist = 1
        starting_point = [start, dist]

        search_field = deque()
        search_field.append(starting_point)

        while len(search_field) > 0 and dist < max_steps:
            field = search_field.pop()
            pos, dist = (field[0], field[1])
            if pos in discovered or dist > max_steps:
                continue
            if pos in threats:
                return True
            discovered.append(pos)
            discovered = list(set(discovered))

            for action in Action.as_list():
                next_pos = pos.apply_action(action)
                if next_pos in walls:
                    continue
                next_x, next_y = (next_pos.row, next_pos.column)
                search_field.append((Position(next_x, next_y), dist + 1))

        return False

    @staticmethod
    def compute_radar(pakman: Position, gums: list[Position], walls: [Position], ghosts: list[Position],
                      max_range: int = 8) -> TargetDirectionRadar:
        discovered = [pakman]

        candidate_directions = []
        for action in Action.as_list():
            if not TargetDirectionRadar.check_threat(pakman.apply_action(action), discovered, ghosts, walls):
                candidate_directions.append(action)

        if len(candidate_directions) <= 1:
            return TargetDirectionRadar(
                Action.UP in candidate_directions,
                Action.DOWN in candidate_directions,
                Action.LEFT in candidate_directions,
                Action.RIGHT in candidate_directions
            )
        relative_position_candidates = [rel_dir for rel_dir in RelativePosition.list() if
                                        [rel_dir.is_in_direction(action) for action in Action.as_list()]]
        gum_candidates = [gum for gum in gums if RelativePosition.get(pakman, gum) in relative_position_candidates]

        min_distance = 9999
        action = None
        for gum in gum_candidates:
            distance = pakman.get_distance(gum)
            if distance < min_distance:
                min_distance = distance
                action = Position.get_action_from(pakman, to=gum)

        return TargetDirectionRadar(
            action == Action.UP,
            action == Action.DOWN,
            action == Action.LEFT,
            action == Action.RIGHT
        )


class State:
    STATE_VAL_SEPARATOR = ""

    @property
    def ghost_radar(self) -> AreaRadar:
        return self.__ghost_radar

    # @property
    # def closest_ghost_radar(self) -> LongRangeRadar:
    #     return self.__closest_ghost_radar

    # @property
    # def second_closest_ghost_radar(self) -> LongRangeRadar:
    #     return self.__second_closest_ghost_radar

    @property
    def gum_radar(self) -> LongRangeRadar:
        return self.__gum_radar

    @property
    def wall_radar(self) -> ShortRangeRadar:
        return self.__wall_radar

    @property
    def target_radar(self) -> TargetDirectionRadar:
        return self.__target_radar

    def __init__(
            self,
            # closest_ghost_radar: LongRangeRadar,
            # second_closest_ghost_radar: LongRangeRadar,
            ghost_radar: AreaRadar,
            gum_radar: LongRangeRadar,
            wall_radar: ShortRangeRadar,
            target_radar: TargetDirectionRadar
    ) -> None:
        # self.__closest_ghost_radar = closest_ghost_radar
        # self.__second_closest_ghost_radar = second_closest_ghost_radar
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
        # sorted_ghosts_by_distance = list(sorted(
        #     ghost_positions,
        #     key = lambda gp: gp.get_distance(pakman_position)
        # ))

        sorted_gums_by_distance = list(sorted(
            gum_positions,
            key=lambda gp: gp.get_distance(pakman_position)
        ))

        return State(
            # LongRangeRadar.compute_radar(pakman_position, sorted_ghosts_by_distance, 0),
            # LongRangeRadar.compute_radar(pakman_position, sorted_ghosts_by_distance, 1),
            AreaRadar.compute_radar(pakman_position, ghost_positions, 5),
            LongRangeRadar.compute_radar(pakman_position, sorted_gums_by_distance, 0),
            ShortRangeRadar.compute_radar(pakman_position, wall_positions),
            TargetDirectionRadar.compute_radar(pakman_position, sorted_gums_by_distance, wall_positions,
                                               ghost_positions)
        )

    # def __eq__(self, __o: object) -> bool:
    #     return isinstance(__o, State) \
    #         and self.__closest_ghost_radar == __o.closest_ghost_radar \
    #         and self.__second_closest_ghost_radar == __o.second_closest_ghost_radar \
    #         and self.__gum_radar == __o.gum_radar \
    #         and self.__wall_radar == __o.wall_radar

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
        # closest_ghost_state = self.__state_str(self.__closest_ghost_radar)
        # second_closest_ghost_state = self.__state_str(self.__second_closest_ghost_radar)
        # gum_state = self.__state_str(self.__gum_radar)
        # wall_state = self.__state_str(self.__wall_radar)

        # return f'closest ghost: {self.__closest_ghost_radar}, second closest ghost: {self.__second_closest_ghost_radar}, gums: {self.__gum_radar}, walls: {self.__wall_radar}'
        return f'ghosts: {self.__ghost_radar}, gums: {self.__gum_radar}, walls: {self.__wall_radar}, target: {self.__target_radar}'
