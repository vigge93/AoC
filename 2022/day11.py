import time
from copy import deepcopy

day = 11

class Monkey:
    __slots__ = ('items', 'operation','test', 'inspections')
    def __init__(self, items, operation, test):
        self.items = items
        self.operation = operation
        self.test = test
        self.inspections = 0
    
    def play_turn_part1(self, data):
        for item in self.items:
            item = self.operation(item) // 3
            new_idx = self.test(item)
            data[new_idx].items.append(item)
            self.inspections += 1
        self.items = []
    
    def play_turn_part2(self, data, mod):
        for item in self.items:
            item = self.operation(item) % mod
            new_idx = self.test(item)
            data[new_idx].items.append(item)
            self.inspections += 1
        self.items = []
 
def part_1(data):
    data = deepcopy(data)
    for _ in range(20):
        for monkey in data:
            monkey.play_turn_part1(data)
    data = sorted(data, key=lambda x: x.inspections, reverse=True)
    return data[0].inspections*data[1].inspections

def part_2(data):
    mod = 2*3*5*7*11*13*17*19
    data = deepcopy(data)
    for _ in range(10_000):
        for monkey in data:
            monkey.play_turn_part2(data, mod)
    data = sorted(data, key=lambda x: x.inspections, reverse=True)
    return data[0].inspections*data[1].inspections

def parse_data():
    data = [
        Monkey([83, 97, 95, 67], lambda x: x*19, lambda y: 2 if y%17==0 else 7),
        Monkey([71, 70, 79, 88, 56, 70], lambda x: x+2, lambda y: 7 if y%19==0 else 0),
        Monkey([98, 51, 51, 63, 80, 85, 84, 95], lambda x: x+7, lambda y: 4 if y%7==0 else 3),
        Monkey([77, 90, 82, 80, 79], lambda x: x+1, lambda y: 6 if y%11==0 else 4),
        Monkey([68], lambda x: x*5, lambda y: 6 if y%13==0 else 5),
        Monkey([60, 94], lambda x: x+5, lambda y: 1 if y%3==0 else 0),
        Monkey([81, 51, 85], lambda x: x*x, lambda y: 5 if y%5==0 else 1),
        Monkey([98, 81, 63, 65, 84, 71, 84], lambda x: x+3, lambda y: 2 if y%2==0 else 3)
    ]
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