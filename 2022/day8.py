import time

day = 8

def part_1(data):
    count = 0
    for y, row in enumerate(data):
        for x, tree in enumerate(row):
            visible = True
            for l in range(0, x): # Left
                if data[y][l] >= tree:
                    visible = False
                    break
            if visible:
                count += 1
                continue
            visible = True
            for r in range(x+1, len(row)): # Right
                if data[y][r] >= tree:
                    visible = False
                    break
            if visible:
                count += 1
                continue
            visible = True
            for u in range(0, y): # Up
                if data[u][x] >= tree:
                    visible = False
                    break
            if visible:
                count += 1
                continue
            visible = True
            for d in range(y+1, len(data)): # Down
                if data[d][x] >= tree:
                    visible = False
                    break
            if visible:
                count += 1
    return count

def part_2(data):
    best_score = 0
    for y, row in enumerate(data):
        for x, tree in enumerate(row):
            score = 1
            for l in range(x-1, -1, -1): # Left
                if data[y][l] >= tree:
                    score *= (x - l)
                    break
            else:
                score *= x
            for r in range(x+1, len(row)): # Right
                if data[y][r] >= tree:
                    score *= (r - x)
                    break
            else:
                score *= (len(row) - x - 1)
            for u in range(y-1, -1, -1): # Up
                if data[u][x] >= tree:
                    score *= (y - u)
                    break
            else:
                score *= y
            for d in range(y+1, len(data)): # Down
                if data[d][x] >= tree:
                    score *= (d - y)
                    break
            else:
                score *= (len(data) - y - 1)
            best_score = max(score, best_score)
    return best_score
def parse_data():
    data = []
    with open(f'day{day}.txt', 'r') as f:
        for line in f:
            data.append([int(x) for x in line.strip()])
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