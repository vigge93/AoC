import time

day = 2

def part_1(data):
    score = 0
    scores = {'A': 1, 'B': 2, 'C': 3, 'X': 1, 'Y': 2, 'Z': 3}
    for move in data:
        score += scores[move[1]]
        if (scores[move[0]] == 1 and scores[move[1]] == 2 or
            scores[move[0]] == 2 and scores[move[1]] == 3 or
            scores[move[0]] == 3 and scores[move[1]] == 1):
            score += 6
        elif scores[move[0]] == scores[move[1]]:
            score += 3
    return score

def part_2(data):
    score = 0
    scores = {'A': 1, 'B': 2, 'C': 3}
    for move in data:
        if move[1] == 'Z':
            m = (scores[move[0]]%3) + 1
            score += 6
        elif move[1] == 'Y':
            m = scores[move[0]]
            score += 3
        else:
            m = (scores[move[0]]+2)%3
            if m == 0: m = 3
        score += m
    return score

def parse_data():
    data = []
    with open(f'day{day}.txt', 'r') as f:
        for line in f:
            data.append((line.strip().split(' ')))
    return data

if __name__ == '__main__':
    start_time = time.perf_counter_ns()
    data = parse_data()
    p1 = part_1(data)
    p2 = part_2(data)
    end_time = time.perf_counter_ns()
    print(f'=== Day {day:02} ===')
    print(f'  · Part 1: {p1}')
    print(f'  · Part 2: {p2}')
    print(f"  · Elapsed: {(end_time - start_time)/10**6:.3f} ms")