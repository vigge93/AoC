#!/bin/python
import time
from typing import TypedDict
from argparse import ArgumentParser, BooleanOptionalAction
from collections import defaultdict

day = 5
part_1_example_answer: int | None = 143
part_2_example_answer: int | None = 123


class DataDict(TypedDict):
    orders: defaultdict[int, set[int]]
    manuals: list[list[int]]
type Data = DataDict


def part_1(data: Data):
    s = 0
    orders = data["orders"]
    manuals = data["manuals"]
    for manual in manuals:
        correct = True
        printed_pages: set[int] = set()
        for page in manual:
            order = orders[page]
            if order & printed_pages:
                correct = False
                break
            printed_pages.add(page)
        if correct:
            s += manual[(len(manual) - 1) // 2]
    return s


def part_2(data: Data):
    s = 0
    orders = data["orders"]
    manuals = data["manuals"]
    for manual in manuals:
        correct = True
        new_order: list[int] = []
        printed_pages: set[int] = set()
        for page in manual:
            order = orders[page]
            if (wrong_pages := order & printed_pages):
                correct = False
                min_index = min([new_order.index(x) for x in wrong_pages])
                new_order.insert(min_index, page)
            else:
                new_order.append(page)
            printed_pages.add(page)
        if not correct:
            s += new_order[(len(new_order) - 1) // 2]

    return s


def parse_data(file: str):
    data: Data = {"orders": defaultdict(set), "manuals": []}
    ordering = True
    with open(file, "r") as f:
        for line in f:
            if line.strip() == "":
                ordering = False
                continue
            if ordering:
                first, second = line.strip().split("|")
                data["orders"][int(first)].add(int(second))
            else:
                data["manuals"].append([int(x) for x in line.strip().split(",")])
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
