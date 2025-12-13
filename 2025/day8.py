#!../venv/bin/python
import heapq
import time
from argparse import ArgumentParser, BooleanOptionalAction
from math import dist
from typing import TypedDict

day = 8
part_1_example_answer: int | None = 40
part_2_example_answer: int | None = 25272


class DataDict(TypedDict):
    pass


Coord = tuple[int, int, int]
Data = list[Coord]  # DataDict


def part_1(data: Data, n: int):
    distances: list[tuple[float, tuple[Coord, Coord]]] = []
    circuits: dict[Coord, set[Coord]] = {}

    for i, first in enumerate(data):
        for second in data[i + 1 :]:
            heapq.heappush(distances, (dist(first, second), (first, second)))

    for _, (fr, to) in heapq.nsmallest(n, distances):
        if fr in circuits and to in circuits:
            if id(circuits[fr]) != id(circuits[to]):
                circuits[fr].update(circuits[to])
                for j in circuits[to]:
                    circuits[j] = circuits[fr]
        elif fr in circuits and to not in circuits:
            circuits[fr].add(to)
            circuits[to] = circuits[fr]
        elif to in circuits and fr not in circuits:
            circuits[to].add(fr)
            circuits[fr] = circuits[to]
        else:
            new_set = {to, fr}
            circuits[to] = new_set
            circuits[fr] = new_set

    seen_ids: set[int] = set()
    connected: list[int] = []
    for conn in circuits.values():
        if id(conn) not in seen_ids:
            connected.append(len(conn))
            seen_ids.add(id(conn))

    connected = sorted(connected, reverse=True)
    return connected[0] * connected[1] * connected[2]


def part_2(data: Data):
    distances: list[tuple[float, tuple[Coord, Coord]]] = []
    circuits: dict[Coord, list[Coord]] = {}
    ids: list[int] = []

    for i, first in enumerate(data):
        for second in data[i + 1 :]:
            heapq.heappush(distances, (dist(first, second), (first, second)))

    while True:
        _, (fr, to) = heapq.heappop(distances)
        if fr in circuits and to in circuits:
            if id(circuits[fr]) != id(circuits[to]):
                ids.remove(id(circuits[to]))
                for j in circuits[to]:
                    circuits[fr].append(j)
                    circuits[j] = circuits[fr]
        elif fr in circuits and to not in circuits:
            circuits[fr].append(to)
            circuits[to] = circuits[fr]
        elif to in circuits and fr not in circuits:
            circuits[to].append(fr)
            circuits[fr] = circuits[to]
        else:
            new_set = [to, fr]
            circuits[to] = new_set
            circuits[fr] = new_set
            ids.append(id(new_set))

        if len(ids) == 1 and len(circuits) == len(data):
            return fr[0] * to[0]


def parse_data(file: str):
    data: Data = []
    with open(file, "r") as f:
        for line in f:
            x, y, z = line.strip().split(",")
            data.append((int(x), int(y), int(z)))
    return data


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--test", action=BooleanOptionalAction, default=False)

    args = parser.parse_args()

    if args.test:
        if part_1_example_answer is not None:  # type: ignore
            data = parse_data(f"day{day}.xexample-1.txt")
            p1 = part_1(data, 10)
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
        p1 = part_1(data, 1000)
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
