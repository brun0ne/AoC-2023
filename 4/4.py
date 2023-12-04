class Card:
    id: int
    winning: list[int]
    numbers: list[int]
    
    def __init__(self, line: str) -> None:
        title, rest = line.split(":")
        
        # ID
        self.id = int(title.split()[1])

        # Numbers
        self.winning, self.numbers = [*map(lambda x: [*map(lambda y: int(y), x.split())], rest.split("|"))]
        
    def count_winning(self) -> int:
        count = 0
        for n in self.numbers:
            if n in self.winning:
                count += 1
        return count
    
    def get_points(self) -> int:
        c_win = self.count_winning()
        if c_win > 0:
            return 2 ** (c_win - 1)
        else:
            return 0

def process_cards(cards: list[Card]) -> int:
    instances = 0
    to_process: list[int] = [card.id for card in cards]
    
    while len(to_process) > 0:
        instances += 1
        card = cards[to_process.pop()-1]
        won = card.count_winning()
        for i in range(card.id + 1, card.id + won + 1):
            if i <= len(cards):
                to_process.append(i)
            else:
                raise Exception("Err")

    return instances
    

def main() -> None:
    lines = open("input.txt").readlines()
    cards: list[Card] = []
    for line in lines:
        cards.append(Card(line))
        
    # Ex. 1
    sum_of_points: int = 0
    for card in cards:
        sum_of_points += card.get_points()
    print(sum_of_points)
    
    # Ex. 2
    print(process_cards(cards))
    
if __name__ == "__main__":
    main()
    