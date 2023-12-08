import time
from copy import deepcopy

day = 20

class Node:
    def __init__(self, value, prev):
        self.prev = prev
        self.value = value
        if prev:
            prev.next = self

    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev
    def __repr__(self) -> str:
        return f'<Node value: {self.value}>'

def part_1(data: "list[Node]"):
    unsorted = data[:]
    for node in unsorted:
        value = node.value
        if (abs(value) % len(data)) != 0:
            next_node = node
            node.remove()
            for _ in range(abs(value) % (len(data)-1)):
                if value > 0:
                    next_node = next_node.next
                else:
                    next_node = next_node.prev
            if value > 0:
                node.next = next_node.next
                node.prev = next_node
                next_node.next = node
                node.next.prev = node
            else:
                node.next = next_node
                node.prev = next_node.prev
                next_node.prev = node
                node.prev.next = node
    node = unsorted[0]
    while node.value != 0:
        node = node.next
    s = 0
    for i in range(1, 3001):
        node = node.next
        if i % 1000 == 0:
            s += node.value
    return s

def part_2(data):
    unsorted = data[:]
    for node in unsorted:
        node.value *= 811589153
    for _ in range(10):
        for node in unsorted:
            # if i % 100 == 0:
            #     print(i)
            # node = unsorted[i]
            # idx = node.idx
            value = node.value
            if (abs(value) % len(data)) != 0:
                next_node = node
                node.remove()
                for _ in range(abs(value) % (len(data)-1)):
                    if value > 0:
                        next_node = next_node.next
                    else:
                        next_node = next_node.prev
                if value > 0:
                    node.next = next_node.next
                    node.prev = next_node
                    next_node.next = node
                    node.next.prev = node
                else:
                    node.next = next_node
                    node.prev = next_node.prev
                    next_node.prev = node
                    node.prev.next = node
    node = unsorted[0]
    while node.value != 0:
        node = node.next
    s = 0
    for i in range(1, 3001):
        node = node.next
        if i % 1000 == 0:
            s += node.value
    return s

def parse_data():
    data1 = []
    data2 = []
    with open(f'day{day}.txt', 'r') as f:
        prev1 = None
        prev2 = None
        for line in f:
            val = int(line.strip())
            node1 = Node(val, prev1)
            node2 = Node(val, prev2)
            prev1 = node1
            prev2 = node2
            data1.append(node1)
            data2.append(node2)
        data1[-1].next = data1[0]
        data2[-1].next = data2[0]
        data1[0].prev = data1[-1]
        data2[0].prev = data2[-1]
    return data1, data2

if __name__ == '__main__':
    start_time = time.perf_counter_ns()
    data1, data2 = parse_data()
    p1 = part_1(data1)
    p2 = part_2(data2)
    end_time = time.perf_counter_ns()
    print(f'=== Day {day:02} ===')
    print(f'  · Part 1: {p1}')
    print(f'  · Part 2: {p2}')
    print(f"  · Elapsed: {(end_time - start_time)/10**6:.3f} ms")