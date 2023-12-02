import re


p_subsets = re.compile(r";")
patterns = {
    "red": re.compile(r"\d* red"),
    "green": re.compile(r"\d* green"),
    "blue": re.compile(r"\d* blue"),
}


def get_subsets(line):
    separators = [0] + [x.start() for x in p_subsets.finditer(line)] + [len(line)]
    subsets = [line[start:end] for start, end in zip(separators, separators[1:])]

    return subsets


def part1(line):
    bag = {"red": 12, "green": 13, "blue": 14}

    subsets = get_subsets(line)

    for subset in subsets:
        for color, color_max in bag.items():
            if (
                sum(
                    [
                        int(subset[x.start() : x.end() - len(color)])
                        for x in patterns[color].finditer(subset)
                    ]
                )
                > color_max
            ):
                return False

    return True


def part2(line):
    color_max = {"red": 0, "green": 0, "blue": 0}

    subsets = get_subsets(line)

    for subset in subsets:
        for color in color_max:
            s = sum(
                [
                    int(subset[x.start() : x.end() - len(color)])
                    for x in patterns[color].finditer(subset)
                ]
            )
            if s > color_max[color]:
                color_max[color] = s

    return color_max["red"] * color_max["green"] * color_max["blue"]


if __name__ == "__main__":
    fpath = r"path_to_file.txt"

    # Part 1
    sol1, c = 0, 1
    with open(fpath, "r") as file:
        for line in file:
            if part1(line):
                sol1 += c
            c += 1

    print(f"Part 1 solution: {sol1}")

    # Part 2
    sol2 = 0
    with open(fpath, "r") as file:
        for line in file:
            sol2 += part2(line)

    print(f"Part 2 solution : {sol2}")
