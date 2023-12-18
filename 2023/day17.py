import time
from dataclasses import dataclass
from enum import IntEnum
from heapq import heappush, heappop

day = 17

class Direction(IntEnum):
    START = 0
    EAST = 1
    WEST = -1
    SOUTH = 2
    NORTH = -2

DIRECTION_MAP = {
    (-1, 0): Direction.WEST,
    (1, 0): Direction.EAST,
    (0, -1): Direction.NORTH,
    (0, 1): Direction.SOUTH
}

@dataclass
class Node():
    x: int
    y: int
    direction: Direction
    chain: int
    
    @property
    def coords(self):
        return (self.x, self.y)
    
    def __eq__(self, other: "Node"):
        return (
            self.x == other.x
            and self.y == other.y 
            and self.direction == other.direction
            and self.chain == other.chain
        )
    
    def __lt__(self, other: "Node"):
        return self.y < other.y or self.x < other.x or self.chain < other.chain or self.direction < other.direction
    
    def __hash__(self) -> int:
        return hash((self.x, self.y, self.direction, self.chain))

def a_star(grid, start_: tuple[int, int], goal: tuple[int, int], min_chain, max_chain):
    '''Function to calculate a path through a grid.'''
    # Initialize sets
    start = Node(*start_, Direction.START, 0)
    open_heap: list[tuple[int, Node]] = []
    heappush(open_heap, (heuristic(start.coords, goal), start))
    closed_set: set[Node] = set()
    came_from = {}
    g_score = {start: 0}

    counter = 0
    while len(open_heap) > 0:
        # Get the next node with the lowest f-score that is in the open set
        _, current = heappop(open_heap)
        # print(len(open_set))
        # print(current.coords)
        # We have reached the goal, return the reconstructed path
        if current.coords == goal and current.chain >= min_chain:
            return g_score[current]
            # return reconstruct_path(came_from, current)

        # Move the current node from the open set to the closed set
        closed_set.add(current)

        # Get all the non-blocked neighbors not in the closed set
        neighbors: dict[Node, int] = {}
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j or i * j != 0:
                    continue
                new_coords = (current.x + i, current.y + j)
                direction = (new_coords[0] - current.x, new_coords[1] - current.y)
                node = Node(*new_coords, DIRECTION_MAP[direction], current.chain)
                if current.direction == node.direction:
                    node.chain += 1
                elif node.chain < min_chain and current.direction != Direction.START:
                    continue
                else:
                    node.chain = 0
                
                if current.direction == -node.direction or node.chain >= max_chain:
                    continue
                # Only consider the horizontal and vertical neighbors
                if node.coords in grid and node not in closed_set:
                    neighbors[node] = grid[node.coords]
        counter += 1
        for neighbor in neighbors:
            # Calculate new g-score
            tentative_g_score = g_score[current] + neighbors[neighbor]

            # If g-score is better than previous g-scores,
            # or the node doesn't have a previous g-score,
            # update the path
            if neighbor not in g_score \
                    or tentative_g_score < g_score[neighbor]:
                # Update the path and g-score
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score

                # Calculate new f-score
                f_score = g_score[neighbor] \
                    + heuristic(neighbor.coords, goal)

                # Ensure neighbor is in the open set
                heappush(open_heap, (f_score, neighbor))
    # If no path is found, return None
    return None

def heuristic(node, goal):
    '''Calculates the manhattan distance from the current node to the goal.'''
    # |x1 - x2| + |y1 - y2|
    dist = abs(node[0] - goal[0]) + abs(node[1] - goal[1])
    return dist

def reconstruct_path(came_from, current):
    '''Reconstructs the path by working backwards'''
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path

def part_1(data):
    return a_star(data, (0, 0), max(data), 0, 3)

def part_2(data):
    return a_star(data, (0, 0), max(data), 3, 10)

def parse_data():
    data = {}
    with open(f'day{day}.txt', 'r') as f:
        for y, row in enumerate(f):
            for x, crucible in enumerate(row.strip()):
                data[(x, y)] = int(crucible)
    return data

if __name__ == '__main__':
    start_time = time.perf_counter_ns()
    data = parse_data()
    data_time = time.perf_counter_ns()
    p1 = part_1(data)
    p1_time = time.perf_counter_ns()
    p2 = part_2(data)
    end_time = time.perf_counter_ns()
    print(f'''=== Day {day:02} ===\n'''
    f'''  · Loading data\n'''
    f'''  · Elapsed: {(data_time - start_time)/10**6:.3f} ms\n\n'''
    f'''  · Part 1: {p1}\n'''
    f'''  · Elapsed: {(p1_time - data_time)/10**6:.3f} ms\n\n'''
    f'''  · Part 2: {p2}\n'''
    f'''  · Elapsed: {(end_time - p1_time)/10**6:.3f} ms\n\n'''
    f'''  · Total elapsed: {(end_time - start_time)/10**6:.3f} ms''')