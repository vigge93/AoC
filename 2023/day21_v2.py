from collections import deque
import numpy as np

FILENAME = "day21.txt"
DIRECTIONS = [(-1, 0), (0, -1), (0, 1), (1, 0)]
ROCK = "#"


def expand_matrix(matrix, factor):
    return [
        [
            matrix[i % len(matrix)][j % len(matrix[0])]
            for j in range(factor * len(matrix[0]))
        ]
        for i in range(factor * len(matrix))
    ]


def is_valid(matrix, row, col):
    return (
        0 <= row < len(matrix)
        and 0 <= col < len(matrix[0])
        and matrix[row][col] != ROCK
    )


def bfs(matrix, start, step_count):
    visited = set()
    queue = deque([(start, 0)])
    while queue:
        (row, col), steps = queue.popleft()
        if steps > step_count:
            continue
        for dr, dc in DIRECTIONS:
            new_row, new_col = row + dr, col + dc
            if is_valid(matrix, new_row, new_col) and (new_row, new_col) not in visited:
                visited.add((new_row, new_col))
                queue.append(((new_row, new_col), steps + 1))
    return len(
        [(row, col) for row, col in visited if (row + col) % 2 == step_count % 2]
    )


def main():
    with open(FILENAME) as input_file:
        matrix = input_file.read().split("\n")
    start = len(matrix) // 2, len(matrix) // 2
    visited = bfs(matrix, start, 64)
    print(visited)

    expanded = expand_matrix(matrix, 5)
    start = len(expanded) // 2, len(expanded) // 2
    y_values = [bfs(expanded, start, step_count) for step_count in [65, 196, 327]]
    print(y_values)
    # 65, 65 + 131, 65 + 131 * 2
    x_values = np.array([0, 1, 2])

    target = (26501365 - 65) // 131
    coefficients = np.polyfit(x_values, y_values, 2)
    result = np.polyval(coefficients, target)
    print(np.round(result, 0))


if __name__ == "__main__":
    main()
