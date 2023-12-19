import math
import time

day = 6


def part_1(data):
    res = 1
    for time, distance in data[1:]:
        # s = v*t_release
        # v = t_hold
        # t_gold = t - t_release
        # v = t - t_release
        # s = (t - t_release)*t_release = - t_release**2 + t*t_release
        # -t_release**2 + t*t_release - s = 0
        # t_release**2 - t*t_release + s = 0
        # t_release = t/2 +- sqrt((t/2)^2 - s)
        c_1 = time / 2
        c_2 = math.sqrt(c_1 * c_1 - distance)
        t_release_1 = int(c_1 - c_2)
        t_release_2 = int(c_1 + c_2)
        res *= t_release_2 - t_release_1
    return res


def part_2(data):
    res = 1
    time, distance = data[0]
    c_1 = time / 2
    c_2 = math.sqrt(c_1 * c_1 - distance)
    t_release_1 = int(c_1 - c_2)
    t_release_2 = int(c_1 + c_2)
    res *= t_release_2 - t_release_1
    return res


def parse_data():
    # data = []
    # with open(f'day{day}.txt', 'r') as f:
    #     times = f.readline().strip()
    #     distances = f.readline().strip()
    #     times = times.split(':')[1]
    #     distances = distances.split(':')[1]
    #     data.append((int(times.strip().replace(' ', '')), int(distances.strip().replace(' ', ''))))
    #     times = [int(time) for time in times.split()]
    #     distances = [int(distance) for distance in distances.split()]
    #     data += zip(times, distances)
    data = (
        (41_77_70_96, 249_1362_1127_1011),
        (41, 249),
        (77, 1362),
        (70, 1127),
        (96, 1011),
    )
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
