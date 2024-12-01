import time
from typing import TypedDict
from argparse import ArgumentParser, BooleanOptionalAction
from collections import Counter

day = 1
part_1_example_answer: int | None = 11
part_2_example_answer: int | None = 31


class DataDict(TypedDict):
    x: list[int]
    y: list[int]
type Data = DataDict


def part_1(data: Data):
    s = 0
    x_lst = sorted(data["x"])
    y_lst = sorted(data["y"])
    for x, y in zip(x_lst, y_lst):
        s += abs(x - y)
    return s


def part_2(data: Data):
    x_lst = data["x"]
    y_lst = data["y"]
    y_cnt = Counter(y_lst)
    s = 0
    for number in x_lst:
        s += number*y_cnt[number]
    return s


def parse_data(file: str):
    data: Data = {}
    x_lst = []
    y_lst = []
    with open(file, "r") as f:
        for line in f:
            x, y = line.strip().split()
            x_lst.append(int(x))
            y_lst.append(int(y))
    data["x"] = x_lst
    data["y"] = y_lst
    return data


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--test", action=BooleanOptionalAction, default=False)
    
    args = parser.parse_args()
    
    if args.test:
        if part_1_example_answer is not None:
            data = parse_data(f"day{day}.xexample-1.txt")
            p1 = part_1(data)
            if p1 != part_1_example_answer:
                print(f"Wrong answer to part 1: answer: {p1}, expected: {part_1_example_answer}")
            else:
                print("Example part 1 passed!")
        if part_2_example_answer is not None:
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
