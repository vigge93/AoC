import time

day = 22

QUAD_SIZE = 50

class Node():

    def __init__(self, x, y, blocked):
        self.north = None
        self.east = None
        self.south = None
        self.west = None
        self.x = x
        self.y = y
        self.blocked = blocked
    
    def __repr__(self) -> str:
        return f"<Node {self.x} {self.y}>"

def part_1(data):
    current = data['board']['start']
    directions = ['east', 'south', 'west', 'north']
    currentDirection = 0
    for move in data['moves']:
        if isinstance(move, str):
            if move == 'R':
                currentDirection = (currentDirection + 1) % 4
            elif move == 'L':
                currentDirection = (currentDirection - 1) % 4
        else:
            for _ in range(move):
                direction = directions[currentDirection]
                if direction == 'east':
                    if not current.east.blocked:
                        current = current.east
                    else:
                        break
                elif direction == 'south':
                    if not current.south.blocked:
                        current = current.south
                    else:
                        break
                elif direction == 'west':
                    if not current.west.blocked:
                        current = current.west
                    else:
                        break
                elif direction == 'north':
                    if not current.north.blocked:
                        current = current.north
                    else:
                        break
    return (current.y + 1)*1000 + (current.x + 1)*4 + currentDirection
        
                                
                

def part_2(data):
    current, _ = data['board']['start']
    directions = ['east', 'south', 'west', 'north']
    currentDirection = 0
    for move in data['moves']:
        if isinstance(move, str):
            if move == 'R':
                currentDirection = (currentDirection + 1) % 4
            elif move == 'L':
                currentDirection = (currentDirection - 1) % 4
        else:
            for _ in range(move):
                direction = directions[currentDirection]
                if direction == 'east':
                    if not current.east[0].blocked:
                        current, rotate = current.east
                        currentDirection = (currentDirection + rotate) % 4
                    else:
                        break
                elif direction == 'south':
                    if not current.south[0].blocked:
                        current, rotate = current.south
                        currentDirection = (currentDirection + rotate) % 4
                    else:
                        break
                elif direction == 'west':
                    if not current.west[0].blocked:
                        current, rotate = current.west
                        currentDirection = (currentDirection + rotate) % 4
                    else:
                        break
                elif direction == 'north':
                    if not current.north[0].blocked:
                        current, rotate = current.north
                        currentDirection = (currentDirection + rotate) % 4
                    else:
                        break
    return (current.y + 1)*1000 + (current.x + 1)*4 + currentDirection


def parse_data1(data, y, line, first_values_vertical, last_values_vertical, prev_row):
    prev_val = None
    first_val = None
    new_prev_row = {}
    line = line.rstrip()
    for x, char in enumerate(line):
        if char == ' ':
            continue
        blocked = False
        if char == '.':
            blocked = False
        elif char == '#':
            blocked = True
        node = Node(x, y, blocked)
        data['board'][(x, y)] = node
        if prev_val is not None:
            node.west = prev_val
            prev_val.east = node
        else:
            first_val = node
        if x in prev_row:
            node.north = prev_row[x]
            prev_row[x].south = node
        else:
            first_values_vertical[x] = node
        last_values_vertical[x] = node
        new_prev_row[x] = node
        prev_val = node
    first_val.west = node
    node.east = first_val
    if y == 0:
        data['board']['start'] = first_val
    return new_prev_row

def parse_data2(data, y, line, prev_row):
    prev_val = None
    new_prev_row = {}
    line = line.rstrip()
    first_val = None
    for x, char in enumerate(line):
        if char == ' ':
            continue
        blocked = False
        if char == '.':
            blocked = False
        elif char == '#':
            blocked = True
        node = Node(x, y, blocked)
        data['board'][(x, y)] = (node, 0)
        if prev_val is not None:
            node.west = (prev_val, 0)
            prev_val.east = (node, 0)
        else:
            first_val = (node, 0)
        if x in prev_row:
            node.north = (prev_row[x], 0)
            prev_row[x].south = (node, 0)
        prev_val = node
        new_prev_row[x] = node
    if y == 0:
        data['board']['start'] = first_val
    return new_prev_row

def parse_data():
    data1 = {'moves': [], 'board': {}}
    data2 = {'moves': [], 'board': {}}
    with open(f'day{day}.txt', 'r') as f:
        y = 0
        x = 0
        prev_row1 = {}
        prev_row2 = {}
        first_values_vertical1 = {}
        first_values_vertical2 = {}
        last_values_vertical1 = {}
        last_values_vertical2 = {}
        for line in f:
            if line.strip() == '':
                line = f.readline().strip()
                numbers = ''
                for ch in line:
                    if ch.isnumeric():
                        numbers += ch
                    else:
                        data1['moves'].append(int(numbers))
                        data1['moves'].append(ch)
                        numbers = ''
                if numbers != '':
                    data1['moves'].append(int(numbers))
                break

            prev_row1 = parse_data1(data1, y, line, first_values_vertical1, last_values_vertical1, prev_row1)
            prev_row2 = parse_data2(data2, y, line, prev_row2)

            y += 1
        for x in first_values_vertical1:
            first_values_vertical1[x].north = last_values_vertical1[x]
            last_values_vertical1[x].south = first_values_vertical1[x]
        data2['moves'] = data1['moves']
        for node, _ in data2['board'].values(): # Hard code wraps:
            quad = (node.x // QUAD_SIZE, node.y // QUAD_SIZE)
            if node.east is None:
                if quad[1] == 0:
                    connected_node, _ = data2['board'][(QUAD_SIZE*2 - 1, QUAD_SIZE*3 - 1 - node.y % QUAD_SIZE)]
                    node.east = (connected_node, 2)
                    connected_node.east = (node, 2)
                elif quad[1] == 1:
                    connected_node, _ = data2['board'][(QUAD_SIZE*2 + node.y % QUAD_SIZE, QUAD_SIZE - 1)]
                    node.east = (connected_node, 3)
                    connected_node.south = (node, 1)
                elif quad[1] == 3:
                    connected_node, _ = data2['board'][(QUAD_SIZE + node.y % QUAD_SIZE, QUAD_SIZE*3 - 1)]
                    node.east = (connected_node, 3)
                    connected_node.south = (node, 1)
            if node.south is None:
                if quad[0] == 0:
                    connected_node, _ = data2['board'][(QUAD_SIZE*2 + node.x % QUAD_SIZE, 0)]
                    node.south = (connected_node, 0)
                    connected_node.north = (node, 0)
            if node.west is None:
                if quad[1] == 0:
                    connected_node, _ = data2['board'][(0, QUAD_SIZE*3 - 1 - node.y % QUAD_SIZE)]
                    node.west = (connected_node, 2)
                    connected_node.west = (node, 2)
                elif quad[1] == 1:
                    connected_node, _ = data2['board'][(node.y % QUAD_SIZE, QUAD_SIZE*2)]
                    node.west = (connected_node, 3)
                    connected_node.north = (node, 1)
                elif quad[1] == 3:
                    connected_node, _ = data2['board'][(QUAD_SIZE + node.y % QUAD_SIZE, 0)]
                    node.west = (connected_node, 3)
                    connected_node.north = (node, 1)
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