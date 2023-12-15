from typing import Final

NUMBER_OF_BOXES = 256

class Entry:
    token: Final[str]
    
    hash: Final[int]
    label: Final[str]
    
    lens: Final[int | None]
    is_removal: Final[bool]
    
    def __init__(self, token: str) -> None:
        self.token = token
        
        self.label = self._label()
        self.hash = self._hash()
        
        self.is_removal = self._is_removal()
        
        if not self.is_removal:
            self.lens = self._lens()
    
    def _hash(self) -> int:
        curr = 0
        for c in self.label:
            curr += ord(c)
            curr = (curr * 17) % NUMBER_OF_BOXES
        
        return curr
    
    def _label(self) -> str:
        if "=" in self.token:
            return self.token.split("=")[0]
        elif "-" in self.token:
            return self.token.split("-")[0]
        raise Exception("Invalid token")
    
    def _lens(self) -> int:
        return int(self.token.split("=")[1])
    
    def _is_removal(self) -> bool:
        if "=" in self.token:
            return False
        if "-" in self.token:
            return True
        raise Exception("Invalid token")
    
    def __repr__(self) -> str:
        return f"[{self.label} {self.lens}]"
    
class Box:
    entries: list[Entry]
    
    def __init__(self) -> None:
        self.entries = []
        
    def process(self, entry: Entry) -> None:
        if not entry.is_removal:
            self.add(entry)
        else:
            self.remove(entry)
    
    def add(self, entry: Entry) -> None:
        found = False
        found_index: int
        
        for i, e in enumerate(self.entries, 0):
            if e.label == entry.label:
                found = True
                found_index = i
                break
            
        if found:
            self.entries[found_index] = entry
        else:
            self.entries.append(entry)
    
    def remove(self, entry: Entry) -> None:
        for e in self.entries:
            if e.label == entry.label:
                self.entries.remove(e)
                break
        else:
            pass
            # raise Exception("Entry to remove not found")
            
    def __repr__(self) -> str:
        return f"{self.entries}"

class HashMap:
    boxes: list[Box]
    
    def __init__(self, tokens: list[str]) -> None:
        self.boxes = [Box() for _ in range(NUMBER_OF_BOXES)]
        
        for token in tokens:
            entry = Entry(token)
            box_index = entry.hash
            self.boxes[box_index].process(entry)
        
    @property    
    def focusing_power(self) -> int:
        power = 0
        
        for box_i, box in enumerate(self.boxes):
            for entry_i, entry in enumerate(box.entries):
                if not entry.lens:
                    raise Exception("Invalid entry")
                
                power += (box_i + 1) * (entry_i + 1) * entry.lens
            
        return power
    
    def __repr__(self) -> str:
        s = ""
        for i, box in enumerate(self.boxes):
            s += f"Box {i}: {box}\n"
        return s

def main() -> None:
    tokens = open("input.txt", "r").read().strip().split(",")
    
    # Ex. 1
    print("Ex. 1")
    
    s = 0
    for token in tokens:
        curr = 0
        for c in token:
            curr += ord(c)
            curr = (curr * 17) % 256
        s += curr
    print(s)
    
    # Ex. 2
    print("Ex. 2")
    
    hash_map = HashMap(tokens)
    # print(hash_map)
    print(hash_map.focusing_power)

if __name__ == "__main__":
    main()
    