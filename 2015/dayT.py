import time

day = dayT


def part_1(data):
    pass


def part_2(data):
    pass


def parse_data():
    data = []
    with open(f"day{day}.txt", "r") as f:
        pass
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
