from __future__ import annotations
from enum import Enum
from typing_extensions import Self


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Beam:
    direction: Direction
    x: int
    y: int
    
    def __init__(self, direction: Direction = Direction.RIGHT, x: int = 0, y: int = 0) -> None:
        self.direction = direction
        self.x = x
        self.y = y

    def move(self) -> None:
        match self.direction:
            case Direction.UP:
                self.y -= 1
            case Direction.DOWN:
                self.y += 1
            case Direction.LEFT:
                self.x -= 1
            case Direction.RIGHT:
                self.x += 1


class LightSystem:
    char_map: list[list[str]]
    energized_map: list[list[int]]
    split_map: list[list[bool]]
    
    beams: list[Beam]
    
    width: int
    height: int
    
    # / 
    R_MIRROR_MAP = {
        Direction.RIGHT: Direction.UP,
        Direction.LEFT: Direction.DOWN,
        Direction.UP: Direction.RIGHT,
        Direction.DOWN: Direction.LEFT
    }
    
    # \
    L_MIRROR_MAP = {
        Direction.RIGHT: Direction.DOWN,
        Direction.LEFT: Direction.UP,
        Direction.UP: Direction.LEFT,
        Direction.DOWN: Direction.RIGHT
    }
    
    DIR_TO_CHAR_MAP = {
        Direction.RIGHT: ">",
        Direction.LEFT: "<",
        Direction.UP: "^",
        Direction.DOWN: "v"
    }
    
    def __init__(self, lines: list[str], start_beam: Beam = Beam()) -> None:
        self.char_map = []
        self.beams = []
        
        # Parse
        for line in lines:
            line = line.strip()
            self.char_map.append([])
            for c in line:
                self.char_map[-1].append(c)
                
        self.width = len(self.char_map[0])
        self.height = len(self.char_map)
                
        # Place the starting beam
        self.beams.append(start_beam)
        
        # Init maps
        self.energized_map = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.split_map = [[False for _ in range(self.width)] for _ in range(self.height)]
        
    def step(self) -> Self:
        for beam in self.beams:
            # Check if out of bounds
            if beam.x >= self.width or beam.x < 0 \
                or beam.y >= self.height or beam.y < 0:
                    self.beams.remove(beam)
                    continue
            
            # Tick energized
            self.energized_map[beam.y][beam.x] = 1
            
            # Get tile
            tile = self.char_map[beam.y][beam.x]
        
            # Process mirrors
            if tile == "/":
                beam.direction = self.R_MIRROR_MAP[beam.direction]
            if tile == "\\":
                beam.direction = self.L_MIRROR_MAP[beam.direction]
                
            # Process splitters
            if tile == "-" and beam.direction in [Direction.UP, Direction.DOWN]:
                if not self.split_map[beam.y][beam.x]:
                    beam.direction = Direction.LEFT
                    self.beams.append(Beam(direction=Direction.RIGHT, x=beam.x, y=beam.y))
                    self.split_map[beam.y][beam.x] = True
                else:
                    self.beams.remove(beam)
            
            if tile == "|" and beam.direction in [Direction.LEFT, Direction.RIGHT]:
                if not self.split_map[beam.y][beam.x]:
                    beam.direction = Direction.UP
                    self.beams.append(Beam(direction=Direction.DOWN, x=beam.x, y=beam.y))
                    self.split_map[beam.y][beam.x] = True
                else:
                    self.beams.remove(beam)
                
            # Move
            beam.move()
            
        return self
                
    def print(self) -> Self:
        for y, row in enumerate(self.char_map):
            for x, tile in enumerate(row):
                for beam in self.beams:
                    if beam.x == x and beam.y == y:
                        print(self.DIR_TO_CHAR_MAP[beam.direction], end="")
                        break
                else:
                    print(tile, end="")
            print()
        print()
        return self
    
    def print_energized(self) -> Self:
        for row in self.energized_map:
            for tile in row:
                print("#" if tile else ".", end="")
            print()
        print()
        return self
    
    def count_energized(self) -> int:
        count = 0
        for row in self.energized_map:
            for tile in row:
                if tile:
                    count += 1
        return count


def main() -> None:
    lines = open("input.txt", "r").readlines()
    TRIES = 1000
    
    # Ex. 1
    light_system = LightSystem(lines)
    for _ in range(TRIES):
        light_system.step()
    
    # light_system.print_energized()
    print(light_system.count_energized())
    
    # Ex. 2
    width = light_system.width
    height = light_system.height
    max_energized = 0
    
    def try_ls(ls: LightSystem):
        nonlocal max_energized
        for _ in range(TRIES):
            ls.step()
        if (x := ls.count_energized()) > max_energized:
            max_energized = x
    
    for y in range(height):
        light_system = LightSystem(lines, Beam(Direction.RIGHT, 0, y))
        try_ls(light_system)
            
        light_system = LightSystem(lines, Beam(Direction.LEFT, width - 1, y))
        try_ls(light_system)
    
    for x in range(width):
        light_system = LightSystem(lines, Beam(Direction.DOWN, x, 0))
        try_ls(light_system)
        
        light_system = LightSystem(lines, Beam(Direction.UP, x, height - 1))
        try_ls(light_system)
        
    print(max_energized)
        

if __name__ == "__main__":
    main()
    