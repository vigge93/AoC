#!/bin/python
import time
from argparse import ArgumentParser, BooleanOptionalAction
from collections import defaultdict
from itertools import combinations
from math import gcd
from typing import TypedDict

day = 8
part_1_example_answer: int | None = 14
part_2_example_answer: int | None = 34


class DataDict(TypedDict):
    map: set[tuple[int, int]]
    frequencies: defaultdict[str, set[tuple[int, int]]]


Data = DataDict


def part_1(data: Data):
    frequencies = data["frequencies"]
    anti_nodes: set[tuple[int, int]] = set()

    for frequency in frequencies:
        for (x1, y1), (x2, y2) in combinations(frequencies[frequency], 2):
            diff_x, diff_y = (x2 - x1, y2 - y1)
            anti_node_1 = (x2 + diff_x, y2 + diff_y)
            anti_node_2 = (x1 - diff_x, y1 - diff_y)
            if anti_node_1 in data["map"]:
                anti_nodes.add(anti_node_1)
            if anti_node_2 in data["map"]:
                anti_nodes.add(anti_node_2)
    return len(anti_nodes)


def part_2(data: Data):
    frequencies = data["frequencies"]
    anti_nodes: set[tuple[int, int]] = set()

    for frequency in frequencies:
        for (x1, y1), (x2, y2) in combinations(frequencies[frequency], 2):
            diff_x, diff_y = (x2 - x1, y2 - y1)
            div = gcd(diff_x, diff_y)
            diff_x, diff_y = diff_x / div, diff_y / div
            anti_node_1 = (x2, y2)
            anti_node_2 = (x1, y1)
            while anti_node_1 in data["map"]:
                anti_nodes.add(anti_node_1)
                anti_node_1 = (anti_node_1[0] + diff_x, anti_node_1[1] + diff_y)
            while anti_node_2 in data["map"]:
                anti_nodes.add(anti_node_2)
                anti_node_2 = (anti_node_2[0] - diff_x, anti_node_2[1] - diff_y)

    return len(anti_nodes)


def parse_data(file: str):
    data: Data = {"frequencies": defaultdict(set), "map": set()}
    with open(file, "r") as f:
        for y, line in enumerate(f):
            for x, pos in enumerate(line.strip()):
                data["map"].add((x, y))
                if pos != ".":
                    data["frequencies"][pos].add((x, y))
    return data


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--test", action=BooleanOptionalAction, default=False)

    args = parser.parse_args()

    if args.test:
        if part_1_example_answer is not None:  # type: ignore
            data = parse_data(f"day{day}.xexample-1.txt")
            p1 = part_1(data)
            if p1 != part_1_example_answer:
                print(
                    f"Wrong answer to part 1: answer: {p1}, expected: {part_1_example_answer}"
                )
            else:
                print("Example part 1 passed!")
        if part_2_example_answer is not None:  # type: ignore
            data = parse_data(f"day{day}.xexample-2.txt")
            p2 = part_2(data)
            if p2 != part_2_example_answer:
                print(
                    f"Wrong answer to part 2: answer: {p2}, expected: {part_2_example_answer}"
                )
            else:
                print("Example part 2 passed!")
    else:
        start_time = time.perf_counter_ns()
        data = parse_data(f"day{day}.txt")
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
