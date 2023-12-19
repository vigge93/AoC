import time

day = 2


def part_1(data):
    MAX_RED = 12
    MAX_GREEN = 13
    MAX_BLUE = 14
    s = 0
    for game in data:
        valid_game = True
        for round in game["rounds"]:
            if (
                round["red"] > MAX_RED
                or round["green"] > MAX_GREEN
                or round["blue"] > MAX_BLUE
            ):
                valid_game = False
                break
        if valid_game:
            s += game["id"]
    return s


def part_2(data):
    s = 0
    for game in data:
        min_red = 0
        min_blue = 0
        min_green = 0
        for round in game["rounds"]:
            min_red = max(min_red, round["red"])
            min_green = max(min_green, round["green"])
            min_blue = max(min_blue, round["blue"])
        power = min_red * min_green * min_blue
        s += power
    return s


def parse_data():
    data = []
    with open(f"day{day}.txt", "r") as f:
        for line in f:
            line = line.strip()
            game = {}
            id, cubes = line.split(":")
            game["id"] = int(id)
            game["rounds"] = []
            rounds = cubes.split(";")
            for round in rounds:
                cubes = {"red": 0, "green": 0, "blue": 0}
                cubes_str = round.split(",")
                for cube in cubes_str:
                    _, amount, color = cube.split(" ")
                    cubes[color] = int(amount)
                game["rounds"].append(cubes)
            data.append(game)
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
