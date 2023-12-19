import time
from functools import cache
from multiprocessing import Pool

day = 12


@cache
def recurse_memoize(springs, schematic) -> int:
    if not schematic:
        return not any(map(lambda s: "#" in s, springs))
    next_schematic = schematic[0]
    s = 0
    prev_s = "."
    break_all = False
    # Find empty spot for next spring:
    for springIdx, spring in enumerate(springs):
        if break_all:
            break
        spring_len = len(spring)
        if spring_len < next_schematic:
            if "#" in spring:
                break
            continue
        for subSpringIdx in range(spring_len):
            if (spring_len - subSpringIdx) < next_schematic:
                prev_s = spring[subSpringIdx]
                break
            if prev_s == "#":
                break_all = True
                break
            if any(map(lambda s: "#" in s, springs[:springIdx])):
                break_all = True
                break
            if (spring_len - subSpringIdx) >= next_schematic + 1 and spring[
                subSpringIdx + next_schematic
            ] == "#":
                prev_s = spring[subSpringIdx]
                continue
            prev_s = spring[subSpringIdx]
            new_springs = (
                springs[springIdx][subSpringIdx + next_schematic + 1 :],
                *springs[springIdx + 1 :],
            )
            s += recurse_memoize(new_springs, schematic[1:])
    return s


def part_1(data):
    s = 0
    for springs, schematic in data["part1"]:
        s += recurse_memoize(springs, schematic)
    return s


def part_2(data):
    with Pool() as p:
        sums = p.starmap(recurse_memoize, data["part2"])
    return sum(sums)


def parse_data():
    data = {"part1": [], "part2": []}
    with open(f"day{day}.txt", "r") as f:
        for line in f:
            springs_1, schematic_1 = line.strip().split()
            springs_2 = "?".join([springs_1] * 5)
            schematic_2 = ",".join([schematic_1] * 5)
            schematic_1 = tuple([int(n) for n in schematic_1.split(",")])
            springs_1 = springs_1.strip().strip(".").split(".")
            schematic_2 = tuple([int(n) for n in schematic_2.split(",")])
            springs_2 = springs_2.strip().strip(".").split(".")
            data["part1"].append(
                (tuple([spring for spring in springs_1 if spring]), schematic_1)
            )
            data["part2"].append(
                (tuple([spring for spring in springs_2 if spring]), schematic_2)
            )
    return data


if __name__ == "__main__":
    start_time = time.perf_counter_ns()
    data = parse_data()
    data_time = time.perf_counter_ns()
    p1 = part_1(data)
    p1_time = time.perf_counter_ns()
    p2 = part_2(data)
    end_time = time.perf_counter_ns()
    print(recurse_memoize.cache_info())
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
