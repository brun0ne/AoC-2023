import itertools
from typing import Tuple

import sys
sys.setrecursionlimit(100000)

class Pipe:
    def __init__(self, lines: list[str], pos_x: int, pos_y: int):
        self.x = pos_x
        self.y = pos_y
        self.symbol = lines[pos_y][pos_x]
        
        self.up: Pipe | None = None
        self.down: Pipe | None = None
        self.left: Pipe | None = None
        self.right: Pipe | None = None
    
    def __repr__(self) -> str:
        up_s = self.up.symbol if self.up else "."
        down_s = self.down.symbol if self.down else "."
        left_s = self.left.symbol if self.left else "."
        right_s = self.right.symbol if self.right else "."
        
        return f"<{self.symbol}: ({up_s}, {down_s}, {left_s}, {right_s})>"
    
    def __eq__(self, __value) -> bool:
        if not __value:
            return False
        return self.x == __value.x and self.y == __value.y and self.symbol == __value.symbol
    
    def try_connect(self, pipes2D: list[list]) -> None:
        up: Pipe | None = None
        down: Pipe | None = None
        left: Pipe | None = None
        right: Pipe | None = None
        
        if self.y > 0:
            up = pipes2D[self.y - 1][self.x]
        if self.y < len(pipes2D) - 1:
            down = pipes2D[self.y + 1][self.x]
        if self.x > 0:
            left = pipes2D[self.y][self.x - 1]
        if self.x < len(pipes2D[0]) - 1:
            right = pipes2D[self.y][self.x + 1]
        
        # north - up
        # south - down
        # west  - left
        # east  - right
        
        if up:
            if up.symbol in "|7FS" and self.symbol in "|LJS":
                up.down = self
        if down:
            if down.symbol in "|LJS" and self.symbol in "|7FS":
                down.up = self
        if left:
            if left.symbol in "-FLS" and self.symbol in "-J7S":
                left.right = self
        if right:
            if right.symbol in "-J7S" and self.symbol in "-FLS":
                right.left = self
                
    def test_for_cycle(self, pipes2D: list[list], coming_from: Tuple[int, int] = (0, 0), start = None, acc: list = []) -> Tuple[bool, list]:
        if coming_from == (0, 0):
            start = self
        
        match coming_from:
            case n if n != (0, 0) and self == start:
                return (True, acc)
            case _:
                if self.up and n != (0, 1):
                    c, path = self.up.test_for_cycle(pipes2D, (0, -1), start, acc + [self])
                    if c: return (c, path)
                if self.down and n != (0, -1):
                    c, path = self.down.test_for_cycle(pipes2D, (0, 1), start, acc + [self])
                    if c: return (c, path)
                if self.right and n != (1, 0):
                    c, path = self.right.test_for_cycle(pipes2D, (-1, 0), start, acc + [self])
                    if c: return (c, path)
                if self.left and n != (-1, 0):
                    c, path = self.left.test_for_cycle(pipes2D, (1, 0), start, acc + [self])
                    if c: return (c, path)
        return (False, [])

