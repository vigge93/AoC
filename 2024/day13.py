#!/bin/python
import re
import time
from argparse import ArgumentParser, BooleanOptionalAction
from typing import TypedDict

day = 13
part_1_example_answer: int | None = 480
part_2_example_answer: int | None = 875318608908

COST_A = 3
COST_B = 1


class DataDict(TypedDict):
    clawA: tuple[int, int]
    clawB: tuple[int, int]
    prize: tuple[int, int]


Data = list[list[list[int]]]


def part_1(data: Data):
    s = 0
    for (clawA_x, clawA_y), (clawB_x, clawB_y), (prize_x, prize_y) in data:

        x = (prize_y*clawB_x - prize_x*clawB_y)//(clawA_y*clawB_x - clawA_x*clawB_y)
        y = (prize_y*clawA_x - prize_x*clawA_y)//(clawA_x*clawB_y - clawB_x*clawA_y)

        if (clawA_x*x + clawB_x*y) == prize_x and (clawA_y*x + clawB_y*y) == prize_y:
            s += COST_A*x + COST_B*y
    return s


def part_2(data: Data):
    s = 0
    for (clawA_x, clawA_y), (clawB_x, clawB_y), (prize_x, prize_y) in data:
        prize_x += 10000000000000
        prize_y += 10000000000000

        x = (prize_y*clawB_x - prize_x*clawB_y)//(clawA_y*clawB_x - clawA_x*clawB_y)
        y = (prize_y*clawA_x - prize_x*clawA_y)//(clawA_x*clawB_y - clawB_x*clawA_y)
        
        if (clawA_x*x + clawB_x*y) == prize_x and (clawA_y*x + clawB_y*y) == prize_y:
            s += COST_A*x + COST_B*y
    return s


def parse_data(file: str):
    data: Data = []
    with open(file, "r") as f:
        machine: list[list[int]] = []
        i = 1
        pattern = re.compile(r"(?:\+|=)([0-9]+)")
        for line in f:
            if i % 4 == 0:
                data.append(machine)
                machine = []
            else:
                claw = [int(x) for x in pattern.findall(line)]
                machine.append(claw)
            i += 1
        data.append(machine)
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
