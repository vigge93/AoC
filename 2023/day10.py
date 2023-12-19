import time
from itertools import batched

day = 10


def get_directions(pipe):
    directions = []
    if pipe in ("-", "L", "F"):
        directions.append((1, 0))
    if pipe in ("-", "J", "7"):
        directions.append((-1, 0))
    if pipe in ("|", "F", "7"):
        directions.append((0, 1))
    if pipe in ("|", "J", "L"):
        directions.append((0, -1))
    return directions


def part_1(data):
    start = data["start"]
    start_x, start_y = start
    if data[(start_x - 1, start_y)] in ("-", "L", "F"):
        current = (start_x - 1, start_y)
    elif data[(start_x + 1, start_y)] in ("-", "J", "7"):
        current = (start_x + 1, start_y)
    elif data[(start_x, start_y - 1)] in ("|", "F", "7"):
        current = (start_x, start_y - 1)
    elif data[(start_x, start_y + 1)] in ("|", "J", "L"):
        current = (start_x, start_y + 1)
    loop_len = 1
    visited = {start, current}
    while current != start:
        current_x, current_y = current
        for direction_x, direction_y in get_directions(data[current]):
            newCurrent = (current_x + direction_x, current_y + direction_y)
            if newCurrent not in visited or (newCurrent == start and loop_len > 1):
                current = newCurrent
                visited.add(newCurrent)
                loop_len += 1
                break
    return loop_len // 2


def part_2(data):
    start = data["start"]
    start_x, start_y = start
    if data[(start_x - 1, start_y)] in ("-", "L", "F"):
        current = (start_x - 1, start_y)
    elif data[(start_x + 1, start_y)] in ("-", "J", "7"):
        current = (start_x + 1, start_y)
    elif data[(start_x, start_y - 1)] in ("|", "F", "7"):
        current = (start_x, start_y - 1)
    elif data[(start_x, start_y + 1)] in ("|", "J", "L"):
        current = (start_x, start_y + 1)
    loop_len = 1
    visited_set = {start, current}
    while current != start:
        current_x, current_y = current
        for direction_x, direction_y in get_directions(data[current]):
            newCurrent = (current_x + direction_x, current_y + direction_y)
            if newCurrent not in visited_set or (newCurrent == start and loop_len > 1):
                current = newCurrent
                visited_set.add(newCurrent)
                loop_len += 1
                break
    visited_list = sorted(list(visited_set))
    prev_visited = visited_list[0]
    prev_prev_visited = visited_list[0]
    inside = data[prev_visited] == "-"
    inside_start = prev_visited if inside else None
    enclosed = 0
    for visited in visited_list[1:]:
        if visited[0] != prev_visited[0]:  # New column
            prev_visited = visited
            prev_prev_visited = visited
            inside = data[visited] == "-"
            inside_start = visited if inside else None
            continue

        if data[visited] == "|":
            prev_visited = visited
            continue
        if data[prev_visited] != "-" and data[visited] != "-":
            if data[prev_prev_visited] == "F" and data[visited] == "J":
                inside = not inside
                if not inside:
                    visited = prev_prev_visited
            if data[prev_prev_visited] == "7" and data[visited] == "L":
                inside = not inside
                if not inside:
                    visited = prev_prev_visited

        if data[visited] == "-":
            inside = not inside

        if inside and inside_start is None:
            inside_start = visited
        elif not inside and inside_start is not None:
            for enclosed_space in range(inside_start[1], visited[1]):
                if (visited[0], enclosed_space) not in visited_set:
                    enclosed += 1
            inside_start = None

        prev_visited = visited
        prev_prev_visited = visited

    return enclosed


def parse_data():
    data = {}
    with open(f"day{day}.txt", "r") as f:
        for y, line in enumerate(f):
            for x, pipe in enumerate(line):
                if pipe == "S":
                    data["start"] = (x, y)
                data[(x, y)] = pipe
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
