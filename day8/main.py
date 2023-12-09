import math


def parse_input(fpath):
    with open(fpath, "r") as file:
        input = [(line[:-1] if "\n" in line else line) for line in file.readlines()]

    path = input[0].replace("L", "0").replace("R", "1")
    graph = {}
    for item in input[2:]:
        chunks = item.split()
        graph[chunks[0]] = [chunks[2][1:-1], chunks[3][:-1]]

    return path, graph


def part1(path, graph):
    counter = 0
    curr_node = "AAA"
    while curr_node != "ZZZ":
        curr_pos = counter % len(path)
        curr_node = graph[curr_node][int(path[curr_pos])]
        counter += 1

    return counter


def part2(path, graph):
    curr_nodes = [item for item in graph.keys() if item[-1] == "A"]
    path_lengths = []

    for curr_node in curr_nodes:
        counter = 0
        while curr_node[-1] != "Z":
            curr_pos = counter % len(path)
            curr_node = graph[curr_node][int(path[curr_pos])]
            counter += 1
        path_lengths.append(counter)

    return math.lcm(*path_lengths)


if __name__ == "__main__":
    fpath = r"C:\Users\Abi\Documents\GitHub\advent_of_code_2023\day8\input.txt"
    path, graph = parse_input(fpath)

    # Part 1
    print(f"Part 1 solution: {part1(path, graph)}")

    # Part 2
    print(f"Part 1 solution: {part2(path, graph)}")
