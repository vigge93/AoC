def find_basin(x, y, grid, visited):
    if (x, y) in visited or grid[x][y] == 9:
        return visited
    visited.add((x, y))
    if x > 0:
        find_basin(x - 1, y, grid, visited)
    if x < len(grid) - 1:
        find_basin(x + 1, y, grid, visited)
    if y > 0:
        find_basin(x, y - 1, grid, visited)
    if y < len(grid[0]) - 1:
        find_basin(x, y + 1, grid, visited)
    return visited

grid = []
min_points = []
with open('day9.txt', 'r') as f:
    for line in f:
        row = [int(x) for x in line.strip()]
        grid.append(row)

for i in range(len(grid)):
    for j in range(len(grid[i])):
        if i > 0 and grid[i][j] >= grid[i-1][j]:
            continue
        if i < len(grid) - 1 and grid[i][j] >= grid[i + 1][j]:
            continue
        if j > 0 and grid[i][j] >= grid[i][j-1]:
            continue
        if j < len(grid) - 1 and grid[i][j] >= grid[i][j + 1]:
            continue
        min_points.append((i, j))

basins = []
for min_point in min_points:
    visited = set()
    visited = find_basin(min_point[0], min_point[1], grid, visited)
    basins.append(visited)

basins.sort(key=lambda x: len(x), reverse=True)
basins = basins[:3]
print(len(basins[0])*len(basins[1])*len(basins[2]))