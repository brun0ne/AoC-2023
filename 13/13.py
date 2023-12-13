from typing import Optional, Tuple, TypeVar
T = TypeVar('T')

class Map:
    array_2d: list[list[bool]]
    width: int
    height: int
    
    EndpointList = list[Tuple[int, int]]
    
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
    
    def find_mirror_axes(self, blocked_endpoints_x: EndpointList,
                         blocked_endpoints_y: EndpointList) -> Tuple[Optional[Tuple[float, Tuple[int, int]]], ...]:
        
        x = self.find_mirror_axis_y(transpose(self.array_2d), blocked_endpoints_x)
        y = self.find_mirror_axis_y(self.array_2d, blocked_endpoints_y)

        return (x, y)
    
    def get_summary(self, blocked_endpoints_x: EndpointList | None = None, blocked_endpoints_y: EndpointList | None = None) -> Tuple[bool, int]:
        if not blocked_endpoints_x:
            blocked_endpoints_x = []
        if not blocked_endpoints_y:
            blocked_endpoints_y = []
        
        x, y = self.find_mirror_axes(blocked_endpoints_x, blocked_endpoints_y)
        
        if x and y:
            return (False, 0) # Both are invalid

        if x:
            offset, e = x
            if e in blocked_endpoints_x:
                raise Exception("Invalid X", e)
            return (True, int(offset) + 1)
        if y:
            offset, e = y
            if e in blocked_endpoints_y:
                raise Exception("Invalid Y", e)
            return (True, (int(offset) + 1) * 100)
        
        return (False, 0)
    
    def get_with_smudge_fixed(self) -> int:
        # get endpoints of the current axis
        axis_x, axis_y = self.find_mirror_axes([], [])
        if axis_x:
            _, endpoints_x = axis_x
            endpoints_y = None
        elif axis_y:
            endpoints_x = None
            _, endpoints_y = axis_y
        else:
            raise Exception("Both or none: not be valid")
        
        for y in range(self.height):
            for x in range(self.width):
                # remember old value
                old = self.array_2d[y][x]
                
                # flip
                self.array_2d[y][x] = not self.array_2d[y][x]
                
                # calculate
                success, num = self.get_summary([endpoints_x] if endpoints_x else [], [endpoints_y] if endpoints_y else [])
                
                # revert
                self.array_2d[y][x] = old
                
                # return
                if success:
                    return num
                
        raise Exception("No smudge found")
    
    @staticmethod
    def process_potential_range(start: int, end: int, array_2d: list[list[bool]], height: int) -> Optional[Tuple[float, Tuple[int, int]]]:
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
            return None
        
        # upper must have slope = 1
        for i in range(len(upper) - 1):                     
            if (upper[i + 1] - upper[i]) != 1:
                return None
        
        # lower must have slope = -1
        for i in range(len(lower) - 1):
            if (lower[i + 1] - lower[i]) != -1:
                return None
        
        # check if something is missing in the middle
        if len(upper) != int((end - start) / 2) + 1:
            return None
        
        # evenness check
        if (start + end) % 2 == 0:
            return None
        
        # axis is at the midpoint
        return ((start + end) / 2, (start, end))
    
    @staticmethod
    def find_mirror_axis_y(array_2d: list[list[bool]], blocked_endpoints: EndpointList) -> Optional[Tuple[float, Tuple[int, int]]]:
        height = len(array_2d)
        
        # Get pair of identical rows and start/end of symmetry
        potential_ranges: list[Tuple[int, int]] = []
        
        for y_1 in range(height):
            for y_2 in range(height-1, y_1, -1):
                if y_1 == y_2:
                    continue
                
                if array_2d[y_1] == array_2d[y_2]:
                    if (y_1 == 0 or y_2 == height - 1) and (y_1, y_2) not in blocked_endpoints:
                        potential_ranges.append((y_1, y_2))

        # Process all potential start-end pairs
        for (start, end) in potential_ranges:
            res = Map.process_potential_range(start, end, array_2d, height)
            if res:
                axis, endpoints = res
                return (axis, endpoints)

        # Nothing found
        return None


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
    print("Ex. 1")
    sum = 0
    for m in maps:
        _, num = m.get_summary()
        sum += num
    print(sum)
    
    # Ex. 2
    print("Ex. 2")
    sum = 0
    for m in maps:
        num = m.get_with_smudge_fixed()
        sum += num
    print(sum)

if __name__ == "__main__":
    main()
    
