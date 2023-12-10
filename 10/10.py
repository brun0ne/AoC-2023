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
                
    def test_for_cycle(self, pipes2D: list[list], coming_from: Tuple[int, int] = (0, 0), start_symbol = "", acc: list = []) -> Tuple[bool, list]:
        if coming_from == (0, 0):
            start_symbol = self.symbol
        
        match coming_from:
            case n if n != (0, 0) and self.symbol == start_symbol:
                return (True, acc)
            case _:
                if self.up and n != (0, 1):
                    c, path = self.up.test_for_cycle(pipes2D, (0, -1), start_symbol, acc + [self])
                    if c: return (c, path)
                if self.down and n != (0, -1):
                    c, path = self.down.test_for_cycle(pipes2D, (0, 1), start_symbol, acc + [self])
                    if c: return (c, path)
                if self.right and n != (1, 0):
                    c, path = self.right.test_for_cycle(pipes2D, (-1, 0), start_symbol, acc + [self])
                    if c: return (c, path)
                if self.left and n != (-1, 0):
                    c, path = self.left.test_for_cycle(pipes2D, (1, 0), start_symbol, acc + [self])
                    if c: return (c, path)
        return (False, [])

class PipeSystem:
    pipes2D: list[list[Pipe]]
    
    def __init__(self, lines: list[str]) -> None:
        self.pipes2D: list[list[Pipe]] = []
        
        # Parse
        for y in range(len(lines)):
            self.pipes2D.append([])
            for x in range(len(lines[0])):
                self.pipes2D[-1].append(Pipe(lines, x, y))
        
        # Connect
        for pipe in itertools.chain(*self.pipes2D):
            pipe.try_connect(self.pipes2D)
            
    def get_pipe_by_symbol(self, symbol: str) -> Pipe:
        for pipe in itertools.chain(*self.pipes2D):
            if pipe.symbol == symbol:
                return pipe
        raise Exception("Pipe not found")

    def find_main_cycle(self) -> Tuple[bool, list[Pipe]]:
        start = self.get_pipe_by_symbol("S")
        return start.test_for_cycle(self.pipes2D)

def main() -> None:
    lines = open("input.txt", "r").readlines()
    pipe_system = PipeSystem(lines)
    
    # Ex. 1
    success, main_cycle = pipe_system.find_main_cycle()
    # print(success, main_cycle)
    furthest = int(len(main_cycle) / 2)
    print(furthest)

if __name__ == "__main__":
    main()
    