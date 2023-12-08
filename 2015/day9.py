import time
from itertools import permutations, pairwise

day = 9


def part_1(data):
    locations = data["locations"]
    min_len = 10**6
    for path in permutations(locations):
        path_length = 0
        for road in pairwise(path):
            path_length += data["distances"][frozenset(road)]
        if path_length < min_len:
            min_len = path_length
    return min_len


def part_2(data):
    locations = data["locations"]
    max_len = -1
    for path in permutations(locations):
        path_length = 0
        for road in pairwise(path):
            path_length += data["distances"][frozenset(road)]
        if path_length > max_len:
            max_len = path_length
    return max_len


def parse_data():
    data = {"locations": set(), "distances": {}}
    with open(f"day{day}.txt", "r") as f:
        for line in f:
            line = line.strip()
            locations, distance = line.split(" = ")
            locations = locations.split(" to ")
            data["locations"] |= set(locations)
            data["distances"][frozenset(locations)] = int(distance)
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
