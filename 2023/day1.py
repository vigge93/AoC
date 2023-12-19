import re
import time

day = 1


def part_1(data):
    s = 0
    for line in data:
        first_num = None
        last_num = None
        for char in line:
            if char.isdigit():
                first_num = char
                break
        for char in line[::-1]:
            if char.isdigit():
                last_num = char
                break
        s += int(first_num + last_num)
    return s


def part_2(data):
    s = 0
    text_num_map = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    for line in data:
        rev_line = line[::-1]
        first_num = None
        last_num = None
        max_idx = len(line) + 1
        first_other_idx = max_idx
        last_other_idx = max_idx
        first_match = re.search(
            "(?:f(?:ive|our)|s(?:even|ix)|t(?:hree|wo)|eight|nine|one)", line
        )
        if first_match:
            first_other_idx = first_match.start()
            first_other_key = first_match.group(0)
        last_match = re.search(
            "(?:e(?:n(?:in|o)|erht|vif)|neves|thgie|ruof|owt|xis)", rev_line
        )
        if last_match:
            last_other_idx = last_match.start()
            last_other_key = last_match.group(0)[::-1]
        for idx, char in enumerate(line):
            if char.isdigit():
                if idx < first_other_idx:
                    first_num = char
                else:
                    first_num = text_num_map[first_other_key]
                break
        else:
            first_num = text_num_map[first_other_key]

        for idx, char in enumerate(rev_line):
            if char.isdigit():
                if idx < last_other_idx:
                    last_num = char
                else:
                    last_num = text_num_map[last_other_key]
                break
        else:
            last_num = text_num_map[last_other_key]
        s += int(first_num + last_num)
    return s


def parse_data():
    data = []
    with open(f"day{day}.txt", "r") as f:
        for line in f:
            data.append(line)
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
