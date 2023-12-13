from typing import Tuple, TypeVar, Iterable
T = TypeVar('T')


class Map:
    array_2d: list[list[bool]]
    width: int
    height: int
    
    def __init__(self, lines: list[str]) -> None:
        self.array_2d = []
        
        # Assuming NxM grid
        self.width = len(lines[0])
        self.height = len(lines)
        
        # Parse
        for y in range(self.height):
            self.array_2d.append([])
            for x in range(self.width):
                if lines[y][x] == "#":
                    self.array_2d[y].append(True)
                else:
                    self.array_2d[y].append(False)
            
    def __repr__(self) -> str:
        res = ""
        for array_2d in [self.array_2d, transpose(self.array_2d)]:
            for row in array_2d:
                for c in row:
                    res += "#" if c else "."
                res += "\n"
            res += "\n"
        return res
    
    def find_mirror_axes(self) -> Tuple[Tuple[bool, float], Tuple[bool, float]]:
        x = self.find_mirrow_axis_y(transpose(self.array_2d))
        y = self.find_mirrow_axis_y(self.array_2d)

        return (x, y)
    
    def get_summary(self) -> int:
        (is_x, x), (is_y, y) = self.find_mirror_axes()
        
        if is_x and is_y:
            raise Exception("Both should not happen")

        if is_x:
            return int(x) + 1
        if is_y:
            return (int(y) + 1) * 100
        
        raise Exception("No axis found")
    
    @staticmethod
    def process_potential_range(start: int, end: int, array_2d: list[list[bool]], height: int) -> Tuple[bool, float]:
        upper: list[int] = []
        lower: list[int] = []
        
        for y_1 in range(height):
            for y_2 in range(height-1, y_1, -1):
                if y_1 < start or y_2 > end:
                    continue
                
                if y_1 == y_2:
                    continue
                
                if array_2d[y_1] == array_2d[y_2]:
                    if y_1 not in upper and y_2 not in lower:
                        upper.append(y_1)
                        lower.append(y_2)
        
        if start < 0 or end < 0:
            raise Exception("Start, end must be positive")
        
        if len(upper) != len(lower):
            raise Exception("Sanity check failed: different upper/lower lengths")

        if start != 0 and end != height - 1:
            raise Exception("Sanity check failed: invalid start/end pair")
        
        ## Determine if it's symmetrical
        # not empty
        if len(upper) == 0:
            return (False, 0)
        
        # upper must have slope = 1
        for i in range(len(upper) - 1):                     
            if (upper[i + 1] - upper[i]) != 1:
                return (False, 0)
        
        # lower must have slope = -1
        for i in range(len(lower) - 1):
            if (lower[i + 1] - lower[i]) != -1:
                return (False, 0)
        
        # check if something is missing in the middle
        if len(upper) != int((end - start) / 2) + 1:
            return (False, 0)
        
        # axis is at the midpoint
        return (True, (start + end) / 2)
    
    @staticmethod
    def find_mirrow_axis_y(array_2d: list[list[bool]]) -> Tuple[bool, float]:
        height = len(array_2d)
        upper: list[int] = []
        lower: list[int] = []
        
        # Get pair of identical rows and start/end of symmetry
        potential_ranges: list[Tuple[int, int]] = []
        
        for y_1 in range(height):
            for y_2 in range(height-1, y_1, -1):
                if y_1 == y_2:
                    continue
                
                if array_2d[y_1] == array_2d[y_2]:
                    if y_1 == 0 or y_2 == height - 1:
                        potential_ranges.append((y_1, y_2))

                    if y_1 not in upper and y_2 not in lower:
                        upper.append(y_1)
                        lower.append(y_2)

        # Process all potential start-end pairs
        for (start, end) in potential_ranges:
            success, axis = Map.process_potential_range(start, end, array_2d, height)
            if success:
                return (success, axis)

        # Nothing found
        return (False, 0)


def transpose(array_2d: list[list[T]]) -> list[list[T]]:
    return list(map(lambda x: list(x), zip(*array_2d)))


def main() -> None:
    lines = open("input.txt", "r").readlines()
    
    maps: list[Map] = []
    buffer: list[str] = []
    i = 0
    for line in lines:
        line = line.strip()
        
        if i == len(lines) - 1:
            buffer.append(line)
        
        if line == "" or i == len(lines) - 1:
            maps.append(Map(buffer))
            buffer = []
        else:
            buffer.append(line)
            
        i += 1
    
    # Ex. 1
    sum = 0
    for m in maps:
        sum += m.get_summary()
    print(sum)


if __name__ == "__main__":
    main()
    