from typing import List, Tuple

global NUM_R, NUM_C
global DIRS
global ARROW_TO_DIR
global START, END


def get_neighbors(grid, r, c, dry=False) -> List[Tuple[int, int]]:
    neighbors = []
    possible_dirs = DIRS
    if not dry and grid[r][c] != ".":
        possible_dirs = [ARROW_TO_DIR[grid[r][c]]]
    for dir in possible_dirs:
        r_t, c_t = r + dir[0], c + dir[1]
        if c_t < 0 or c_t >= NUM_C or r_t < 0 or r_t >= NUM_R or grid[r_t][c_t] == "#":
            continue
        if not dry and (
            (dir == [0, 1] and grid[r_t][c_t] == "<")
            or (dir == [0, -1] and grid[r_t][c_t] == ">")
            or (dir == [1, 0] and grid[r_t][c_t] == "^")
            or (dir == [-1, 0] and grid[r_t][c_t] == "v")
        ):
            continue
        neighbors.append((r_t, c_t))
    return neighbors


def contract_graph(grid, dry=False):
    edge_contraction: List[Tuple[int, int]] = [START, END]
    for r in range(NUM_R):
        for c in range(NUM_C):
            if grid[r][c] == "#":
                continue
            if len(get_neighbors(grid, r, c, True)) > 2:
                edge_contraction.append((r, c))

    contracted_graph = {node: {} for node in edge_contraction}

    for r, c in edge_contraction:
        stack = [(r, c, int(0))]
        visited = set()
        visited.add((r, c))

        while stack:
            r_i, c_i, l = stack.pop()
            if l != 0 and (r_i, c_i) in edge_contraction:
                contracted_graph[(r, c)][(r_i, c_i)] = l
                continue

            for r_t, c_t in get_neighbors(grid, r_i, c_i, dry):
                if (r_t, c_t) not in visited:
                    stack.append((r_t, c_t, l + 1))
                    visited.add((r_t, c_t))

    return contracted_graph


def dfs(contracted_graph, node, visited=None):
    if visited is None:
        visited = set()

    if node == END:
        return 0

    max_path_length = -float("inf")
    visited.add(node)
    for neighbor in contracted_graph[node]:
        if neighbor not in visited:
            max_path_length = max(
                max_path_length,
                dfs(contracted_graph, neighbor, visited)
                + contracted_graph[node][neighbor],
            )
    visited.remove(node)

    return max_path_length


if __name__ == "__main__":
    fpath = r"path_to_input.txt"
    with open(fpath, "r") as file:
        grid = tuple(tuple(line.strip()) for line in file.readlines())

    DIRS = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    ARROW_TO_DIR = {">": [0, 1], "<": [0, -1], "v": [1, 0], "^": [-1, 0]}
    NUM_R, NUM_C = len(grid), len(grid[0])
    START, END = (0, grid[0].index(".")), (NUM_R - 1, grid[NUM_R - 1].index("."))
    contracted_graph = contract_graph(grid)

    print(f"Part 1 Solution: {dfs(contracted_graph, START)}")

    dry_contraction = contract_graph(grid, True)
    print(f"Part 2 Solution: {dfs(dry_contraction, START)}")
