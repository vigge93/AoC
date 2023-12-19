import time
from itertools import pairwise

day = 9


def part_1_and_2(data):
    s_p1 = 0
    s_p2 = 0
    for series in data:
        intermediate_series = []
        while any(series):
            new_series = []
            for l, r in pairwise(series):
                new_series.append(r - l)
            intermediate_series.append(series)
            series = new_series
        next_value_p1, next_value_p2 = 0, 0

        for inter_series in intermediate_series[::-1]:
            next_value_p1 = inter_series[-1] + next_value_p1
            next_value_p2 = inter_series[0] - next_value_p2
        s_p1 += next_value_p1
        s_p2 += next_value_p2
    return s_p1, s_p2


def parse_data():
    data = []
    with open(f"day{day}.txt", "r") as f:
        for line in f:
            data.append([int(val) for val in line.strip().split()])
    return data


if __name__ == "__main__":
    start_time = time.perf_counter_ns()
    data = parse_data()
    data_time = time.perf_counter_ns()
    p1, p2 = part_1_and_2(data)
    end_time = time.perf_counter_ns()
    print(
        f"""=== Day {day:02} ===\n"""
        f"""  · Loading data\n"""
        f"""  · Elapsed: {(data_time - start_time)/10**6:.3f} ms\n\n"""
        f"""  · Part 1: {p1}\n"""
        f"""  · Part 2: {p2}\n\n"""
        f"""  · Elapsed: {(end_time - data_time)/10**6:.3f} ms\n\n"""
        f"""  · Total elapsed: {(end_time - start_time)/10**6:.3f} ms"""
    )
