#!../venv/bin/python
import time
from argparse import ArgumentParser, BooleanOptionalAction
from typing import TypedDict

day = 5
part_1_example_answer: int | None = 3
part_2_example_answer: int | None = 16


class DataDict(TypedDict):
    fresh: list[tuple[int, int]]
    ingredients: list[int]


Data = DataDict


def part_1(data: Data):
    s = 0
    for ingredient in data["ingredients"]:
        for start, end in data["fresh"]:
            if start <= ingredient <= end:
                s += 1
                break
    return s


def part_2(data: Data):
    ranges: list[tuple[int, int]] = []
    new_fresh = data["fresh"]
    combined = True
    while combined:
        combined = False
        for start, end in new_fresh:
            for idx, (r_start, r_end) in enumerate(ranges):
                if start <= r_start and end >= r_end:
                    ranges[idx] = (start, end)
                    combined = True
                    break
                if r_start <= start <= r_end + 1 or r_start - 1 <= end <= r_end:
                    ranges[idx] = (min(start, r_start), max(r_end, end))
                    combined = True
                    break
            else:
                ranges.append((start, end))

        new_fresh = ranges
        ranges = []
    s = 0
    for start, end in new_fresh:
        s += end - start + 1
    return s


def parse_data(file: str):
    data: Data = {
        "fresh": [],
        "ingredients": [],
    }
    fresh = True
    with open(file, "r") as f:
        for line in f:
            if not line.strip():
                fresh = False
                continue
            if fresh:
                start, end = line.strip().split("-")
                data["fresh"].append((int(start), int(end)))
            else:
                data["ingredients"].append(int(line))
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
