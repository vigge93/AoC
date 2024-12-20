#!/bin/pypy3
import time
from typing import TypedDict
from argparse import ArgumentParser, BooleanOptionalAction
from itertools import combinations

day = 20
part_1_example_answer: int | None = 0
part_2_example_answer: int | None = 285


class DataDict(TypedDict):
    track: set[tuple[int, int]]
    start: tuple[int, int]
    end: tuple[int, int]

Data = DataDict


def part_1(data: Data):
    distances: dict[tuple[int, int], int] = {}
    current = data["start"]
    track_length = len(data["track"]) - 1
    i = 0
    while current != data["end"]:
        n = None
        for off in (-1, 1):
            c = (current[0] + off, current[1])
            if c in data["track"] and c not in distances:
                n = c
                break
            c = (current[0], current[1] + off)
            if c in data["track"] and c not in distances:
                n = c
                break
        distances[current] = track_length - i
        i += 1
        if not n:
            print("Error")
            break
        current = n
    distances[data["end"]] = 0
    s = 0
    for pos1, pos2 in combinations(data["track"], 2):
        if abs(pos1[0] - pos2[0]) > 2:
            continue
        if abs(pos1[1] - pos2[1]) > 2:
            continue
        if abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) != 2:
            continue
        if abs(distances[pos1] - distances[pos2]) < 102:
            continue
        s += 1
    return s

def part_1_and_2(data: Data):
    distances: dict[tuple[int, int], int] = {}
    current = data["start"]
    track_length = len(data["track"]) - 1
    i = 0
    while current != data["end"]:
        n = None
        for off in (-1, 1):
            c = (current[0] + off, current[1])
            if c in data["track"] and c not in distances:
                n = c
                break
            c = (current[0], current[1] + off)
            if c in data["track"] and c not in distances:
                n = c
                break
        distances[current] = track_length - i
        i += 1
        if not n:
            print("Error")
            break
        current = n
    distances[data["end"]] = 0
    s1 = 0
    s2 = 0
    for pos1, pos2 in combinations(data["track"], 2):
        if (dx := abs(pos1[0] - pos2[0])) > 20:
            continue
        if (dy := abs(pos1[1] - pos2[1])) > 20:
            continue
        if not 1 < (dist := dx + dy) <= 20:
            continue
        if dist == 2:
            if abs(distances[pos1] - distances[pos2]) >= 102:
                s1 += 1
        if abs(distances[pos1] - distances[pos2]) >= 100 + dist:
            s2 += 1
    return s1, s2


def parse_data(file: str):
    data: Data = {"track": set(), "start": (-1, -1), "end": (-1, -1)}
    with open(file, "r") as f:
        for y, line in enumerate(f):
            for x, p in enumerate(line.strip()):
                if p == "#":
                    continue
                if p == "S":
                    data["start"] = (x, y)
                elif p == "E":
                    data["end"] = (x, y)
                data["track"].add((x, y))
    return data


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--test", action=BooleanOptionalAction, default=False)
    
    args = parser.parse_args()
    
    if args.test:
        if part_1_example_answer is not None: # type: ignore
            data = parse_data(f"day{day}.xexample-1.txt")
            p1 = part_1(data)
            if p1 != part_1_example_answer:
                print(f"Wrong answer to part 1: answer: {p1}, expected: {part_1_example_answer}")
            else:
                print("Example part 1 passed!")
        if part_2_example_answer is not None: # type: ignore
            data = parse_data(f"day{day}.xexample-2.txt")
            p2 = part_2(data)
            if p2 != part_2_example_answer:
                print(f"Wrong answer to part 2: answer: {p2}, expected: {part_2_example_answer}")
            else:
                print("Example part 2 passed!")
    else:
        start_time = time.perf_counter_ns()
        data = parse_data(f"day{day}.txt")
        data_time = time.perf_counter_ns()
        p1, p2 = part_1_and_2(data)
        end_time = time.perf_counter_ns()
        print(
            f"""=== Day {day:02} ===\n"""
            f"""  · Loading data\n"""
            f"""  · Elapsed: {(data_time - start_time)/10**6:.3f} ms\n\n"""
            f"""  · Part 1: {p1}\n"""
            f"""  · Elapsed: 0 ms\n\n"""
            f"""  · Part 2: {p2}\n"""
            f"""  · Elapsed: {(end_time - data_time)/10**6:.3f} ms\n\n"""
            f"""  · Total elapsed: {(end_time - start_time)/10**6:.3f} ms"""
        )
