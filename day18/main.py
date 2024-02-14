DIR = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}
NUM_DIR = {0: (0, 1), 2: (0, -1), 3: (-1, 0), 1: (1, 0)}


def get_boundary(commands):
    boundary, boundary_len = [(0, 0)], 0
    for command in commands:
        curr_x, curr_y = boundary[-1]
        for _ in range(command[1]):
            curr_x += DIR[command[0]][0]
            curr_y += DIR[command[0]][1]
            boundary_len += 1
        boundary.append((curr_x, curr_y))
    return boundary, boundary_len


def get_hex_boundary(commands):
    boundary, boundary_len = [(0, 0)], 0
    for command in commands:
        curr_x, curr_y = boundary[-1]
        steps, dir_num = int(command[2][1:6], 16), int(command[2][-1])
        curr_x += steps * NUM_DIR[dir_num][0]
        curr_y += steps * NUM_DIR[dir_num][1]
        boundary_len += steps
        boundary.append((curr_x, curr_y))

    return boundary, boundary_len


def shoelace(boundary):
    A = 0
    for i in range(len(boundary)):
        A += (boundary[i][0] * boundary[(i + 1) % len(boundary)][1]) - (
            boundary[(i + 1) % len(boundary)][0] * boundary[i][1]
        )
    return abs(A) // 2


if __name__ == "__main__":
    fpath = r"C:\Users\Abi\Documents\GitHub\advent_of_code_2023\day18\input.txt"
    with open(fpath, "r") as file:
        commands = [
            [parts[0], int(parts[1]), parts[2].strip("()")]
            for line in file
            for parts in [line.strip().split()]
        ]

    boundary, boundary_len = get_boundary(commands)
    inner_area = shoelace(boundary)

    print(f"Part 1 Solution: {inner_area + boundary_len - boundary_len//2 + 1}")

    hex_boundary, hex_boundary_len = get_hex_boundary(commands)
    hex_inner_area = shoelace(hex_boundary)
    print(
        f"Part 2 Solution: {hex_inner_area + hex_boundary_len - hex_boundary_len//2 + 1}"
    )
