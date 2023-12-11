from dataclasses import dataclass


@dataclass
class Graph:
    X: int
    Y: int
    graph: list[str]
    s_x: int
    s_y: int
    path: list[list]


dirs = {
    "U": [(-1, 0), "|F7"],
    "D": [(1, 0), "|LJ"],
    "R": [(0, 1), "-J7"],
    "L": [(0, -1), "-LF"],
}

next_dir = {
    ("U", "|"): "U",
    ("U", "F"): "R",
    ("U", "7"): "L",
    ("D", "|"): "D",
    ("D", "L"): "R",
    ("D", "J"): "L",
    ("R", "-"): "R",
    ("R", "J"): "U",
    ("R", "7"): "D",
    ("L", "-"): "L",
    ("L", "L"): "U",
    ("L", "F"): "D",
}


def part1(pipes: Graph):
    pipes.path[pipes.s_y][pipes.s_x] = 1  # For Part 2

    starts = []
    for dir in dirs.keys():
        x = pipes.s_x + dirs[dir][0][1]
        y = pipes.s_y + dirs[dir][0][0]
        if (
            x >= 0
            and x <= X
            and y >= 0
            and y <= Y
            and pipes.graph[y][x] in dirs[dir][1]
        ):
            starts.append(dir)

    # Can take either starting direction
    move_dir = starts[0]
    print(starts)
    n_x = pipes.s_x + dirs[move_dir][0][1]
    n_y = pipes.s_y + dirs[move_dir][0][0]
    path_length = 1
    pipes.path[n_y][n_x] = 1  # For Part 2

    while n_x != pipes.s_x or n_y != pipes.s_y:
        move_dir = next_dir[(move_dir, pipes.graph[n_y][n_x])]  # type: ignore
        n_x = n_x + dirs[move_dir][0][1]
        n_y = n_y + dirs[move_dir][0][0]
        pipes.path[n_y][n_x] = 1  # For Part 2
        path_length += 1

    return path_length // 2


def part2(pipes: Graph):
    enclosed_tiles = 0
    for y in range(pipes.Y):
        parity = 0
        for x in range(pipes.X):
            if pipes.path[y][x] == 1:
                if pipes.graph[y][x] in "|JL":
                    parity = not parity
            else:
                enclosed_tiles += parity

    return enclosed_tiles


if __name__ == "__main__":
    fpath = r"path_to_file.txt"
    with open(fpath, "r") as file:
        input = [(line[:-1] if "\n" in line else line) for line in file.readlines()]

    X, Y = len(input[0]), len(input)

    s_x, s_y = -1, -1
    for x in range(Y):
        for y in range(X):
            if input[y][x] == "S":
                s_x, s_y = x, y

    pipes = Graph(
        X=X,
        Y=Y,
        graph=input,
        s_x=s_x,
        s_y=s_y,
        path=[[0] * X for _ in range(Y)],  # For the points that are on our path
    )

    print(f"Part 1 solution: {part1(pipes)}")
    print(f"Part 2 solution: {part2(pipes)}")
