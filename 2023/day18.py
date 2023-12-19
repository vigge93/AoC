import time

import numpy as np
import numpy.typing as np_t

day = 18

direction_map: dict[str, tuple[int, int]] = {
    "L": (-1, 0),
    "R": (1, 0),
    "U": (0, -1),
    "D": (0, 1),
}

hex_direction_map = {0: "R", 1: "D", 2: "L", 3: "U"}


def part_1(data: list[tuple[str, int, str]]):
    current = (0, 0)
    xs = []
    ys = []
    edge_len = 0
    for direction, steps, _ in data:
        x_off, y_off = direction_map[direction]
        new_x = current[0] + x_off * steps
        new_y = current[1] + y_off * steps
        xs.append(new_x)
        ys.append(new_y)
        edge_len += steps
        current = (new_x, new_y)
    return int(
        PolyArea(np.array(xs, dtype="i8"), np.array(ys, dtype="i8")) + edge_len / 2 + 1
    )


def part_2(data: list[tuple[str, int, str]]):
    transformed_data: list[tuple[str, int, str]] = []
    for _, _, hex_code in data:
        hex_num_s, direction = hex_code[1:6], hex_code[-1]
        direction = hex_direction_map[int(direction)]
        hex_num = int(hex_num_s, base=16)
        transformed_data.append((direction, hex_num, hex_code))
    return part_1(transformed_data)


def PolyArea(x: np_t.NDArray, y: np_t.NDArray) -> float:
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def parse_data():
    data = []
    with open(f"day{day}.txt", "r") as f:
        for line in f:
            direction, distance, color = line.strip().split()
            data.append((direction, int(distance), color[1:-1]))
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
