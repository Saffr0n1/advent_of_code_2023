import re
from functools import cache
from time import time


def brute_force(input_str, groups, current_string="", index=0):
    if index == len(input_str):
        return 1 if validate_arrangement(current_string, groups) else 0

    if input_str[index] == "?":
        return brute_force(
            input_str, groups, current_string + ".", index + 1
        ) + brute_force(input_str, groups, current_string + "#", index + 1)
    else:
        return brute_force(
            input_str, groups, current_string + input_str[index], index + 1
        )


def validate_arrangement(input, groups):
    pattern = re.compile(r"(#+.)")
    matches = [match[1][:-1] for match in pattern.finditer(input)]

    if len(groups) != len(matches):
        return False

    for i in range(len(groups)):
        if groups[i] != len(matches[i]):
            return False

    return True


manual_cache = {}


def manual_cached_count(input, groups):
    if input == "":
        return 1 if not groups else 0
    if not groups:
        return 1 if "#" not in input else 0

    if (input, groups) in manual_cache:
        return manual_cache[(input, groups)]

    count = 0

    if input[0] in ".?":
        count += manual_cached_count(input[1:], groups)

    if input[0] in "#?":
        group_len = groups[0]
        if (
            group_len <= len(input)
            and "." not in input[:group_len]
            and (group_len == len(input) or input[group_len] != "#")
        ):
            count += manual_cached_count(input[group_len + 1 :], groups[1:])

    manual_cache[(input, groups)] = count

    return count


@cache
def cached_count(input, groups):
    if input == "":
        return 1 if not groups else 0
    if not groups:
        return 1 if "#" not in input else 0

    count = 0

    if input[0] in ".?":
        count += cached_count(input[1:], groups)

    if input[0] in "#?":
        group_len = groups[0]
        if (
            group_len <= len(input)
            and "." not in input[:group_len]
            and (group_len == len(input) or input[group_len] != "#")
        ):
            count += cached_count(input[group_len + 1 :], groups[1:])

    return count


if __name__ == "__main__":
    fpath = r"path_to_file.txt"
    with open(fpath, "r") as file:
        input = [
            (line[:-1].split() if "\n" in line else line.split())
            for line in file.readlines()
        ]
    input = [[inp[0] + ".", tuple(int(x) for x in inp[1].split(","))] for inp in input]
    unfolded_input = [[((inp[0][:-1] + "?") * 5)[:-1], inp[1] * 5] for inp in input]

    # PART 1
    s_bf = time()
    part1 = 0
    for line in input:
        part1 += brute_force(line[0], line[1])
    e_bf = time()
    print(f"Part 1 brute force solution: {part1} with time {e_bf - s_bf}")

    # PART 1
    s_c_1 = time()
    part1 = 0
    for line in input:
        part1 += cached_count(line[0], line[1])
    e_c_1 = time()
    print(f"Part 1 cached solution: {part1} with time {e_c_1 - s_c_1}")

    # PART 2
    s_mc = time()
    part2 = 0
    for line in unfolded_input:
        part2 += manual_cached_count(line[0], line[1])
    e_mc = time()

    print(f"Part 2 manual cache solution: {part2} with runtime {e_mc - s_mc}")

    # PART 2
    s_c_2 = time()
    part2 = 0
    for line in unfolded_input:
        part2 += cached_count(line[0], line[1])
    e_c_2 = time()
    print(f"Part 2 cached solution: {part2} with runtime {e_c_2 - s_c_2}")
