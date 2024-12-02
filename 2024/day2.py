import time
from typing import TypedDict
from argparse import ArgumentParser, BooleanOptionalAction
from itertools import pairwise, combinations


day = 2
part_1_example_answer: int | None = 2
part_2_example_answer: int | None = 4


class DataDict(TypedDict):
    pass
type Data = list # DataDict


def check_if_safe(report: list[int]):
    increasing = None
    safe = True
    for prev, cur in pairwise(report):
        if not (1 <= abs(prev - cur) <= 3):
            safe = False
            break
        if increasing is None:
            if prev < cur:
                increasing = True
            elif prev > cur:
                increasing = False
        else:
            if increasing and prev > cur:
                safe = False
                break
            elif not increasing and prev < cur:
                safe = False
                break
    return safe

def part_1(data: Data):
    safe_reports = 0
    for report in data:
        safe = check_if_safe(report)
        safe_reports += safe
    return safe_reports

def part_2(data: Data):
    safe_reports = 0
    for report in data:
        report_safe = False
        if check_if_safe(report):
            report_safe = True
        else:
            for report_variant in combinations(report, len(report) - 1):
                if check_if_safe(report_variant):
                    report_safe = True
                    break
        safe_reports += report_safe
    return safe_reports


def parse_data(file: str):
    data: Data = []
    with open(file, "r") as f:
        for line in f:
            line = line.strip()
            data.append([int(x) for x in line.split()])
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
