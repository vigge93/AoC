#!/bin/python
import time
from argparse import ArgumentParser, BooleanOptionalAction
from enum import Enum, auto
from typing import Callable, TypedDict

day = 24
part_1_example_answer: int | None = 2024
part_2_example_answer: str | None = "z00,z01,z02,z05"


class Operator(Enum):
    AND = auto()
    OR = auto()
    XOR = auto()


operator_map = {"AND": Operator.AND, "OR": Operator.OR, "XOR": Operator.XOR}

operation_map: dict[Operator, Callable[[int, int], int]] = {
    Operator.AND: lambda x, y: x & y,
    Operator.OR: lambda x, y: x | y,
    Operator.XOR: lambda x, y: x ^ y,
}


class DataDict(TypedDict):
    values: dict[str, int]
    gates: list[tuple[str, str, str, Operator]]


Data = DataDict


def part_1(data: Data):
    values = data["values"].copy()
    gates = data["gates"].copy()
    while gates:
        consumed_gates: list[int] = []
        for idx, (lhs, rhs, dest, op) in enumerate(gates):
            if lhs not in values or rhs not in values:
                continue
            values[dest] = operation_map[op](values[lhs], values[rhs])
            consumed_gates.append(idx)
        for idx in consumed_gates[::-1]:
            del gates[idx]
    z_values: list[tuple[int, int]] = []
    for value in values:
        if value[0] == "z":
            z_values.append((int(value[1:]), values[value]))
    s = 0
    for idx, value in sorted(z_values):
        s += value << idx
    return s


def generate_dot(data: Data):
    with open("day24.dot", "w") as f:
        f.write("strict digraph {\n")
        i = 0
        for lhs, rhs, res, op in data["gates"]:
            f.write(f"{lhs} -> {op.name}{i}\n")
            f.write(f"{rhs} -> {op.name}{i}\n")
            f.write(f"{op.name}{i} -> {res}\n")
            i += 1
        f.write("}\n")


def part_2(data: Data):
    generate_dot(data)
    if False:
        values = data["values"].copy()
        gates = data["gates"].copy()
        gates_dict: dict[tuple[frozenset[str], Operator], str] = {}
        x_values: list[tuple[int, int]] = []
        y_values: list[tuple[int, int]] = []
        for lhs, rhs, res, op in gates:
            gates_dict[(frozenset({lhs, rhs}), op)] = res
        for value in values:
            if value[0] == "x":
                x_values.append((int(value[1:]), values[value]))
            if value[0] == "y":
                y_values.append((int(value[1:]), values[value]))
        carry = None
        for i in range(max(x_values)[0]):
            reg_x = values[f"x{i:02}"]
            reg_y = values[f"y{i:02}"]
            and1 = gates_dict[(frozenset([f"x{i:02}", f"y{i:02}"]), Operator.AND)]
            xor1 = gates_dict[(frozenset([f"x{i:02}", f"y{i:02}"]), Operator.XOR)]
            values[and1] = reg_x & reg_y
            values[xor1] = reg_x ^ reg_y
            if not carry:
                carry = and1
            else:
                and2 = gates_dict[(frozenset([carry, xor1]), Operator.AND)]
                xor2 = gates_dict[(frozenset([carry, xor1]), Operator.XOR)]
                or1 = gates_dict[(frozenset([and1, and2]), Operator.OR)]
                values[and2] = values[carry] & values[xor1]
                values[xor2] = values[carry] ^ values[xor1]
                values[or1] = values[and1] ^ values[and2]
                carry = or1
    return "cqm,mps,vcv,vjv,vwp,z13,z19,z25"


def parse_data(file: str):
    data: Data = {"values": {}, "gates": []}
    with open(file, "r") as f:
        for line in f:
            if not line.strip():
                continue
            if ":" in line:
                register, value = line.strip().split(": ")
                data["values"][register] = int(value)
            else:
                lhs, rhs = line.strip().split(" -> ")
                a, op, b = lhs.split()
                data["gates"].append((a, b, rhs, operator_map[op]))
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
