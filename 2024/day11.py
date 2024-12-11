import time
from typing import TypedDict
from argparse import ArgumentParser, BooleanOptionalAction
from collections import defaultdict
from math import log10

day = 11
part_1_example_answer: int | None = 55312
part_2_example_answer: int | None = None


class DataDict(TypedDict):
    pass
Data = defaultdict[int, int] # DataDict

def do_iterations(rounds: int, data: Data):
    for _ in range(rounds):
        next_iteration: Data = defaultdict(int)
        for stone, count in data.items():
            if stone == 0:
                next_iteration[1] += count
            elif (length := int(log10(stone))) % 2 == 0: # Odd length
                next_iteration[stone * 2024] += count
            else:
                length += 1
                partition = int(10**(length/2))
                left_stone = stone // partition
                right_stone = stone % partition
                next_iteration[left_stone] += count
                next_iteration[right_stone] += count
        data = next_iteration
    return sum(data.values())

def part_1(data: Data):
    return do_iterations(25, data)
                    

def part_2(data: Data):
    return do_iterations(75, data)


def parse_data(file: str):
    data: Data = defaultdict(int)
    with open(file, "r") as f:
        stones = [int(s) for s in f.read().strip().split()]
        for stone in stones:
            data[stone] += 1
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
