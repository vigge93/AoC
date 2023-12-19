import time
from dataclasses import dataclass
from itertools import batched

day = 5


@dataclass
class Mapping:
    source_start: int
    destination_start: int
    range: int

    @property
    def source_end(self):
        return self.source_start + self.range - 1

    def source_in_map(self, source: int):
        return source >= self.source_start and source < (self.source_start + self.range)

    def range_source_in_map(self, range_start, range_end):
        return self.source_start <= range_end and self.source_end >= range_start

    def map(self, source: int) -> int:
        return self.destination_start + (source - self.source_start)


class Pipeline:
    def __init__(self, wrapped_step=None):
        self.wrapped_step: Pipeline | None = wrapped_step
        self.mappings: list[Mapping] = []

    def add_mapping(self, source_start: int, destination_start: int, steps: int):
        self.mappings.append(Mapping(source_start, destination_start, steps))

    def map(self, seed):
        if self.wrapped_step is not None:
            seed = self.wrapped_step.map(seed)
        for mapping in self.mappings:
            if mapping.source_in_map(seed):
                return mapping.map(seed)
        return seed

    def map_range(self, range):
        if self.wrapped_step is not None:
            range = self.wrapped_step.map_range(range)
        ranges = []
        for start, steps in batched(range, 2):
            end = start + steps - 1
            split_ranges = [start, steps]
            for mapping in self.mappings:
                if not mapping.range_source_in_map(start, end):
                    continue
                new_split_ranges = []
                for range_start, range_step in batched(split_ranges, 2):
                    range_end = range_start + range_step - 1
                    if not mapping.range_source_in_map(range_start, range_end):
                        new_split_ranges += (range_start, range_step)
                    else:
                        map_start = range_start
                        map_end = range_end
                        if mapping.source_start > range_start:
                            new_split_ranges += (
                                range_start,
                                mapping.source_start - range_start,
                            )
                            map_start = mapping.source_start
                        if mapping.source_end < range_end:
                            new_split_ranges += (
                                mapping.source_end + 1,
                                range_end - mapping.source_end,
                            )
                            map_end = mapping.source_end
                        new_split_ranges += (map_start, map_end - map_start + 1)
                split_ranges = new_split_ranges
            ranges += split_ranges
        mapped_ranges = []
        for start, steps in batched(ranges, 2):
            for mapping in self.mappings:
                if mapping.source_in_map(start):
                    start = mapping.map(start)
                    break
            mapped_ranges += (start, steps)
        return mapped_ranges


def part_1(data: dict[str, list[int] | Pipeline]):
    min_location = 2**32
    pipeline: Pipeline = data["pipeline"]
    seeds: list[int] = data["seeds"]
    for seed in seeds:
        location = pipeline.map(seed)
        if location < min_location:
            min_location = location
    return min_location


def part_2(data):
    min_location = 2**32
    pipeline: Pipeline = data["pipeline"]
    seeds: list[int] = data["seeds"]
    for range in batched(seeds, 2):
        ranges = pipeline.map_range(range)
        for location, _ in batched(ranges, 2):
            if location < min_location:
                min_location = location
    return min_location


def parse_data():
    data = {}
    with open(f"day{day}.txt", "r") as f:
        seeds = f.readline().strip()
        _, seeds = seeds.split(":")
        seeds = [int(seed) for seed in seeds.split()]
        data["seeds"] = seeds
        prev_step = None
        for line in f:
            if not line.strip():
                continue
            if "to" in line:
                prev_step = Pipeline(prev_step)
            else:
                destination, source, steps = [int(n) for n in line.strip().split()]
                prev_step.add_mapping(source, destination, steps)
        data["pipeline"] = prev_step
    return data


if __name__ == "__main__":
    start_time = time.perf_counter_ns()
    data = parse_data()
    data_time = time.perf_counter_ns()
    p1 = part_1(data)
    p1_time = time.perf_counter_ns()
    p2 = part_2(data)
    end_time = time.perf_counter_ns()
    print(
        f"""=== Day {day:02} ===\n"""
        f"""  · Loading data\n"""
        f"""  · Elapsed: {(data_time - start_time)/10**6:.3f} ms\n\n"""
        f"""  · Part 1: {p1}\n"""
        f"""  · Elapsed: {(p1_time - data_time)/10**6:.3f} ms\n\n"""
        f"""  · Part 2: {p2}\n"""
        f"""  · Elapsed: {(end_time - p1_time)/10**6:.3f} ms\n\n"""
        f"""  · Total elapsed: {(end_time - start_time)/10**6:.3f} ms"""
    )
