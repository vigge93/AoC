import time
from copy import deepcopy

day = 23

class Elf():
    __slots__ = ['x', 'y', 'nextMove']
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.nextMove = None
    

    def move(self, data):
        if self.nextMove is None:
            return Elf(self.x, self.y)
        if self.nextMove == 'S':
            if Elf(self.x, self.y + 2) not in data or data[Elf(self.x, self.y + 2)].nextMove != 'N':
                return Elf(self.x, self.y + 1)
        elif self.nextMove == 'N':
            if Elf(self.x, self.y - 2) not in data or data[Elf(self.x, self.y - 2)].nextMove != 'S':
                return Elf(self.x, self.y - 1)
        elif self.nextMove == 'W':
            if Elf(self.x - 2, self.y) not in data or data[Elf(self.x - 2, self.y)].nextMove != 'E':
                return Elf(self.x - 1, self.y)
        elif self.nextMove == 'E':
            if Elf(self.x + 2, self.y) not in data or data[Elf(self.x + 2, self.y)].nextMove != 'W':
                return Elf(self.x + 1, self.y)
        return Elf(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f'<Elf x={self.x}, y={self.y}, nextMove={self.nextMove}>'

def part_1(data):
    data = deepcopy(data)
    considerations = ['N', 'S', 'W', 'E']
    for _ in range(10):
        # Part 1, calculate move
        for elf in data.values():
            # Check if alone
            alone = True
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x == y == 0:
                        continue
                    if Elf(elf.x + x, elf.y + y) in data:
                        alone = False
                        break
                if not alone:
                    break
            if alone:
                elf.nextMove = None
                continue
            for c in considerations:
                alone = True
                if c == 'N':
                    for x in range(-1, 2):
                        if Elf(elf.x + x, elf.y - 1) in data:
                            alone = False
                            break
                elif c == 'S':
                    for x in range(-1, 2):
                        if Elf(elf.x + x, elf.y + 1) in data:
                            alone = False
                            break
                elif c == 'W':
                    for y in range(-1, 2):
                        if Elf(elf.x - 1, elf.y + y) in data:
                            alone = False
                            break
                elif c == 'E':
                    for y in range(-1, 2):
                        if Elf(elf.x + 1, elf.y + y) in data:
                            alone = False
                            break
                if alone:
                    elf.nextMove = c
                    break
        new_data = {}
        for elf in data.values():
            new_elf = elf.move(data)
            new_data[new_elf] = new_elf
        data = new_data
        considerations.append(considerations.pop(0))
    minX = min(data.values(), key=lambda elf: elf.x).x
    maxX = max(data.values(), key=lambda elf: elf.x).x
    minY= min(data.values(), key=lambda elf: elf.y).y
    maxY= max(data.values(), key=lambda elf: elf.y).y
    count = 0
    for x in range(minX, maxX + 1):
        for y in range(minY, maxY + 1):
            if Elf(x, y) not in data:
                count += 1
    return count
def part_2(data):
    considerations = ['N', 'S', 'W', 'E']
    anyMoved = True
    step = 0
    while anyMoved:
        anyMoved = False
        # Part 1, calculate move
        for elf in data.values():
            # Check if alone
            alone = True
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x == y == 0:
                        continue
                    if Elf(elf.x + x, elf.y + y) in data:
                        anyMoved = True
                        alone = False
                        break
                if not alone:
                    break
            if alone:
                elf.nextMove = None
                continue
            for c in considerations:
                alone = True
                if c == 'N':
                    for x in range(-1, 2):
                        if Elf(elf.x + x, elf.y - 1) in data:
                            alone = False
                            break
                elif c == 'S':
                    for x in range(-1, 2):
                        if Elf(elf.x + x, elf.y + 1) in data:
                            alone = False
                            break
                elif c == 'W':
                    for y in range(-1, 2):
                        if Elf(elf.x - 1, elf.y + y) in data:
                            alone = False
                            break
                elif c == 'E':
                    for y in range(-1, 2):
                        if Elf(elf.x + 1, elf.y + y) in data:
                            alone = False
                            break
                if alone:
                    elf.nextMove = c
                    break
        new_data = {}
        for elf in data.values():
            new_elf = elf.move(data)
            new_data[new_elf] = new_elf
        data = new_data
        considerations.append(considerations.pop(0))
        step += 1
    # minX = min(data.values(), key=lambda elf: elf.x).x
    # maxX = max(data.values(), key=lambda elf: elf.x).x
    # minY= min(data.values(), key=lambda elf: elf.y).y
    # maxY= max(data.values(), key=lambda elf: elf.y).y
    # count = 0
    # for x in range(minX, maxX + 1):
    #     for y in range(minY, maxY + 1):
    #         if Elf(x, y) not in data:
    #             count += 1
    return step

def parse_data():
    data = {}
    with open(f'day{day}.txt', 'r') as f:
        for y, line in enumerate(f):
            for x, cell in enumerate(line.strip()):
                if cell == '#':
                    data[Elf(x, y)] = Elf(x, y)
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