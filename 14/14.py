from __future__ import annotations
from enum import Enum
from typing import Final, Iterable, TypeVar, Tuple

T = TypeVar('T')


class CycleData:
    start_offset: int
    period: int
    values: list[int]
    
    def __init__(self, start_offset: int, period: int, values: list[int]) -> None:
        self.start_offset = start_offset
        self.period = period
        self.values = values
        
    def __str__(self) -> str:
        return f"start: {self.start_offset}, period: {self.period} | {self.values}"


class Field(Enum):
    EMPTY = 0
    ROCK = 1
    BARRIER = 2
    
    
class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class RockSystem:
    array_2d: list[list[Field]]
    cycle_data: CycleData | None
    
    def __init__(self, lines: list[str] | None = None, array_2d: list[list[Field]] | None = None) -> None:
        self.cycle_data = None
        
        if array_2d:
            # From 2D array
            self.array_2d = array_2d
        else:
            self.array_2d = []
            
            if not lines:
                # Empty RockSystem object created
                return
            
            # Parse input
            for line in lines:
                line = line.strip()
                self.array_2d.append([])
                for c in line:
                    if c == "O":
                        self.array_2d[-1].append(Field.ROCK)
                    elif c == "#":
                        self.array_2d[-1].append(Field.BARRIER)
                    else:
                        self.array_2d[-1].append(Field.EMPTY)
    
    def get_tilted(self, direction: Direction) -> RockSystem:
        is_transposed: Final[bool] = direction in [Direction.UP, Direction.DOWN]
        is_reversed: Final[bool] = direction in [Direction.UP, Direction.LEFT]
        
        a2d: Final[list[list[Field]]] = transpose(self.array_2d) if is_transposed else self.array_2d
        
        # For each row collect a list of groups.
        # Each group counts the number of rocks
        #   and ends at a barrier, or at end of line.
        groups: list[list[int]] = []
        row_range: Iterable
        
        for row in a2d:
            buffer: int = 0
            groups.append([])
            
            if is_reversed:
                row_range = reversed(range(len(row)))
            else:
                row_range = range(len(row))
            
            for i in row_range:
                if row[i] == Field.ROCK:
                    buffer += 1
                
                if is_reversed:
                    at_end = i == 0
                else:
                    at_end = i == len(row) - 1
                
                if row[i] == Field.BARRIER or at_end:
                    groups[-1].append(buffer)
                    buffer = 0
        
        # Build the resulting 2D array
        WIDTH = len(a2d[0])
        HEIGHT = len(a2d)
        
        res: list[list[Field]] = [[Field.EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]
        
        for y in range(HEIGHT):
            row_groups = groups.pop(0)
            hit = 0
            approaching = False
            
            if is_reversed:
                row_range = reversed(range(WIDTH))
            else:
                row_range = range(WIDTH)
            
            for x in row_range:
                # Determine if we are approaching the barrier / EOL
                if is_reversed:
                    if x - row_groups[hit] < 0 or a2d[y][x - row_groups[hit]] == Field.BARRIER:
                        approaching = True
                else:
                    if x + row_groups[hit] >= WIDTH or a2d[y][x + row_groups[hit]] == Field.BARRIER:
                        approaching = True
                    
                # Copy barriers, rest is empty
                if a2d[y][x] == Field.BARRIER:
                    res[y][x] = Field.BARRIER
                    # Reset
                    approaching = False
                    # Next group
                    hit += 1
                elif approaching:
                    # Place rocks if approaching
                    res[y][x] = Field.ROCK
                    
        return RockSystem(array_2d=(transpose(res) if is_transposed else res))

    def get_load(self) -> int:
        sum = 0
        HEIGHT = len(self.array_2d)
        
        for i in range(HEIGHT):
            for el in self.array_2d[i]:
                if el == Field.ROCK:
                    sum += HEIGHT - i
        
        return sum
    
    # Set window and cycles higher to avoid wrong results caused by collisions
    def find_period(self, cycles: int, window: int) -> CycleData:
        if self.cycle_data:         # calculate this only once
            return self.cycle_data
        
        curr = self
        previous: list[int] = []
        
        for _ in range(cycles):
            curr = curr.get_tilted(Direction.UP)    \
                    .get_tilted(Direction.LEFT)  \
                    .get_tilted(Direction.DOWN)  \
                    .get_tilted(Direction.RIGHT)
                    
            load = curr.get_load()
            previous.append(load)
            
            for i in range(len(previous) - window):
                for offset in range(i + window, len(previous) - window):
                    if previous[i:(i + window)] == previous[(i + offset):(i + window + offset)]:
                        cycle_data = CycleData(start_offset=i, period=offset, values=previous)
                        
                        self.cycle_data = cycle_data
                        return cycle_data
        
        raise Exception("Period not found")

    def get_load_in_cycles(self, cycles: int) -> int:
        if not self.cycle_data:
            raise Exception("Call find_period() first")
        
        if cycles <= self.cycle_data.start_offset + self.cycle_data.period:
            return self.cycle_data.values[cycles - 1]
        
        repeating_values = self.cycle_data.values[:-self.cycle_data.period]
        return repeating_values[cycles % self.cycle_data.period - 1]

    @staticmethod
    def str_of_array_2d(a2d: list[list[Field]]) -> str:
        res: str = ""
        for row in a2d:
            for c in row:
                if c == Field.ROCK:
                    res += "O"
                elif c == Field.BARRIER:
                    res += "#"
                else:
                    res += "."
            res += "\n"
        return res
    
    def __repr__(self) -> str:
        return self.str_of_array_2d(self.array_2d)


def transpose(a2d: list[list[T]]) -> list[list[T]]:
    return list(map(lambda x: list(x), zip(*a2d)))


def main() -> None:
    lines = open("input.txt", "r").readlines()
    rock_system = RockSystem(lines)
    
    # Ex. 1
    print("Ex. 1")
    tilted_up = rock_system.get_tilted(Direction.UP)
    print(tilted_up.get_load())
    
    # Ex. 2
    print("Ex. 2")
    rock_system.find_period(cycles=10000, window=500)
    
    CYCLES = 1000000000
    print(rock_system.get_load_in_cycles(CYCLES))

if __name__ == "__main__":
    main()
    