#!../venv/bin/python
import time
from argparse import ArgumentParser, BooleanOptionalAction

day = 3
part_1_example_answer: int | None = 357
part_2_example_answer: int | None = 3121910778619

Data = list[str]


def part_1(data: Data):
    s = 0
    for bank in data:
        largest = max(bank[:-1])
        largest_idx = bank.index(largest)
        second_largest = max(bank[largest_idx + 1 :])
        s += int(largest + second_largest)
    return s


def part_2(data: Data):
    s = 0
    for bank in data:
        prev_largest_idx = -1
        bits: list[str] = []
        for n in range(11, -1, -1):
            active = bank[prev_largest_idx + 1 :]
            if n != 0:
                active = active[:-n]
            largest = max(active)
            bits.append(largest)
            prev_largest_idx = active.index(largest) + prev_largest_idx + 1
        s += int("".join(bits))
    return s


def parse_data(file: str):
    data: Data = []
    with open(file, "r") as f:
        for line in f:
            data.append(line.strip())
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
