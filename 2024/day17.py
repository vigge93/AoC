import time
from typing import TypedDict, Callable
from argparse import ArgumentParser, BooleanOptionalAction

day = 17
part_1_example_answer: str | None = "4,6,3,5,6,3,5,2,1,0"
part_2_example_answer: int | None = 117440


class DataDict(TypedDict):
    A: int
    B: int
    C: int
    program: list[int]

Data = DataDict


def part_1(data: Data):
    data = data.copy()
    pc = 0
    jumped = False
    stdout: list[str] = []
    program = data["program"]
    program_size = len(program)

    operand: dict[int, Callable[[], int]] = {
        0: lambda: 0,
        1: lambda: 1,
        2: lambda: 2,
        3: lambda: 3,
        4: lambda: data["A"],
        5: lambda: data["B"],
        6: lambda: data["C"],
    }

    def adv(op: int):
        data["A"] = data["A"] // 2**operand[op]()
    
    def bxl(op: int):
        data["B"] = data["B"] ^ op
    
    def bst(op: int):
        data["B"] = operand[op]() % 8
        
    def jnz(op: int):
        if data["A"] != 0:
            nonlocal pc, jumped
            pc = op
            jumped = True

    def bxc(op: int):
        data["B"] = data["B"] ^ data["C"] % 8
    
    def out(op: int):
        stdout.append(f"{operand[op]() % 8}")
    
    def bdv(op: int):
        data["B"] = data["A"] // 2**operand[op]()
    
    def cdv(op: int):
        data["C"] = (data["A"] // 2**operand[op]()) % 8
    
    instructions = {
        0: adv,
        1: bxl,
        2: bst,
        3: jnz,
        4: bxc,
        5: out,
        6: bdv,
        7: cdv,
    }
    
    while 0 <= pc < program_size - 1:
        instruction = program[pc]
        op = program[pc + 1]
        instructions[instruction](op)
        if not jumped:
            pc += 2
        else:
            jumped = False
    return ','.join(stdout)
    
def part_2(data: Data):
    data = data.copy()
    program = data["program"]
    program_size = len(program)
    stdout = 0

    operand: dict[int, Callable[[], int]] = {
        0: lambda: 0,
        1: lambda: 1,
        2: lambda: 2,
        3: lambda: 3,
        4: lambda: data["A"],
        5: lambda: data["B"],
        6: lambda: data["C"],
    }

    def adv(op: int):
        data["A"] = data["A"] // 2**operand[op]()
    
    def bxl(op: int):
        data["B"] = data["B"] ^ op
    
    def bst(op: int):
        data["B"] = operand[op]() % 8
        
    def jnz(op: int):
        pass

    def bxc(op: int):
        data["B"] = data["B"] ^ data["C"] % 8
    
    def out(op: int):
        nonlocal stdout
        stdout = operand[op]() % 8
    
    def bdv(op: int):
        data["B"] = data["A"] // 2**operand[op]()
    
    def cdv(op: int):
        data["C"] = (data["A"] // 2**operand[op]()) % 8
    
    instructions = {
        0: adv,
        1: bxl,
        2: bst,
        3: jnz,
        4: bxc,
        5: out,
        6: bdv,
        7: cdv,
    }

    def run_iteration(a: int):
        pc = 0
        data["A"] = a
        while 0 <= pc < program_size - 1:
            instruction = program[pc]
            op = program[pc + 1]
            instructions[instruction](op)
            pc += 2
        return stdout
    
    def run_iteration_fast(a: int):  # type: ignore
        b = (a % 8)
        b ^= 1
        c = (a >> b) % 8
        a >>= 3
        b ^= 4
        b = b ^ c
        return b % 8
    
    stack: list[tuple[int, int]] = [(0, 0)]
    while stack:
        n, a = stack.pop(0)
        if n == len(program):
            return a
        next_out = program[-n-1]
        for new in range(8):
            new_a = (a << 3) + new
            # c_out = run_iteration_fast(new_a)
            c_out = run_iteration(new_a)
            if c_out == next_out:
                stack.append((n + 1, new_a))
    return -1


def parse_data(file: str):
    data: Data = {"A": 0, "B": 0, "C": 0, "program": []}
    with open(file, "r") as f:
        data["A"] = int(f.readline().split(":")[1].strip())
        data["B"] = int(f.readline().split(":")[1].strip())
        data["C"] = int(f.readline().split(":")[1].strip())
        f.readline()
        data["program"] = [int(p) for p in f.readline().split(":")[1].strip().split(",")]
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
