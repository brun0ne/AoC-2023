import math
from itertools import cycle

class BinaryNode:
    val: str
    left: str
    right: str
    
    def __init__(self, line: str) -> None:
        # Parse
        lhs, rhs = line.split("=")
        self.val = lhs.strip()
        
        self.left, self.right = map(
            lambda x: x.replace(")", "").replace("(", "").strip(),
            rhs.split(",")
        )
        
    def try_link(self, nodes) -> None:
        linked = 0
        for node in nodes:
            if node.val == self.right:
                self.right_link = node
                linked += 1
            if node.val == self.left:
                self.left_link = node
                linked += 1
        if linked != 2:
            raise Exception("Node not found")

    @property
    def is_ghost_start(self) -> bool:
        return self.val.endswith("A")
    
    @property
    def is_ghost_end(self) -> bool:
        return self.val.endswith("Z")
        
    def __repr__(self) -> str:
        return f"<{self.val}: {self.left}, {self.right}>"

class BinaryGraph:
    nodes: list[BinaryNode]
    
    def __init__(self, lines: list[str]) -> None:
        self.nodes = []
        
        # Parse
        for line in lines:
            node = BinaryNode(line)
            self.nodes.append(node)
        
        # Link
        for node in self.nodes:
            node.try_link(self.nodes)
            
    def get(self, val: str) -> BinaryNode:
        for node in self.nodes:
            if node.val == val:
                return node
        raise Exception("Node not found")
    
    @property
    def hd(self) -> BinaryNode:
        for node in self.nodes:
            if node.val == "AAA":
                return node
        raise Exception("Start node not found")
    
    def count_steps_to(self, dest_val: str, steps: str) -> int:
        ptr = self.hd
        count = 0
        
        for step in cycle(steps):
            # End condition
            if ptr.val == dest_val:
                return count
            
            # Follow links
            if step == 'L':
                ptr = ptr.left_link
            elif step == 'R':
                ptr = ptr.right_link
            else:
                raise Exception("Invalid step")
            
            # Increment count
            count += 1
            
        raise Exception("Unreachable code")
    
    def count_ghost_steps(self, steps: str) -> int:
        # Assemble starting points
        ptrs: list[BinaryNode] = []
        for node in self.nodes:
            if node.is_ghost_start:
                ptrs.append(node)
                
        # Go
        needed_steps: list[int] = []
        count = 0
        for step in cycle(steps):
            for ptr in ptrs:
                if ptr.is_ghost_end:
                    # Append
                    needed_steps.append(count)
                    # Remove ptr (found)
                    ptrs.remove(ptr)
            
            if len(ptrs) == 0:
                # The result is their lowest common multiple
                return math.lcm(*needed_steps)
            
            for i in range(0, len(ptrs)):
                if step == 'L':
                    ptrs[i] = ptrs[i].left_link
                elif step == 'R':
                    ptrs[i] = ptrs[i].right_link
                else:
                    raise Exception("Invalid step")
            
            # Increment count
            count += 1
            
        raise Exception("Unreachable code")

def main() -> None:
    lines = open("input.txt", "r").readlines()
    graph = BinaryGraph(lines[2:])
    steps = lines[0].strip()
    
    # Ex. 1
    print("Ex. 1")
    count = graph.count_steps_to("ZZZ", steps)
    print(count)
    
    # Ex. 2
    print("Ex. 2")
    count = graph.count_ghost_steps(steps)
    print(count)

if __name__ == "__main__":
    main()
    