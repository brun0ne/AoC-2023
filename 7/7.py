class Hand:
    cards: str
    points: int
    with_joker_rule: bool
    
    card_values = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
    
    def __init__(self, line: str, with_joker: bool = False) -> None:
        # Parse
        cards, points = line.split()
        self.cards = cards
        self.points = int(points)
        self.with_joker_rule = with_joker

    def __repr__(self) -> str:
        return f"{self.cards} | {self.points}"
    
    def get_counts(self) -> list[int]:
        card_dict: dict[str, int] = {}
        for c in self.cards:
            if not c in card_dict.keys():
                card_dict[c] = 0
            card_dict[c] += 1
        
        if self.with_joker_rule and 'J' in card_dict.keys():
            # grab and zero out jokers
            jokers = card_dict['J']
            card_dict['J'] = 0
            
            # add them to the most couted card
            s = sorted(card_dict.values(), reverse=True)
            s[0] += jokers
            
            return s
        
        # without joker rule
        return sorted(card_dict.values(), reverse=True)
    
    def type(self) -> int:
        match self.get_counts():
            case [a, *_] if a == 5:
                return 6
            case [a, b, *_] if a == 4 and b == 1:
                return 5
            case [a, b, *_] if a == 3 and b == 2:
                return 4
            case [a, b, *_] if a == 3 and b == 1:
                return 3
            case [a, b, *_] if a == 2 and b == 2:
                return 2
            case [a, b, *_] if a == 2 and b == 1:
                return 1
            case [a, _, *_] if a == 1:
                return 0
        raise Exception("Something went wrong")
    
    def beats(self, c1: str, c2: str) -> bool:
        if self.with_joker_rule:
            # loses with everything
            if c1 == "J":
                return False
            if c2 == "J":
                return True
        
        if c1 in Hand.card_values:
            val1 = Hand.card_values[c1]
        else:
            val1 = int(c1)
        
        if c2 in Hand.card_values:
            val2 = Hand.card_values[c2]
        else:
            val2 = int(c2)
        
        return val1 > val2
    
    def __lt__(self, other) -> bool:
        s_type = self.type()
        o_type = other.type()
        
        if s_type < o_type:
            return True
        elif s_type > o_type:
            return False
        else:
            def f(s_cards: list[str], o_cards: list[str]) -> bool:
                match s_cards, o_cards:
                    case [s, *s_rest], [o, *o_rest]:
                        if self.beats(o, s):
                            return True
                        elif self.beats(s, o):
                            return False
                        else:
                            return f(s_rest, o_rest)
                    case [], []:
                        raise Exception("Equal hands")
                raise Exception("Invalid input")
            
            return f(list(self.cards), list(other.cards))

def get_sum_of_points(hands: list[Hand]) -> int:
    ranked = sorted(hands) # from worst to best
    
    sum = 0
    i = 1
    for hand in ranked:
        sum += hand.points * i
        i += 1
    
    return sum

def main() -> None:
    lines = open("input.txt", "r").readlines()
    
    # Ex. 1
    print("Ex. 1")
    hands: list[Hand] = []
    for line in lines:
        hands.append(Hand(line))
    print(get_sum_of_points(hands))
    
    # Ex. 2
    print("Ex. 2")
    for hand in hands:
        hand.with_joker_rule = True
    print(get_sum_of_points(hands))

if __name__ == "__main__":
    main()
    