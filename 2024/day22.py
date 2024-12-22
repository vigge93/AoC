#!/bin/pypy3
import time
from argparse import ArgumentParser, BooleanOptionalAction
from collections import defaultdict

day = 22
part_1_example_answer: int | None = 37327623
part_2_example_answer: int | None = 23


Data = list[int] # DataDict

def next_secret(secret: int):
    s1 = ((secret << 6) ^ secret) & 0xffffff
    s2 = ((s1 >> 5) ^ s1) & 0xffffff
    s3 = ((s2 << 11) ^ s2) & 0xffffff
    return s3

def part_1(data: Data):
    s = 0
    for o_secret in data:
        secret = o_secret
        for _ in range(2000):
            secret = next_secret(secret)
        s += secret
    return s

def part_2(data: Data):
    bananas: defaultdict[tuple[int, int, int, int], int] = defaultdict(int)
    for o_secret in data:
        secret = o_secret
        secret_bananas = o_secret % 10
        sequence: list[int] = []
        seq_len = 0
        known_seq: set[tuple[int,...]] = set()
        for _ in range(2000):
            n_secret = next_secret(secret)
            n_secret_bananas = n_secret % 10
            sequence.append(n_secret_bananas - secret_bananas)
            seq_len += 1
            if seq_len > 4:
                del sequence[0]
                seq_len -= 1
            if seq_len == 4:
                if (t_seq := tuple(sequence)) not in known_seq:
                    known_seq.add(t_seq)
                    bananas[t_seq] += n_secret_bananas
            secret_bananas = n_secret_bananas
            secret = n_secret
    return max(bananas.values())


def parse_data(file: str):
    data: Data = []
    with open(file, "r") as f:
        for line in f:
            data.append(int(line.strip()))
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
