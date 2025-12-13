#!../venv/bin/python
import re
import time
from argparse import ArgumentParser, BooleanOptionalAction
from multiprocessing import Pool

import numpy as np

day = 2
part_1_example_answer: int | None = 1227775554
part_2_example_answer: int | None = 4174379265

Data = list[tuple[int, int]]

regexp_1 = re.compile(r"(\d+)\1")
regexp_2 = re.compile(r"(\d+)\1+")


def get_sum(inp: tuple[int, int]):
    s_2 = 0
    s_1 = 0
    for serial in range(inp[0], inp[1] + 1):
        serial_str = str(serial)
        if regexp_2.fullmatch(serial_str):
            s_2 += serial
            if regexp_1.fullmatch(serial_str):
                s_1 += serial
    return s_1, s_2


def part_1_and_2(data: Data):
    with Pool() as p:
        res = np.fromiter(p.imap_unordered(get_sum, data), dtype=np.dtype((int, 2)))
        res = np.add.reduce(res)
    return res[0], res[1]


def parse_data(file: str):
    data: Data = []
    with open(file, "r") as f:
        ids = f.read().split(",")
        for id in ids:
            first, last = id.split("-")
            data.append((int(first), int(last)))
    return data


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--test", action=BooleanOptionalAction, default=False)

    args = parser.parse_args()

    if args.test:
        if part_1_example_answer is not None:  # type: ignore
            data = parse_data(f"day{day}.xexample-1.txt")
            p1, p2 = part_1_and_2(data)
            if p1 != part_1_example_answer:
                print(
                    f"Wrong answer to part 1: answer: {p1}, expected: {part_1_example_answer}"
                )
            else:
                print("Example part 1 passed!")
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
        p1, p2 = part_1_and_2(data)
        end_time = time.perf_counter_ns()
        print(
            f"""=== Day {day:02} ===\n"""
            f"""  · Loading data\n"""
            f"""  · Elapsed: {(data_time - start_time)/10**6:.3f} ms\n\n"""
            f"""  · Part 1: {p1}\n"""
            f"""  · Elapsed: {(end_time - data_time)/10**6:.3f} ms\n\n"""
            f"""  · Part 2: {p2}\n"""
            f"""  · Elapsed: 0 ms\n\n"""
            f"""  · Total elapsed: {(end_time - start_time)/10**6:.3f} ms"""
        )
