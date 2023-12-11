from functools import reduce

class Galaxy:
    x: int
    y: int
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"<{self.x}, {self.y}>"
    
    def __eq__(self, __value) -> bool:
        if not __value:
            return False
        return self.x == __value.x and self.y == __value.y
        
class GalaxySystem:
    galaxies: list[Galaxy]
    
    def __init__(self, lines: list[str], stretch_mult: int = 2) -> None:
        self.galaxies = []
        stretch_mult -= 1   # convert to added amount
        
        # Strip lines
        lines = list(map(lambda x: x.strip(), lines))
        
        # Stretch
        stretch_list_y = self.get_stretch_coords(lines)
        stretch_list_x = self.get_stretch_coords(transpose(lines))
        
        # Parse
        translated_y = 0
        for y in range(len(lines)):
            translated_x = 0
            for x in range(len(lines[y])):
                # Sanity check
                if (x in stretch_list_x or y in stretch_list_y) and lines[y][x] == "#":
                    raise Exception(f"Invalid stretch list: error on coordinate ({x}, {y})")
                
                # Append galaxy
                if lines[y][x] == "#":
                    self.galaxies.append(Galaxy(translated_x, translated_y))
                # Stretch
                if x in stretch_list_x:
                    translated_x += stretch_mult
                # Increment
                translated_x += 1
                
            # Stretch
            if y in stretch_list_y:
                translated_y += stretch_mult
            # Increment
            translated_y += 1
    
    def find_all_distances(self) -> list[int]:
        res: list[int] = []
        for i in range(len(self.galaxies)):
            for g2 in self.galaxies[i:]:
                g1 = self.galaxies[i]
                if g1 == g2:
                    continue
                res.append(self.distance_between(g1, g2))
        return res
    
    def print(self) -> None:
        res: list[list[str]] = []
        
        max_x = reduce(lambda acc, galaxy: max(acc, galaxy.x), self.galaxies, 0)
        max_y = reduce(lambda acc, galaxy: max(acc, galaxy.y), self.galaxies, 0)
        
        for y in range(max_y + 1):
            res.append(["."] * (max_x + 1))
        
        for galaxy in self.galaxies:
            res[galaxy.y][galaxy.x] = "#"
        
        for line in res:
            for c in line:
                print(c, end="")
            print()
    
    @staticmethod
    def distance_between(g1: Galaxy, g2: Galaxy) -> int:
        return abs(g1.x - g2.x) + abs(g1.y - g2.y)
    
    @staticmethod
    def is_empty(row: str) -> bool:
        for c in row:
            if c != ".":
                return False
        return True
    
    @staticmethod
    def get_stretch_coords(lines: list[str]) -> list[int]:
        # Return coordinates of "empty" rows
        res: list[int] = []
        i = 0
        for row in lines:
            if GalaxySystem.is_empty(row):
                res.append(i)
            i += 1
        return res

def transpose(xss: list[str]) -> list:
    return list(map(lambda x: list(x), zip(*xss)))

def main() -> None:
    lines = open("input.txt", "r").readlines()
    
    # Ex. 1
    print("Ex. 1")
    galaxy_system = GalaxySystem(lines)
    distances = galaxy_system.find_all_distances()
    print(reduce(lambda acc, x: acc+x, distances, 0))
    
    # Ex. 2
    print("Ex. 2")
    galaxy_system = GalaxySystem(lines, stretch_mult=1000000)
    distances = galaxy_system.find_all_distances()
    print(reduce(lambda acc, x: acc+x, distances, 0))

if __name__ == "__main__":
    main()
    