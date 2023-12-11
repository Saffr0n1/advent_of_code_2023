import math


def get_root_range(a, b, c):
    sq_root = math.sqrt(b**2 - 4 * a * c)
    r1, r2 = (-1 * b + sq_root) / (2.0 * a), (-1 * b - sq_root) / (2.0 * a)
    r1 = r1 + 1 if r1.is_integer() else r1
    r2 = r2 - 1 if r2.is_integer() else r2

    return math.floor(r2) - math.ceil(r1) + 1


def part1(input):
    times = [int(num) for num in input[0].split()[1:]]
    distances = [int(num) for num in input[1].split()[1:]]
    time_dist = zip(times, distances)
    sol1 = 1
    for item in time_dist:
        sol1 *= get_root_range(-1, item[0], -1 * item[1])
    return sol1


def part2(input):
    time = int("".join(input[0].split()[1:]))
    distance = int("".join(input[1].split()[1:]))
    return get_root_range(-1, time, -1 * distance)


if __name__ == "__main__":
    fpath = r"path_to_file.txt"
    with open(fpath, "r") as file:
        input = [(line[:-1] if "\n" in line else line) for line in file.readlines()]

    # Part 1
    print(f"Part 1 solution: {part1(input)}")

    # Part 2
    print(f"Part 2 solution: {part2(input)}")
