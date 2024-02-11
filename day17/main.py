from heapq import heappop, heappush
from dataclasses import dataclass

NUM_ROWS, NUM_COLS = 0, 0


@dataclass
class Crucible:
    r: int
    c: int
    dir_r: int
    dir_c: int
    straight_steps: int

    def __eq__(self, other):
        if isinstance(other, Crucible):
            return (
                self.r == other.r
                and self.c == other.c
                and self.dir_r == other.dir_r
                and self.dir_c == other.dir_c
                and self.straight_steps == other.straight_steps
            )
        return False

    def __hash__(self):
        return hash((self.r, self.c, self.dir_r, self.dir_c, self.straight_steps))

    # LOL
    def __lt__(self, other):
        return True


def is_active(crucible: Crucible):
    global NUM_ROWS, NUM_COLS
    if (
        crucible.c < 0
        or crucible.c >= NUM_COLS
        or crucible.r < 0
        or crucible.r >= NUM_ROWS
    ):
        return False
    return True


def get_part_params(part):
    if part == 1:
        return (0, 3)
    else:
        return (4, 10)


def dijkstra(graph, start, part):
    visited = set()
    min_heap = [(0, start)]

    END_STRAIGHT, MAX_STRAIGHT = get_part_params(part)

    while min_heap:
        heat_loss, curr_node = heappop(min_heap)
        if (
            curr_node.r == NUM_ROWS - 1
            and curr_node.c == NUM_COLS - 1
            and curr_node.straight_steps >= END_STRAIGHT
        ):
            return heat_loss
        if curr_node in visited:
            continue
        visited.add(curr_node)

        if curr_node.straight_steps < MAX_STRAIGHT and (
            curr_node.dir_r,
            curr_node.dir_c,
        ) != (
            0,
            0,
        ):
            new_node = Crucible(
                curr_node.r + curr_node.dir_r,
                curr_node.c + curr_node.dir_c,
                curr_node.dir_r,
                curr_node.dir_c,
                curr_node.straight_steps + 1,
            )
            if is_active(new_node):
                heappush(
                    min_heap, (heat_loss + graph[new_node.r][new_node.c], new_node)
                )

        if part == 1 or (
            curr_node.straight_steps >= 4
            or (curr_node.dir_r, curr_node.dir_c) == (0, 0)
        ):
            for dir_r, dir_c in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                if (curr_node.dir_r, curr_node.dir_c) != (dir_r, dir_c) and (
                    curr_node.dir_r,
                    curr_node.dir_c,
                ) != (-dir_r, -dir_c):
                    new_node = Crucible(
                        curr_node.r + dir_r,
                        curr_node.c + dir_c,
                        dir_r,
                        dir_c,
                        1,
                    )
                    if is_active(new_node):
                        heappush(
                            min_heap,
                            (heat_loss + graph[new_node.r][new_node.c], new_node),
                        )


if __name__ == "__main__":
    fpath = r"path_to_file.txt"
    with open(fpath, "r") as file:
        grid = [list(map(int, line.strip())) for line in file]

    NUM_ROWS, NUM_COLS = len(grid), len(grid[0])
    start = Crucible(0, 0, 0, 0, 0)
    print(f"Part 1 solution: {dijkstra(grid, start, 1)}")
    print(f"Part 2 solution: {dijkstra(grid, start, 2)}")
