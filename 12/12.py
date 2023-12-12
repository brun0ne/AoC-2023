from typing import Tuple, Iterable
from itertools import chain, combinations
from functools import reduce

# Combinations of all possible lengths
def powerset(iterable: Iterable) -> Iterable:
    s = list(set(iterable))
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

# Get list of indexes where 'symbol' is
def find_symbol(record: list[str], symbol: str) -> list[int]:
    res = []
    for i in range(len(record)):
        if record[i] == symbol:
            res.append(i)
    return res

# Count symbol
def count_symbol(record: list[str], symbol: str) -> int:
    return reduce(lambda acc, x: acc + 1 if x == symbol else acc, record, 0)

# Produce one possible solution considering some indexes blocked
def produce_one_possible(record: list[str], groups: list[int], undefined_idx: list[int],
                         populated_count: int, to_populate: int, blocked_idx: list[int]) -> Tuple[bool, list[int]]:
    indexes = []
    for index in undefined_idx:
        if index not in blocked_idx:
            indexes.append(index)
            populated_count += 1
        if populated_count >= to_populate:
            break

    # Verify groups
    check_groups = []
    check_curr = 0
    for i in range(len(record)):
        if record[i] == "#" or i in indexes:
            check_curr += 1
        elif check_curr > 0:
            check_groups.append(check_curr)
            check_curr = 0
    
    # Flush at the end
    if check_curr > 0:
        check_groups.append(check_curr)
    
    return (check_groups == groups, indexes)

def main() -> None:
    lines = open("input.txt", "r").readlines()
    
    sum = 0
    
    for line in lines:
        line = line.strip()
        record_str, groups_str = line.split()
        
        # Parse data
        groups = list(map(lambda x: int(x), groups_str.split(",")))
        record = list(record_str)
        # print(record, groups)
        
        # Ex. 1
        undefined: list[int] = find_symbol(record, "?")
        populated_count = count_symbol(record, "#")
        to_populate = reduce(lambda acc, x: acc + x, groups, 0)
    
        blocked_combinations: Iterable[list[int]] = powerset(undefined)
        successful: list[Tuple[int, ...]] = []
        
        for combination in blocked_combinations:
            success, indexes = produce_one_possible(record, groups, undefined, populated_count, to_populate, combination)
            # print(combination, success, indexes)
            if success:
                successful.append(tuple(indexes))
        
        sum += len(set(successful))
    
    print(sum)

if __name__ == "__main__":
    main()
    