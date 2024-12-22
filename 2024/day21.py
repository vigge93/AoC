#!/bin/python
import time
from argparse import ArgumentParser, BooleanOptionalAction
from enum import Enum, IntEnum, auto

day = 21
part_1_example_answer: int | None = 126384
part_2_example_answer: int | None = None

class DirectionKeys(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    A = auto()

class NumKeys(IntEnum):
    KEY_0 = 0
    KEY_1 = auto()
    KEY_2 = auto()
    KEY_3 = auto()
    KEY_4 = auto()
    KEY_5 = auto()
    KEY_6 = auto()
    KEY_7 = auto()
    KEY_8 = auto()
    KEY_9 = auto()
    A = auto()

direction_key_map: dict[DirectionKeys, dict[DirectionKeys, tuple[int, set[tuple[DirectionKeys, ...]]]]] = {
    DirectionKeys.UP: {
        DirectionKeys.UP: (1, {(DirectionKeys.A,)}),
        DirectionKeys.DOWN: (2, {(DirectionKeys.DOWN,DirectionKeys.A)}),
        DirectionKeys.LEFT: (3, {(DirectionKeys.DOWN, DirectionKeys.LEFT, DirectionKeys.A)}),
        DirectionKeys.RIGHT: (3, {(DirectionKeys.DOWN, DirectionKeys.RIGHT, DirectionKeys.A), (DirectionKeys.RIGHT, DirectionKeys.DOWN, DirectionKeys.A)}),
        DirectionKeys.A: (2, {(DirectionKeys.RIGHT, DirectionKeys.A)}),
    },
    DirectionKeys.DOWN: {
        DirectionKeys.UP: (2, {(DirectionKeys.UP, DirectionKeys.A)}),
        DirectionKeys.DOWN: (1, {(DirectionKeys.A, )}),
        DirectionKeys.LEFT: (2, {(DirectionKeys.LEFT, DirectionKeys.A)}),
        DirectionKeys.RIGHT: (2, {(DirectionKeys.RIGHT, DirectionKeys.A)}),
        DirectionKeys.A: (3, {(DirectionKeys.RIGHT, DirectionKeys.UP, DirectionKeys.A), (DirectionKeys.UP, DirectionKeys.RIGHT, DirectionKeys.A)}),
    },
    DirectionKeys.LEFT: {
        DirectionKeys.UP: (3, {(DirectionKeys.RIGHT, DirectionKeys.UP, DirectionKeys.A)}),
        DirectionKeys.DOWN: (2, {(DirectionKeys.RIGHT, DirectionKeys.A)}),
        DirectionKeys.LEFT: (1, {(DirectionKeys.A, )}),
        DirectionKeys.RIGHT: (3, {(DirectionKeys.RIGHT, DirectionKeys.RIGHT, DirectionKeys.A)}),
        DirectionKeys.A: (4, {(DirectionKeys.RIGHT, DirectionKeys.RIGHT, DirectionKeys.UP, DirectionKeys.A)}),
    },
    DirectionKeys.RIGHT: {
        DirectionKeys.UP: (3, {(DirectionKeys.LEFT, DirectionKeys.UP, DirectionKeys.A), (DirectionKeys.UP, DirectionKeys.LEFT, DirectionKeys.A)}),
        DirectionKeys.DOWN: (2, {(DirectionKeys.LEFT, DirectionKeys.A)}),
        DirectionKeys.LEFT: (3, {(DirectionKeys.LEFT, DirectionKeys.LEFT, DirectionKeys.A)}),
        DirectionKeys.RIGHT: (1, {(DirectionKeys.A, )}),
        DirectionKeys.A: (2, {(DirectionKeys.UP, DirectionKeys.A)}),
    },
    DirectionKeys.A: {
        DirectionKeys.UP: (2, {(DirectionKeys.LEFT, DirectionKeys.A)}),
        DirectionKeys.DOWN: (3, {(DirectionKeys.LEFT,DirectionKeys.DOWN, DirectionKeys.A), (DirectionKeys.DOWN,DirectionKeys.LEFT, DirectionKeys.A)}),
        DirectionKeys.LEFT: (4, {(DirectionKeys.DOWN, DirectionKeys.LEFT, DirectionKeys.LEFT, DirectionKeys.A)}),
        DirectionKeys.RIGHT: (2, {(DirectionKeys.DOWN, DirectionKeys.A)}),
        DirectionKeys.A: (1, {(DirectionKeys.A, )}),
    },
}

direction_keymap = {
    DirectionKeys.UP: (1, 0),
    DirectionKeys.A: (2, 0),
    DirectionKeys.LEFT: (0, 1),
    DirectionKeys.DOWN: (1, 1),
    DirectionKeys.RIGHT: (2, 1),
}

num_keymap = {
    NumKeys.KEY_7: (0, 0),
    NumKeys.KEY_8: (1, 0),
    NumKeys.KEY_9: (2, 0),
    NumKeys.KEY_4: (0, 1),
    NumKeys.KEY_5: (1, 1),
    NumKeys.KEY_6: (2, 1),
    NumKeys.KEY_1: (0, 2),
    NumKeys.KEY_2: (1, 2),
    NumKeys.KEY_3: (2, 2),
    NumKeys.KEY_0: (1, 3),
    NumKeys.A: (2, 3)
}

Data = list[str] # DataDict

def move_numeric(key_from: NumKeys, key_to: NumKeys):
    key_to_coord = num_keymap[key_to]
    key_from_coord = num_keymap[key_from]
    sequences: set[tuple[DirectionKeys,...]] = set()
    x_first_possible = (key_to_coord[0], key_from_coord[1]) in num_keymap.values()
    y_first_possible = (key_from_coord[0], key_to_coord[1]) in num_keymap.values()
    left = key_from_coord[0] > key_to_coord[0]
    right = key_from_coord[0] < key_to_coord[0]
    up = key_from_coord[1] > key_to_coord[1]
    down = key_from_coord[1] < key_to_coord[1]
    if x_first_possible:
        n_seq: list[DirectionKeys] = []
        if left:
            n_seq.extend([DirectionKeys.LEFT]*(key_from_coord[0] - key_to_coord[0]))
        elif right:
            n_seq.extend([DirectionKeys.RIGHT]*(key_to_coord[0] - key_from_coord[0]))
        if up:
            n_seq.extend([DirectionKeys.UP]*(key_from_coord[1] - key_to_coord[1]))
        elif down:
            n_seq.extend([DirectionKeys.DOWN]*(key_to_coord[1] - key_from_coord[1]))
        n_seq.append(DirectionKeys.A)
        sequences.add(tuple(n_seq))
    if y_first_possible:
        n_seq: list[DirectionKeys] = []
        if up:
            n_seq.extend([DirectionKeys.UP]*(key_from_coord[1] - key_to_coord[1]))
        elif down:
            n_seq.extend([DirectionKeys.DOWN]*(key_to_coord[1] - key_from_coord[1]))
        if left:
            n_seq.extend([DirectionKeys.LEFT]*(key_from_coord[0] - key_to_coord[0]))
        elif right:
            n_seq.extend([DirectionKeys.RIGHT]*(key_to_coord[0] - key_from_coord[0]))
        n_seq.append(DirectionKeys.A)
        sequences.add(tuple(n_seq))
    return sequences

def move_directional(key_from: DirectionKeys, key_to: DirectionKeys):
    cost, sequences = direction_key_map[key_from][key_to]
    return cost, sequences

print_map = {
    DirectionKeys.A: "A",
    DirectionKeys.UP: "^",
    DirectionKeys.DOWN: "v",
    DirectionKeys.LEFT: "<",
    DirectionKeys.RIGHT: ">"
}

def part_1(data: Data):
    numerical_robot = NumKeys.A
    directional_robot_1 = DirectionKeys.A
    directional_robot_2 = DirectionKeys.A
    s = 0
    for keypad in data:
        tot_cost = 0
        for k in keypad:
            if k == "A":
                key = NumKeys.A
            else:
                key = NumKeys(int(k))
            num_sequences = move_numeric(numerical_robot, key)
            best_cost: int | None = None
            best_sequences: list[list[set[tuple[DirectionKeys, ...]]]] = []
            for n_sequence in num_sequences:
                seq_cost = 0
                seq: list[set[tuple[DirectionKeys, ...]]] = []
                t_robot_1 = directional_robot_1
                for move in n_sequence:
                    cost, dir_sequences = move_directional(t_robot_1, move)
                    seq.append(dir_sequences)
                    seq_cost += cost
                    t_robot_1 = move
                if best_cost is None or seq_cost <= best_cost:
                    best_cost = seq_cost
                    best_sequences.append(seq)
                
            best_tot = None    
            for best_sequence in best_sequences:
                tot = 0
                for next_key in best_sequence:
                    best_cost: int | None = None
                    for alternative in next_key:
                        cost = 0
                        t_robot_2 = directional_robot_2
                        for move in alternative:
                            m_cost, dir_sequences = move_directional(t_robot_2, move)
                            cost += m_cost
                            t_robot_2 = move
                        if best_cost is None or cost < best_cost:
                            best_cost = cost
                    if best_cost is None:
                        print("Error!")
                        return
                    tot += best_cost
                if best_tot is None or tot < best_tot:
                    best_tot = tot
            if best_tot is None:
                print("Error!")
                return
            tot_cost += best_tot
    
            numerical_robot = key
        s += tot_cost * int(keypad.removesuffix("A"))
    return s

def part_2(data: Data):
    pass

def parse_data(file: str):
    data: Data = []
    with open(file, "r") as f:
        for line in f:
            data.append(line.strip())
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
