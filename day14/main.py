from functools import cache


def tuple_to_list(t):
    return [list(l) for l in t]


def list_to_tuple(l):
    return tuple(tuple(t) for t in l)


@cache
def get_weight(matrix):
    max_score = len(matrix)
    weight = 0
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            if matrix[x][y] == "O":
                weight += max_score - x
    return weight


@cache
def shift(matrix):
    matrix = tuple_to_list(matrix)
    for y in range(len(matrix[0])):
        for _ in range(len(matrix)):
            for x in range(1, len(matrix)):
                if matrix[x][y] == "O" and matrix[x - 1][y] == ".":
                    matrix[x][y], matrix[x - 1][y] = ".", "O"
    return list_to_tuple(matrix)


@cache
def rotate_90_ccw(matrix):
    X, Y = len(matrix), len(matrix[0])
    return tuple(tuple(matrix[j][i] for j in range(X - 1, -1, -1)) for i in range(Y))


if __name__ == "__main__":
    fpath = r"/Users/saffron/Documents/Github/advent_of_code_2023/day14/input.txt"
    with open(fpath, "r") as file:
        lines = [line.strip() for line in file.readlines()]

    matrix = tuple(tuple(line) for line in lines)

    # PART 1
    print(f"Part 1 solution: {get_weight(shift(matrix))}")

    # Part 2
    NUM_CYCLES = 1_000_000_000
    c = 0
    matrix_cache = {}
    while c < NUM_CYCLES:
        c += 1
        for _ in range(4):
            matrix = rotate_90_ccw(shift(matrix))
        if matrix in matrix_cache:
            cycle_len = c - matrix_cache[matrix]
            rem_cycles = (NUM_CYCLES - c) // cycle_len
            c += cycle_len * rem_cycles
        matrix_cache[matrix] = c

    print(f"Part 2 solution: {get_weight(matrix)}")
