#!../venv/bin/python
import time
from argparse import ArgumentParser, BooleanOptionalAction

day = 4
part_1_example_answer: int | None = 13
part_2_example_answer: int | None = 43

Data = dict[tuple[int, int], set[tuple[int, int]]]

offs = ((-1, -1), (0, -1), (1, -1),
        (-1, 0),           (1, 0),
        (-1, 1),  (0, 1),  (1, 1))


def part_1(data: Data):
    s = 0
    for roll in data:
        x, y = roll
        adj_rolls = 0
        for x_off, y_off in offs:
            if (x + x_off, y + y_off) in data:
                adj_rolls += 1
        if adj_rolls < 4:
            s += 1
    return s

def part_2(data: Data):
    s = 0
    
    for roll in data:
        x, y = roll
        for x_off, y_off in offs:
            if (x + x_off, y + y_off) in data:
                data[roll].add((x + x_off, y + y_off))

    removed = True
    while removed:
        data_proxy = data.copy()
        removed = False
        for roll in data:
            x, y = roll
            if len(data_proxy[roll]) < 4:
                s += 1
                removed = True
                for adj in data_proxy[roll]:
                    data_proxy[adj].remove(roll)
                del data_proxy[roll]

        data = data_proxy
    return s


def parse_data(file: str):
    data: Data = {}
    with open(file, "r") as f:
        for y, line in enumerate(f):
            for x, cell in enumerate(line):
                if cell == "@":
                    data[(x, y)] = set()
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
