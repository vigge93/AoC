#!../venv/bin/python
import time
from argparse import ArgumentParser, BooleanOptionalAction
from itertools import pairwise

day = 9
part_1_example_answer: int | None = 50
part_2_example_answer: int | None = 24


Data = list[tuple[int, int]]


def part_1(data: Data):
    largest_a = 0
    for i, (x1, y1) in enumerate(data):
        for x2, y2 in data[i + 1 :]:
            a = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if a > largest_a:
                largest_a = a
    return largest_a


def part_2(data: Data):
    border: set[tuple[int, int]] = set(data)
    data.append(data[0])
    for (x1, y1), (x2, y2) in pairwise(data):
        for x in range(min(x1, x2), max(x1, x2)):
            border.add((x, y1))
        for y in range(min(y1, y2), max(y1, y2)):
            border.add((x1, y))

    squares: list[tuple[int, tuple[tuple[int, int], tuple[int, int]]]] = []
    for i, (x1, y1) in enumerate(data):
        for x2, y2 in data[i + 1 :]:
            a = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            squares.append((a, ((x1, y1), (x2, y2))))

    squares.sort(reverse=True)
    for a, ls in squares:
        lsx1 = min(ls[0][0], ls[1][0])
        lsx2 = max(ls[0][0], ls[1][0])
        lsy1 = min(ls[0][1], ls[1][1])
        lsy2 = max(ls[0][1], ls[1][1])
        found = True
        for bx, by in border:
            if lsx1 < bx < lsx2:
                if lsy1 < by < lsy2:
                    found = False
                    break
        if found:
            return a
    return 0


def parse_data(file: str):
    data: Data = []
    with open(file, "r") as f:
        for line in f:
            x, y = line.strip().split(",")
            data.append((int(x), int(y)))
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
