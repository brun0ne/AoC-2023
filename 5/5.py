from abc import ABC, abstractmethod
from typing import TypedDict
from intervaltree import Interval, IntervalTree # type: ignore

DEBUG = False

class Entry:
    src_range: Interval
    dst_range: Interval
    
    class EntryRes(TypedDict):
        res: IntervalTree
        overlap: Interval
    
    def __init__(self, line: str) -> None:
        # parse
        dest_range_start, source_range_start, range_length = map(lambda x: int(x), line.split())
        self.src_range = Interval(source_range_start, source_range_start + range_length)
        self.dst_range = Interval(dest_range_start, dest_range_start + range_length)
        
    def get_values(self, r: Interval) -> EntryRes:
        overlap_size = self.src_range.overlap_size(r)
        overlap = Interval(max(self.src_range.begin, r.begin), min(self.src_range.end, r.end))
        
        if DEBUG:
            print(f"{self.src_range} {r} {overlap_size}")
        
        if overlap_size != 0:
            shift = overlap.begin - self.src_range.begin  
            return {
                "res": IntervalTree([Interval(self.dst_range.begin + shift, self.dst_range.begin + overlap_size + shift)]),
                "overlap": overlap
            }
        else:
            return {
                "res": IntervalTree(),
                "overlap": overlap
            }
        
    def __repr__(self) -> str:
        return (f"<src: {self.src_range[0]}-{self.src_range[-1]}, "
                f"dest: {self.dst_range[0]}-{self.dst_range[-1]}>")
                
class AMapping(ABC):
    name: str
    entries: list[Entry]
    
    @abstractmethod
    def _get_value(self, itree: IntervalTree) -> IntervalTree: pass
    
    def evaluate(self, nums: IntervalTree) -> IntervalTree:
        res = IntervalTree()
        for entry in self.entries:
            act_res = IntervalTree()
            mapped = IntervalTree()
            
            for num in nums:
                r = entry.get_values(num)
                act_res = act_res.union(self._get_value(r["res"]))
                
                if DEBUG:
                    print(f"{self.name} R", r)
                
                if r["overlap"].length() > 0:
                    mapped.add(r["overlap"])
                
            for a in mapped:
                nums.chop(a.begin, a.end)
                
            res = res.union(act_res)

        # leftover nums (they map to themselves as new keys)
        res = res.union(self._get_value(nums))
        res.merge_overlaps(strict=False)
        
        return res
    
    def parse(self, lines: list[str]) -> None:
        self.entries = []
        append: bool = False
        
        for line in lines:
            # start collecting
            if f"{self.name}" in line:
                append = True
                continue
            # skip
            if not append:
                continue
            # stop collecting
            if line.strip() == "":
                break 
            # parse an entry
            self.entries.append(Entry(line))

class Mapping(AMapping):
    maps_to: AMapping
    
    def __init__(self, maps_to: AMapping, name: str, lines: list[str]) -> None:
        self.entries = []
        self.maps_to = maps_to
        self.name = name
        
        self.parse(lines)
    
    def _get_value(self, itree: IntervalTree) -> IntervalTree:
        return self.maps_to.evaluate(itree)
    
class FinalMapping(AMapping):
    def __init__(self, name: str, lines: list[str]) -> None:
        self.entries = []
        self.name = name
        
        self.parse(lines)
        
    def _get_value(self, itree: IntervalTree) -> IntervalTree:
        return itree
    
def parse_seed_ranges(line: str) -> IntervalTree:
    nums = [*map(lambda x: int(x), line.split(":")[1].split())]
    
    def f(xs: list[int], acc: set[Interval]) -> set[Interval]:
        match xs:
            case [a, b, *rest]:
                return f(rest, {*acc, Interval(a, a+b)})
            case []:
                return acc
            case _:
                raise Exception("Invalid input: not even!")
    
    t = IntervalTree(list(f(nums, set())))
    t.merge_overlaps(strict=False)
    
    return t

def main() -> None:
    lines = open("input.txt", "r").readlines()
    
    # prepare data
    humidity_to_location = FinalMapping(name="humidity-to-location", lines=lines)
    temp_to_humidity = Mapping(maps_to=humidity_to_location, name="temperature-to-humidity", lines=lines)
    light_to_temperature = Mapping(maps_to=temp_to_humidity, name="light-to-temperature", lines=lines)
    water_to_light = Mapping(maps_to=light_to_temperature, name="water-to-light", lines=lines)
    fertilizer_to_water = Mapping(maps_to=water_to_light, name="fertilizer-to-water", lines=lines)
    soil_to_fertilizer = Mapping(maps_to=fertilizer_to_water, name="soil-to-fertilizer", lines=lines)
    seed_to_soil = Mapping(maps_to=soil_to_fertilizer, name="seed-to-soil", lines=lines)
    
    # ex. 1
    print("# Ex. 1")
    seed_point_intervals: IntervalTree = IntervalTree(map(lambda x: Interval(int(x), int(x)+1), lines[0].split(":")[1].split()))
    if DEBUG:
        print("Seeds: ", seed_point_intervals)
    
    location_intervals = seed_to_soil.evaluate(seed_point_intervals)
    min_location = min(map(lambda x: x.begin, location_intervals))
    print(min_location)
    
    # ex. 2
    print("# Ex. 2")
    
    seed_intervals: IntervalTree = parse_seed_ranges(lines[0])
    if DEBUG:
        print("Seeds: ", seed_intervals)
    
    location_intervals = seed_to_soil.evaluate(seed_intervals)
    if DEBUG:
        print(location_intervals)
    
    # find the min location
    min_location = min(map(lambda x: x.begin, location_intervals))
    print(min_location)

if __name__ == "__main__":
    main()
        