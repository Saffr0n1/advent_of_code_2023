from collections import deque
from dataclasses import dataclass

NUM_ROWS, NUM_COLS = 0, 0


@dataclass
class Beam:
    r: int
    c: int
    dir_r: int
    dir_c: int

    def __eq__(self, other):
        if isinstance(other, Beam):
            return (
                self.r == other.r
                and self.c == other.c
                and self.dir_r == other.dir_r
                and self.dir_c == other.dir_c
            )
        return False

    def __hash__(self):
        return hash((self.r, self.c, self.dir_r, self.dir_c))


def is_active(beam: Beam):
    global NUM_ROWS, NUM_COLS
    if beam.c < 0 or beam.c >= NUM_COLS or beam.r < 0 or beam.r >= NUM_ROWS:
        return False
    return True


def get_energized(visited_matrix):
    return sum(sum(row) for row in visited_matrix)


def fill_contraption(grid, start):
    global NUM_ROWS, NUM_COLS
    visited = set()
    visited_matrix = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    queue = deque([start])

    while queue:
        curr_beam = queue.popleft()
        new_r = curr_beam.r + curr_beam.dir_r
        new_c = curr_beam.c + curr_beam.dir_c
        if is_active(Beam(new_r, new_c, curr_beam.dir_r, curr_beam.dir_c)):
            curr_space = grid[new_r][new_c]
            visited_matrix[new_r][new_c] = 1
            if (
                curr_space == "."
                or (curr_space == "|" and curr_beam.dir_r != 0)
                or (curr_space == "-" and curr_beam.dir_c != 0)
            ):
                if Beam(new_r, new_c, curr_beam.dir_r, curr_beam.dir_c) not in visited:
                    visited.add(Beam(new_r, new_c, curr_beam.dir_r, curr_beam.dir_c))
                    queue.append(Beam(new_r, new_c, curr_beam.dir_r, curr_beam.dir_c))
            elif curr_space == "/":
                dir_r, dir_c = -curr_beam.dir_c, -curr_beam.dir_r
                if Beam(new_r, new_c, dir_r, dir_c) not in visited:
                    visited.add(Beam(new_r, new_c, dir_r, dir_c))
                    queue.append(Beam(new_r, new_c, dir_r, dir_c))
            elif curr_space == "\\":
                dir_r, dir_c = curr_beam.dir_c, curr_beam.dir_r
                if Beam(new_r, new_c, dir_r, dir_c) not in visited:
                    visited.add(Beam(new_r, new_c, dir_r, dir_c))
                    queue.append(Beam(new_r, new_c, dir_r, dir_c))
            else:
                for dir_r, dir_c in (
                    [(1, 0), (-1, 0)] if curr_space == "|" else [(0, 1), (0, -1)]
                ):
                    if Beam(new_r, new_c, dir_r, dir_c) not in visited:
                        visited.add(Beam(new_r, new_c, dir_r, dir_c))
                        queue.append(Beam(new_r, new_c, dir_r, dir_c))

    return visited_matrix


def custom_start(grid):
    global NUM_ROWS, NUM_COLS
    max_energized = 0

    for r in range(NUM_ROWS):
        max_energized = max(
            max_energized, get_energized(fill_contraption(grid, Beam(r, -1, 0, 1)))
        )
        max_energized = max(
            max_energized,
            get_energized(fill_contraption(grid, Beam(r, NUM_COLS, 0, -1))),
        )

    for c in range(NUM_ROWS):
        max_energized = max(
            max_energized, get_energized(fill_contraption(grid, Beam(-1, c, 1, 0)))
        )
        max_energized = max(
            max_energized,
            get_energized(fill_contraption(grid, Beam(NUM_ROWS, c, -1, 0))),
        )

    return max_energized


if __name__ == "__main__":
    fpath = r"path_to_file.txt"
    with open(fpath, "r") as file:
        grid = [line.strip() for line in file.readlines()]

    NUM_ROWS, NUM_COLS = len(grid), len(grid[0])
    visited_matrix = fill_contraption(grid, start=Beam(0, -1, 0, 1))

    print(f"Part 1 solution: {get_energized(visited_matrix)}")
    print(f"Part 1 solution: {custom_start(grid)}")