class PipeSystem:
    # Assuming NxM grid
    pipes2D: list[list[Pipe]]
    start: Pipe
    
    def __init__(self, lines: list[str]) -> None:
        self.pipes2D: list[list[Pipe]] = []
        
        # Parse
        for y in range(len(lines)):
            self.pipes2D.append([])
            for x in range(len(lines[0].strip())):
                self.pipes2D[-1].append(Pipe(lines, x, y))
        
        # Connect
        for pipe in itertools.chain(*self.pipes2D):
            pipe.try_connect(self.pipes2D)
            
        self.determine_start()
            
    @property
    def width(self) -> int:
        return len(self.pipes2D[0])
            
    @property
    def height(self) -> int:
        return len(self.pipes2D)
            
    def get_pipe_by_symbol(self, symbol: str) -> Pipe:
        for pipe in itertools.chain(*self.pipes2D):
            if pipe.symbol == symbol:
                return pipe
        raise Exception("Pipe not found")
    
    def determine_start(self) -> None:
        start = self.get_pipe_by_symbol("S")
        if start.up and start.down:
            start.symbol = "|"
        elif start.left and start.right:
            start.symbol = "-"
        elif start.up and start.right:
            start.symbol = "L"
        elif start.up and start.left:
            start.symbol = "J"
        elif start.down and start.right:
            start.symbol = "F"
        elif start.down and start.left:
            start.symbol = "7"
        else:
            raise Exception("Invalid start connections")
        self.start = start

    def find_main_cycle(self) -> Tuple[bool, list[Pipe]]:
        return self.start.test_for_cycle(self.pipes2D)
    
    def place_if_empty(self, xss: list[list], relative_to_pipe: Pipe, x: int, y: int) -> None:
        x += relative_to_pipe.x
        y += relative_to_pipe.y
        
        if x < 0 or x > self.width - 1:
            return
        if y < 0 or y > self.height - 1:
            return
            
        if xss[y][x] == " ":
            xss[y][x] = "I"
            
    def replicate_marked(self, xss: list[list], symbol: str = "I"):
        # Replicate 'symbol' in all directions until filled
        while True:
            added = 0
            for y in range(len(xss)):
                for x in range(len(xss[0])):
                    if xss[y][x] == symbol:
                        # up
                        if y > 0 and xss[y - 1][x] == " ":
                            xss[y - 1][x] = symbol
                            added += 1
                        # down
                        if y < len(xss) - 1 and xss[y + 1][x] == " ":
                            xss[y + 1][x] = symbol
                            added += 1
                        # left
                        if x > 0 and xss[y][x - 1] == " ":
                            xss[y][x - 1] = symbol
                            added += 1
                        # right
                        if x < len(xss[0]) - 1 and xss[y][x + 1] == " ":
                            xss[y][x + 1] = symbol
                            added += 1
            if added == 0:
                break
            
    def mark_to_the_right(self, xss: list[list], velocity: Tuple[int, int], relative_to_pipe: Pipe):
        # Mark spots to the right from the POV of the pipe
        if velocity == (0, 1):  # going down
            self.place_if_empty(xss, relative_to_pipe, -1, 0)
        if velocity == (0, -1): # going up
            self.place_if_empty(xss, relative_to_pipe, 1, 0)
        if velocity == (1, 0):  # going right
            self.place_if_empty(xss, relative_to_pipe, 0, 1)
        if velocity == (-1, 0): # going left
            self.place_if_empty(xss, relative_to_pipe, 0, -1)
    
    # Note: it is not guaranteed that this algorithm 
    #       will find the number of inner or outer spots.
    # 
    #       Whether it returns inner or outer count depends on the starting point.
    #       
    #       I decided it's good enough to manually check the outputed map
    #       and tweak the right-left handedness accordingly.
    #
    def get_inner_marked_2D(self, cycle = None) -> Tuple[int, list[list[str]]]:
        # Returns: count, 2D map
        
        if cycle:
            success, pipes = cycle
        else:
            success, pipes = self.find_main_cycle()
        if not success:
            raise Exception("Main cycle not found")
        
        # Fill with zeros
        cycle2D: list[list[str]] = []
        for y in range(self.height):
            cycle2D.append([])
            for _ in range(self.width):
                cycle2D[y].append(" ")
            
        # Mark the cycle
        for pipe in pipes:
            cycle2D[pipe.y][pipe.x] = pipe.symbol
        
        # Determine starting velocity
        if pipes[0].up == pipes[1]:
            velocity = (0, -1)
        elif pipes[0].right == pipes[1]:
            velocity = (1, 0)
        elif pipes[0].down == pipes[1]:
            velocity = (0, 1)
        elif pipes[0].left == pipes[1]:
            velocity = (-1, 0)
        else:
            raise Exception("Invalid start")
        
        for pipe in pipes:
            # Mark area to the right from pipe's POV
            self.mark_to_the_right(cycle2D, velocity, relative_to_pipe=pipe)
            
            # Update velocity
            match pipe.symbol, velocity:
                case "L", (c_x, c_y):
                    if c_x == -1:   # going left
                        velocity = (0, -1)
                    elif c_y == 1:  # going down
                        velocity = (1, 0)
                case "J", (c_x, c_y):
                    if c_x == 1:    # going right
                        velocity = (0, -1)
                    elif c_y == 1:  # going down
                        velocity = (-1, 0)
                case "7", (c_x, c_y):
                    if c_x == 1:    # going right
                        velocity = (0, 1)
                    elif c_y == -1: # going up
                        velocity = (-1, 0)
                case "F", (c_x, c_y):
                    if c_x == -1:   # going left
                        velocity = (0, 1)
                    elif c_y == -1:  # going up
                        velocity = (1, 0)
                        
            # Mark area to the right from pipe's POV (again after possibly changing the direction)
            self.mark_to_the_right(cycle2D, velocity, relative_to_pipe=pipe)
        
        # Replicate 'I's in all directions until filled
        self.replicate_marked(cycle2D, "I")
        
        # Count 'I's
        count = 0
        for line in cycle2D:
            for c in line:
                if c == "I":
                    count += 1
        return (count, cycle2D)
    
def print_map_2D(map2D: list[list[str]]) -> None:
    for row in map2D:
        for c in row:
            print(c, end="")
        print()

def main() -> None:
    lines = open("input.txt", "r").readlines()
    pipe_system = PipeSystem(lines)
    
    # Ex. 1
    print("Ex. 1")
    success, main_cycle = pipe_system.find_main_cycle()
    # print(main_cycle)
    furthest = int(len(main_cycle) / 2)
    print(furthest)
    
    # Ex. 2
    print("Ex. 2")
    count, marked_2D = pipe_system.get_inner_marked_2D((success, main_cycle))
    # print_map_2D(marked_2D)
    print(count)

if __name__ == "__main__":
    main()
    