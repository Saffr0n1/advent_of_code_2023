from collections import deque, defaultdict

global NUM_ROWS, NUM_COLS
global DIRS

# TODO: Part 2 here is a bit hacky as well. I heavily used the fact that our input
# grid had a garden boundary as well as no rocks on the row/column of `S`. This wasn't
# true for my test input. I'll come back someday with a generalized solution.


def get_neighbors(grid, r, c):
    neighbors = []
    for dir in DIRS:
        r_t, c_t = r + dir[0], c + dir[1]
        if (
            c_t < 0
            or c_t >= NUM_COLS
            or r_t < 0
            or r_t >= NUM_ROWS
            or grid[r_t][c_t] == "#"
        ):
            continue
        neighbors.append((r_t, c_t))
    return neighbors


def bfs(grid, start):
    visited = set()
    queue = deque([start])
    visited.add((start[0], start[1]))
    num_visited = 0

    while queue:
        node = queue.popleft()
        if node[2] % 2 == 0:
            num_visited += 1
        if node[2] == 0:
            continue
        for neighbor in get_neighbors(grid, node[0], node[1]):
            if neighbor not in visited:
                queue.append((neighbor[0], neighbor[1], node[2] - 1))
                visited.add(neighbor)

    return num_visited


if __name__ == "__main__":
    fpath = r"path_to_file.txt"
    with open(fpath, "r") as file:
        grid = tuple(tuple(line.strip()) for line in file.readlines())

    NUM_ROWS, NUM_COLS = len(grid), len(grid[0])
    DIRS = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    MAX_STEPS = 64
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if grid[r][c] == "S":
                START = (r, c, MAX_STEPS)

    num_visited = bfs(grid, START)
    print(f"Part 1 Solution: {num_visited}")

    MAX_STEPS = 26501365
    NUM_GRIDS = MAX_STEPS // NUM_ROWS - 1

    # Please draw a diagram out for yourself. I'm essentially breaking this down into
    # different 'types' of grids based on their parity with respect to the starting
    # grid and their position with respect to the boundary formed by the maximum
    # number of steps

    ODD_GRIDS = (NUM_GRIDS // 2 * 2 + 1) ** 2
    EVEN_GRIDS = ((NUM_GRIDS + 1) // 2 * 2) ** 2
    s_x, s_y = START[0], START[1]

    points_dict = defaultdict(int)
    points_dict["o"] = ODD_GRIDS * bfs(grid, (s_x, s_y, NUM_ROWS * 2 - 1))
    points_dict["e"] = EVEN_GRIDS * bfs(grid, (s_x, s_y, NUM_ROWS * 2))
    points_dict["corners"] = (
        bfs(grid, (NUM_ROWS - 1, s_y, NUM_ROWS - 1))
        + bfs(grid, (s_x, 0, NUM_ROWS - 1))
        + bfs(grid, (s_x, NUM_ROWS - 1, NUM_ROWS - 1))
        + bfs(grid, (0, s_y, NUM_ROWS - 1))
    )
    points_dict["less_than_half"] = (
        bfs(grid, (0, 0, NUM_ROWS // 2 - 1))
        + bfs(grid, (NUM_ROWS - 1, 0, NUM_ROWS // 2 - 1))
        + bfs(grid, (0, NUM_ROWS - 1, NUM_ROWS // 2 - 1))
        + bfs(grid, (NUM_ROWS - 1, NUM_ROWS - 1, NUM_ROWS // 2 - 1))
    )
    points_dict["more_than_half"] = (
        bfs(grid, (NUM_ROWS - 1, 0, NUM_ROWS * 3 // 2 - 1))
        + bfs(grid, (0, NUM_ROWS - 1, NUM_ROWS * 3 // 2 - 1))
        + bfs(grid, (NUM_ROWS - 1, NUM_ROWS - 1, NUM_ROWS * 3 // 2 - 1))
        + bfs(grid, (0, 0, NUM_ROWS * 3 // 2 - 1))
    )

    points_reached = (
        points_dict["o"]
        + points_dict["e"]
        + points_dict["corners"]
        + NUM_GRIDS * (points_dict["less_than_half"] + points_dict["more_than_half"])
        + points_dict["less_than_half"]
    )

    print(f"Part 2 Solution: {points_reached}")
