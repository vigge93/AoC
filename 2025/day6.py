#!../venv/bin/python
import time
from argparse import ArgumentParser, BooleanOptionalAction
from typing import TypedDict

day = 6
part_1_example_answer: int | None = 4277556
part_2_example_answer: int | None = 3263827


class DataDict(TypedDict):
    pass


Data = list[str]  # DataDict


def part_1(data: Data):
    parsed_data: list[list[int]] = []
    ops: list[str] = []
    for line in data:
        cols = line.split()
        try:
            n_cols = list(map(int, cols))
            parsed_data.append(n_cols)
        except Exception:
            ops = cols
    s = 0
    for col in range(len(parsed_data[0])):
        op = ops[col]
        p_s = parsed_data[0][col]
        for row in range(1, len(parsed_data)):
            if op == "+":
                p_s += parsed_data[row][col]
            elif op == "*":
                p_s *= parsed_data[row][col]
        s += p_s
    return s


def part_2(data: Data):
    s = 0
    p_s = 0
    first = True
    op = ""
    for col in range(len(data[0])):
        empty = True
        num = ""
        for row in range(len(data)):
            char = data[row][col]
            if char == " ":
                continue
            empty = False
            if char.isnumeric():
                num += char
            else:
                op = char
        if empty:
            s += p_s
            first = True
            op = ""
            continue

        num = int(num)
        if first:
            p_s = num
        elif op == "+":
            p_s += num
        elif op == "*":
            p_s *= num
        first = False

    s += p_s
    return s

def parse_data(file: str):
    data: Data = []
    with open(file, "r") as f:
        for line in f:
            data.append(line.strip("\n"))
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
