import math
import time
from functools import reduce
from itertools import cycle

day = 8


def part_1(data):
    moves = data["moves"]
    nodes = data["nodes"]
    n_steps = 0
    current = "AAA"
    for step in cycle(moves):
        if current == "ZZZ":
            break
        current = nodes[current][step]
        n_steps += 1
    return n_steps


def part_2(data):
    moves = data["moves"]
    nodes = data["nodes"]
    current = list(filter(lambda node: node[-1] == "A", nodes))

    cycles = []
    for node in current:
        seen = {}
        current = node
        start = None
        cycle_steps = None
        for idx, step in enumerate(cycle(moves)):
            step_idx = idx % len(moves)
            current = nodes[current][step]
            if (current, step_idx) in seen:
                start = seen[(current, step_idx)]
                cycle_steps = idx + 1 - start
                break
            idx += 1
            if current[-1] == "Z":
                seen[(current, step_idx)] = idx
        cycles.append(start)  # start == cycle_steps, GCD for all cycles = 271

    return math.lcm(*cycles)


def parse_data():
    data = {"moves": [], "nodes": {}}
    with open(f"day{day}.txt", "r") as f:
        moves = [
            int(c) for c in f.readline().strip().replace("L", "0").replace("R", "1")
        ]
        data["moves"] = moves
        f.readline()
        for line in f:
            node, children = line.strip().split("=")
            left, right = children.strip().replace("(", "").replace(")", "").split(",")
            data["nodes"][node.strip()] = (left.strip(), right.strip())
    return data


if __name__ == "__main__":
    start_time = time.perf_counter_ns()
    data = parse_data()
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
