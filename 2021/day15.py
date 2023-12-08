import math
grid = []

def a_star(grid, start, goal):
    '''Function to calculate a path through a grid.'''
    # Create a dictionary with the non-blocked nodes
    available_nodes = {}
    for i, row in enumerate(grid):
        for j, state in enumerate(row):
            available_nodes[(j, i)] = state

    # Initialize sets
    open_set = {start: grid[start[1]][start[0]]}
    closed_set = {}
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while len(open_set) > 0:
        # Get the next node with the lowest f-score that is in the open set
        current = min([x for x in f_score if x in open_set],
                      key=lambda x: f_score[x])
        print(current)
        # We have reached the goal, return the reconstructed path
        if current == goal:
            return g_score[current]

        # Move the current node from the open set to the closed set
        del open_set[current]
        closed_set[current] = grid[current[1]][current[0]]

        # Get all the non-blocked neighbors not in the closed set
        neighbors = {}
        for i in range(-1, 2):
            for j in range(-1, 2):
                node = (current[0] + i, current[1] + j)
                # Only consider the horizontal and vertical neighbors
                if not i == j and not i * j != 0:
                    if node in available_nodes and node not in closed_set:
                        neighbors[node] = available_nodes[node]

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
                f_score[neighbor] = g_score[neighbor] \
                    + heuristic(neighbor, goal)

                # Ensure neighbor is in the open set
                if neighbor not in open_set:
                    open_set[neighbor] = neighbors[neighbor]
    # If no path is found, return None
    return None

def heuristic(node, goal):
    '''Calculates the manhattan distance from the current node to the goal.'''
    # |x1 - x2| + |y1 - y2|
    dist = abs(node[0] - goal[0]) + abs(node[1] - goal[1])
    return dist

with open('day15.txt', 'r') as f:
    for line in f:
        row = [int(x) for x in line.strip()]
        grid.append(row)

grid2 = grid[:]
grid3 = grid[:]
for i in range(4):
    for j, row in enumerate(grid2):
        grid3[j] = grid3[j][:]
        grid2[j] =grid2[j][:]
        newRow = [max((x + 1) % 10, 1) for x in row]
        grid3[j] = grid3[j] + newRow
        grid2[j] = newRow
grid2 = grid3
for j in range(4):
    newGrid = []
    for row in grid2:
        row2 = [max((x + 1) % 10, 1) for x in row]
        newGrid.append(row2)
    grid3 = grid3 + newGrid
    grid2 = newGrid
grid = grid3

print(a_star(grid, (0, 0), (len(grid[0]) - 1, len(grid) - 1)))