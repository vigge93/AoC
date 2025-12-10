#!../venv/bin/python
from dataclasses import dataclass
import itertools
import time
from argparse import ArgumentParser, BooleanOptionalAction
import numpy as np
import scipy

day = 10
part_1_example_answer: int | None = 7
part_2_example_answer: int | None = 33


@dataclass
class Machine:
    indicator_lights: int
    button_bits: list[int]
    buttons: list[tuple[int,...]]
    joltic: tuple[int,...]


Data = list[Machine]  # DataDict

def find_indicator_flips_bfs(buttons: list[int], target_state: int):
    for n in range(1, len(buttons) + 1):
        for button_presses in itertools.combinations(buttons, n):
            state = 0
            for b in button_presses:
                state ^= b
            if state == target_state:
                return n
    raise Exception("Did not find any possible flips!")

def part_1(data: Data):
    s = 0
    for machine in data:
        s += find_indicator_flips_bfs(machine.button_bits, machine.indicator_lights)
    return s
    
def part_2(data: Data):
    s = 0
    for machine in data:
        rows, cols = len(machine.joltic), len(machine.buttons)
        A = np.zeros((rows, cols))
        for joltic in range(rows):
            for i, button in enumerate(machine.buttons):
                if joltic in button:
                    A[joltic,i] = 1
        b = np.array(machine.joltic)

        res = scipy.optimize.linprog([1]*cols, A_eq=A,b_eq=b, integrality=True)
        s += round(sum(res.x))
    return s


def parse_data(file: str):
    data: Data = []
    with open(file, "r") as f:
        for line in f:
            m = Machine(0, [], [], tuple())
            for item in line.strip().split():
                if item[0] == "[":
                    for idx, light in enumerate(item[1:-1]):
                        if light == "#":
                            m.indicator_lights |= 1 << idx
                elif item[0] == "(":
                    b_s = 0
                    b_t: list[int] = []
                    for b in item[1:-1].split(","):
                        b_s |= 1 << int(b)
                        b_t.append(int(b))
                    m.buttons.append(tuple(b_t))
                    m.button_bits.append(b_s)
                elif item[0] == "{":
                    j_t: list[int] = []
                    for j in item[1:-1].split(","):
                        j_t.append(int(j))
                    m.joltic = tuple(j_t)
            data.append(m)

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
