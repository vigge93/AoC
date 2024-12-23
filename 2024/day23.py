#!/bin/python
import time
from argparse import ArgumentParser, BooleanOptionalAction
from collections import defaultdict

day = 23
part_1_example_answer: int | None = 7
part_2_example_answer: str | None = "co,de,ka,ta"


Data = defaultdict[str, set[str]]


def bron_kerbosch_factory(data: Data):
    maximal_cliques: list[set[str]] = []

    def bron_kerbosch(R: set[str], P: set[str], X: set[str]):
        if not P and not X:
            maximal_cliques.append(R)
            return
        pivot = next(iter(P | X))
        candidates = P - data[pivot]
        while candidates:
            v = candidates.pop()
            bron_kerbosch(R | {v}, P & data[v], X & data[v])
            P.remove(v)
            X.add(v)

    return bron_kerbosch, maximal_cliques


def part_1(data: Data):
    lans: set[frozenset[str]] = set()
    for computer in data:
        for computer2 in data[computer]:
            common = data[computer] & data[computer2]
            if len(common):
                for computer3 in common:
                    if "t" in (computer[0], computer2[0], computer3[0]):
                        lans.add(frozenset([computer, computer2, computer3]))
    return len(lans)


def part_2(data: Data):
    bron_kerbosch, maximal_lans = bron_kerbosch_factory(data)
    bron_kerbosch(set(), set(data.keys()), set())
    maximal_lan = max(maximal_lans, key=lambda x: len(x))
    return ",".join(sorted(maximal_lan))


def parse_data(file: str):
    data: Data = defaultdict(set)
    with open(file, "r") as f:
        for line in f:
            comp1, comp2 = line.strip().split("-")
            data[comp1].add(comp2)
            data[comp2].add(comp1)
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
