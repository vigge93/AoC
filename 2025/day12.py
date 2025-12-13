#!../venv/bin/python
import time
from argparse import ArgumentParser, BooleanOptionalAction
from functools import cache
from typing import Iterable, TypedDict

day = 12
part_1_example_answer: int | None = 2


class DataDict(TypedDict):
    presents: list[set[tuple[int, int]]]
    trees: list[tuple[tuple[int, int], list[int]]]


Data = DataDict


def print_grid(data: Iterable[tuple[int, int]]):
    max_x = max([x for (x, _) in data])
    max_y = max([y for (_, y) in data])
    grid = [["." for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for x, y in data:
        grid[y][x] = "#"
    grid = ["".join(row) for row in grid]
    print(*grid, sep="\n")


def get_offset_func(x_off: int, y_off: int):
    def offset(present: tuple[int, int]):
        return present[0] + x_off, present[1] + y_off

    return offset


def get_boundary_check_func(x_max: int, y_max: int):
    def check_boundary(present: tuple[int, int]):
        return 0 <= present[0] < x_max and 0 <= present[1] < y_max

    return check_boundary


def flip_func(present: tuple[int, int]):
    if present[0] == 0:
        return 2, present[1]
    if present[0] == 2:
        return 0, present[1]
    return present


@cache
def flip_func_f(presents: frozenset[tuple[int, int]]):
    n_set: set[tuple[int, int]] = set()
    for present in presents:
        n_set.add(flip_func(present))
    return frozenset(n_set)


@cache
def rotate_full(presents: frozenset[tuple[int, int]], rotate: int):
    rotate_func = get_rotate_func(rotate)
    n_set: set[tuple[int, int]] = set()
    for present in presents:
        n_set.add(rotate_func(present))
    return frozenset(n_set)


def get_rotate_func(rotate: int):
    if rotate == 0:

        def rotate_func(present: tuple[int, int]):
            return present

    else:

        def int_rotate_func(present: tuple[int, int]):
            x, y = present
            match present:
                case (0, 0):
                    return (0, 2)
                case (1, 0):
                    return (0, 1)
                case (2, 0):
                    return (0, 0)
                case (0, 1):
                    return (1, 2)
                case (1, 1):
                    return (1, 1)
                case (2, 1):
                    return (1, 0)
                case (0, 2):
                    return (2, 2)
                case (1, 2):
                    return (2, 1)
                case (2, 2):
                    return (2, 0)
            return x, y

        def rotate_func(present: tuple[int, int]):
            for _ in range(rotate):
                present = int_rotate_func(present)
            return present

    return rotate_func


def part_1_recurse_factory(presents: list[set[tuple[int, int]]]):

    @cache
    def part_1_recurse(
        grid: frozenset[tuple[int, int]],
        current: tuple[int, ...],
        goal: tuple[int, ...],
        explored: frozenset[tuple[int, int]] = frozenset(),
    ):
        if current == goal:
            return True
        remaining_presents: list[int] = []
        for i, g in enumerate(goal):
            remaining_presents.append(g - current[i])
        for idx, present in enumerate(presents):
            if not remaining_presents[idx]:
                continue
            visited: list[tuple[int, int]] = []
            for off_x, off_y in grid - explored:
                visited.append((off_x, off_y))
                for flip in (0, 1):
                    for rotate in range(4):
                        n_present = frozenset(present)
                        if flip:
                            n_present = flip_func_f(n_present)
                        if rotate:
                            n_present = rotate_full(n_present, rotate)
                        if off_x or off_y:
                            n_present = map(get_offset_func(off_x, off_y), n_present)
                        n_present = frozenset(n_present)
                        if n_present <= grid:
                            new_current = list(current)
                            new_current[idx] += 1
                            if new_current[idx]:
                                if part_1_recurse(
                                    grid - n_present,
                                    tuple(new_current),
                                    goal,
                                    explored | frozenset(visited),
                                ):
                                    return True
                            else:
                                if part_1_recurse(
                                    grid - n_present, tuple(new_current), goal
                                ):
                                    return True
            break
        return False

    return part_1_recurse


def part_1(data: Data):
    s = 0
    areas = list(map(len, data["presents"]))
    for i, tree in enumerate(data["trees"]):
        print(i)
        (s_x, s_y), presents = tree
        max_area = s_x * s_y
        area = 0
        for idx, present in enumerate(presents):
            area += areas[idx] * present
        if area > max_area:
            continue
        if max_area >= 9 * sum(presents):
            s += 1
            continue

        part_1_recurse = part_1_recurse_factory(data["presents"])
        if part_1_recurse(
            frozenset([(x, y) for x in range(s_x) for y in range(s_y)]),
            (0,) * len(presents),
            tuple(presents),
        ):
            s += 1
    return s


def parse_data(file: str):
    data: Data = {
        "presents": [],
        "trees": [],
    }
    with open(file, "r") as f:
        present_c: set[tuple[int, int]] = set()
        present = False
        y = 0
        for line in f:
            if line.strip().endswith(":"):
                present = True
                present_c = set()
                y = 0
                continue
            if not line.strip():
                if present:
                    data["presents"].append(present_c)
                present = False
                continue
            if present:
                for x, t in enumerate(line.strip()):
                    if t == "#":
                        present_c.add((x, y))
                y += 1
            else:
                size, presents = line.strip().split(":")
                size_x, size_y = size.split("x")
                presents = presents.split()
                data["trees"].append(
                    ((int(size_x), int(size_y)), list(map(int, presents)))
                )
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

    else:
        start_time = time.perf_counter_ns()
        data = parse_data(f"day{day}.txt")
        data_time = time.perf_counter_ns()
        p1 = part_1(data)
        end_time = time.perf_counter_ns()
        print(
            f"""=== Day {day:02} ===\n"""
            f"""  · Loading data\n"""
            f"""  · Elapsed: {(data_time - start_time)/10**6:.3f} ms\n\n"""
            f"""  · Part 1: {p1}\n"""
            f"""  · Elapsed: {(end_time - data_time)/10**6:.3f} ms\n\n"""
            f"""  · Total elapsed: {(end_time - start_time)/10**6:.3f} ms"""
        )
