import time
from typing import TypedDict
from argparse import ArgumentParser, BooleanOptionalAction
from copy import deepcopy

day = 9
part_1_example_answer: int | None = 1928
part_2_example_answer: int | None = 2858


class DataDict(TypedDict):
    start: int
    size: int
    val: int

class DataDict2(TypedDict):
    memory: dict[int, DataDict]
    free: list[int]
    allocated: list[int]

Data = DataDict2

FREE_ID = -1


def part_1(data: Data):
    memory = deepcopy(data["memory"])
    free = data["free"][:]
    allocated = data["allocated"][:]
    while free:
        next_free = memory[free[0]]
        next_mem = memory[allocated[-1]]
        if next_free["start"] > next_mem["start"]:
            break
        if next_free["size"] <= next_mem["size"]:
            next_free["val"] = next_mem["val"]
            next_mem["size"] -= next_free["size"]
            free.pop(0)
            if next_mem["size"] == 0:
                next_mem["val"] = FREE_ID
                allocated.pop()
        else: # next_free["size"] > next_mem["size"]
            new_free_addr = next_free["start"] + next_mem["size"]
            new_free_size = next_free["size"] - next_mem["size"]
            next_free["size"] = next_mem["size"]
            next_free["val"] = next_mem["val"]
            memory[new_free_addr] = {
                "start": new_free_addr,
                "size": new_free_size,
                "val": FREE_ID
            }
            next_mem["val"] = FREE_ID
            allocated.pop()
            free[0] = new_free_addr

    s = 0
    for mem in memory.values():
        if mem["val"] == FREE_ID:
            continue
        s += mem["val"] * mem["size"] * (2 * mem["start"] + mem["size"] - 1) // 2
    return s

def part_2(data: Data):
    memory = data["memory"]
    free = data["free"]
    allocated = data["allocated"]
    while allocated:
        next_mem = memory[allocated[-1]]
        for next_free_idx, next_free_addr in enumerate(free):
            next_free = memory[next_free_addr]
            if next_free["start"] > next_mem["start"]:
                break
            if next_mem["size"] > next_free["size"]:
                continue
            
            if next_mem["size"] == next_free["size"]:
                next_free["val"] = next_mem["val"]
                next_mem["val"] = FREE_ID
                free.pop(next_free_idx)
            else: # next_mem["size"] < next_free["size"]
                new_free_addr = next_free["start"] + next_mem["size"]
                new_free_size = next_free["size"] - next_mem["size"]
                next_free["size"] = next_mem["size"]
                next_free["val"] = next_mem["val"]
                memory[new_free_addr] = {
                    "start": new_free_addr,
                    "size": new_free_size,
                    "val": FREE_ID
                }
                next_mem["val"] = FREE_ID
                free[next_free_idx] = new_free_addr
            break
        allocated.pop()
    s = 0
    for mem in memory.values():
        if mem["val"] == FREE_ID:
            continue
        s += mem["val"] * mem["size"] * (2 * mem["start"] + mem["size"] - 1) // 2
    return s


def parse_data(file: str):
    data: Data = {
        "memory": {},
        "free": [],
        "allocated": []
    }
    i = 0
    id = 0
    address = 0
    with open(file, "r") as f:
        for c in f.read().strip():
            size = int(c)
            if size == 0:
                i += 1
                continue
            if i % 2 == 0: # allocated
                val = id
                id += 1
                if size > 0:
                    data["allocated"].append(address)
            else: # free
                data["free"].append(address)
                val = FREE_ID

            data["memory"][address] = {
                "start": address,
                "size": size,
                "val": val
            }
            address += size
            i += 1
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
