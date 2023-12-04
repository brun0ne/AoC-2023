from typing import Tuple

class Game:
    id: int
    
    red: int
    green: int
    blue: int
    
    red_sets: list[int]
    green_sets: list[int]
    blue_sets: list[int]

    def __init__(self, line: str) -> None:
        # set initial values
        self.red = 0
        self.green = 0
        self.blue = 0
        
        self.red_sets = []
        self.green_sets = []
        self.blue_sets = []
        
        # [[Example]] Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        
        # split
        title, rounds_str = line.split(":")
        
        # get id
        self.id = int(title.split(" ")[1])
        
        # get rounds
        rounds = rounds_str.split(";")
        
        # for each round add up colors
        for round in rounds:
            if "," in round:
                turns = round.split(",")
            else:
                turns = [round]

            for turn in turns:
                if turn == ' ' or turn == '':
                    continue
                amount_str, color = turn.strip().split(" ")
                amount = int(amount_str)
                
                if color == "red":
                    self.red += amount
                    self.red_sets.append(amount)
                elif color == "green":
                    self.green += amount
                    self.green_sets.append(amount)
                elif color == "blue":
                    self.blue += amount
                    self.blue_sets.append(amount)
    
    def check_if_possible(self, red: int, green: int, blue: int) -> bool:
        for rset in self.red_sets:
            if rset > red:
                return False
        for gset in self.green_sets:
            if gset > green:
                return False
        for bset in self.blue_sets:
            if bset > blue:
                return False
        return True
    
    def min_to_be_possible(self) -> Tuple[int, int, int]:
        max_red = self.red_sets[0]
        max_green = self.green_sets[0]
        max_blue = self.blue_sets[0]
        
        for rset in self.red_sets[1:]:
            if rset > max_red:
                max_red = rset
        for gset in self.green_sets[1:]:
            if gset > max_green:
                max_green = gset
        for bset in self.blue_sets[1:]:
            if bset > max_blue:
                max_blue = bset
        
        return (max_red, max_green, max_blue)
    
    def power(self) -> int:
        r, g, b = self.min_to_be_possible()
        return r*g*b
                    
    def __str__(self) -> str:
        return f"{self.id}: R{self.red_sets} G{self.green_sets} B{self.blue_sets}"
        
def main() -> None:
    lines = open("input.txt", "r").readlines()
    games: list[Game] = []
    
    for line in lines:
        game = Game(line)
        games.append(game)
        
    # Ex. 1
    sum_of_ids = 0
    for game in games:
        if game.check_if_possible(red=12, green=13, blue=14):
            sum_of_ids += game.id
    print(sum_of_ids)
    
    # Ex. 2
    sum_of_powers = 0
    for game in games:
        sum_of_powers += game.power()
    print(sum_of_powers)

if __name__ == "__main__":
    main()
