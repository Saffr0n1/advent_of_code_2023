from time import time


def parse_input(fpath):
    with open(fpath, "r") as file:
        input = [(line[:-1] if "\n" in line else line) for line in file.readlines()]

    inputs = {}
    seeds = [int(num) for num in input[0].split()[1:]]
    dividers = []
    for l in range(1, len(input)):
        if any(char.isalpha() and "a" <= char <= "z" for char in input[l]):
            dividers.append(l)

    inputs["seed-to-soil"] = [
        [int(num) for num in string.split()]
        for string in input[dividers[0] + 1 : dividers[1] - 1]
    ]
    inputs["soil-to-fertilizer"] = [
        [int(num) for num in string.split()]
        for string in input[dividers[1] + 1 : dividers[2] - 1]
    ]
    inputs["fertilizer-to-water"] = [
        [int(num) for num in string.split()]
        for string in input[dividers[2] + 1 : dividers[3] - 1]
    ]
    inputs["water-to-light"] = [
        [int(num) for num in string.split()]
        for string in input[dividers[3] + 1 : dividers[4] - 1]
    ]
    inputs["light-to-temperature"] = [
        [int(num) for num in string.split()]
        for string in input[dividers[4] + 1 : dividers[5] - 1]
    ]
    inputs["temperature-to-humidity"] = [
        [int(num) for num in string.split()]
        for string in input[dividers[5] + 1 : dividers[6] - 1]
    ]
    inputs["humidity-to-location"] = [
        [int(num) for num in string.split()] for string in input[dividers[6] + 1 :]
    ]

    for key in inputs.keys():
        inputs[key] = sorted(inputs[key], key=lambda x: x[1])

    return seeds, inputs


def get_next(input, mapping):
    if input < mapping[0][1] or input > mapping[-1][1]:
        return input
    else:
        for item in mapping:
            if input < item[1] + item[2]:
                return item[0] + input - item[1]
        return input


def get_prev(input, mapping):
    if input < mapping[0][0] or input > mapping[-1][0]:
        return input
    else:
        for item in mapping:
            if input < item[0] + item[2]:
                return item[1] + input - item[0]
        return input


def in_seed_range(input, seed_range):
    for item in seed_range:
        if input >= item[0] and input <= item[1]:
            return True
    return False


def linear_search(l, r, graph, seed_range):
    for loc in range(l, r):
        input = loc
        for mapping in list(graph.values())[::-1]:
            input = get_prev(input, mapping)

        if in_seed_range(input, seed_range):
            return [loc, "final"]
    return [0, "final"]


def gapped_search(location, graph, seed_range, gap):
    input = location
    for mapping in list(graph.values())[::-1]:
        input = get_prev(input, mapping)
    if not in_seed_range(input, seed_range):
        location = max(1, location + gap)
        return [location, "loc"]
    else:
        return linear_search(location - gap, location, graph, seed_range)


def part1(seeds, graph):
    min_location = (
        graph["humidity-to-location"][-1][0] + graph["humidity-to-location"][-1][2] - 1
    )
    for seed in seeds:
        input = seed
        for mapping in graph.values():
            input = get_next(input, mapping)
        if input < min_location:
            min_location = input

    return min_location


def part2(seeds, graph, part_1_ans):
    seed_range = sorted(
        [[x, x + y - 1] for x, y in zip(seeds[::2], seeds[1::2])], key=lambda x: x[0]
    )

    rev_graph = {}
    for key in graph.keys():
        rev_graph[key] = sorted(graph[key], key=lambda x: x[0])

    loc, max_loc = 0, part_1_ans - 1
    while loc < max_loc:
        gap_out = gapped_search(loc, rev_graph, seed_range, gap=40_000)
        if gap_out[1] == "loc":
            loc = gap_out[0]
        else:
            return gap_out[0]


if __name__ == "__main__":
    # Parse inputs
    fpath = r"path_to_file.txt"
    seeds, graph = parse_input(fpath)

    # Part 1
    part_1_ans = part1(seeds, graph)
    print(f"Part 1 solution: {part_1_ans}")

    # Part 2
    start = time()
    print(f"Part 2 solution: {part2(seeds, graph, part_1_ans)}")
    end = time()
    print(f"Part 2 time: {end - start}")
