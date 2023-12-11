def consecutive_difference(num_list):
    diff_list = list(zip(num_list, num_list[1:]))
    return [nums[1] - nums[0] for nums in diff_list]


def reduce(num_list):
    ends = []
    ends.append(num_list[-1])
    while set(num_list) != {0}:
        num_list = consecutive_difference(num_list)
        ends.append(num_list[-1])
    return sum(ends)


def reduced_sum(input):
    out_sum = 0
    for num_list in input:
        out_sum += reduce(num_list)
    return out_sum


if __name__ == "__main__":
    fpath = r"path_to_file.txt"
    with open(fpath, "r") as file:
        input = [
            (line[:-1].split() if "\n" in line else line.split())
            for line in file.readlines()
        ]
    input = [[int(num) for num in sublist] for sublist in input]

    # Part 1
    print(f"Part 1 solution: {reduced_sum(input)}")

    # Part 2
    rev_input = [num_list[::-1] for num_list in input]
    print(f"Part 2 solution: {reduced_sum(rev_input)}")
