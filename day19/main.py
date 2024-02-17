def sort_part(workflows, part):
    curr_key = "in"
    curr_instructions = workflows[curr_key]
    while True:
        new_instruction = False
        for instruction in curr_instructions[:-1]:
            if eval(instruction[0].replace(instruction[0][0], part[instruction[0][0]])):
                curr_key = instruction[1]
                new_instruction = True
                break
        if not new_instruction:
            curr_key = curr_instructions[-1]
        if curr_key == "A":
            return sum(int(value) for value in part.values())
        if curr_key == "R":
            return 0
        curr_instructions = workflows[curr_key]


def parse_input(inp):
    workflows_inp = inp[0].split("\n")
    parts_inp = inp[1].strip().replace("{", "").replace("}", "").split("\n")

    parts = []
    for part in parts_inp:
        pairs = part.split(",")
        parts.append({pair.split("=")[0]: pair.split("=")[1] for pair in pairs})

    workflows_tmp = {
        workflow[: workflow.find("{")]: workflow[workflow.find("{") + 1 : -1]
        for workflow in workflows_inp
    }

    workflows = {}
    for key, value in workflows_tmp.items():
        workflows[key] = [
            condition.split(":") if ":" in condition else condition
            for condition in value.split(",")
        ]

    return parts, workflows


def num_valid_paths(workflows, valid_ranges, curr_node="in"):
    if curr_node == "R":
        return 0
    if curr_node == "A":
        curr_combinations = 1
        for l, h in valid_ranges.values():
            curr_combinations *= h - l + 1
        return curr_combinations

    curr_instructions = workflows[curr_node][:-1]
    final_instruction = workflows[curr_node][-1]
    fallback = True
    num_paths = 0

    for instruction in curr_instructions:
        op = instruction[0][1]
        l, h = valid_ranges[instruction[0][0]]
        if op == "<":
            if l <= min(int(instruction[0][2:]) - 1, h):
                valid_ranges_copy = dict(valid_ranges)
                valid_ranges_copy[instruction[0][0]] = (
                    l,
                    min(int(instruction[0][2:]) - 1, h),
                )
                num_paths += num_valid_paths(
                    workflows, valid_ranges_copy, instruction[1]
                )
            if max(int(instruction[0][2:]), l) <= h:
                valid_ranges = dict(valid_ranges)
                valid_ranges[instruction[0][0]] = (max(int(instruction[0][2:]), l), h)
            else:
                fallback = False
                break
        else:
            if max(int(instruction[0][2:]) + 1, l) <= h:
                valid_ranges_copy = dict(valid_ranges)
                valid_ranges_copy[instruction[0][0]] = (
                    max(int(instruction[0][2:]) + 1, l),
                    h,
                )
                num_paths += num_valid_paths(
                    workflows, valid_ranges_copy, instruction[1]
                )
            if l <= min(int(instruction[0][2:]), h):
                valid_ranges = dict(valid_ranges)
                valid_ranges[instruction[0][0]] = (l, min(int(instruction[0][2:]), h))
            else:
                fallback = False
                break

    if fallback:
        num_paths += num_valid_paths(workflows, valid_ranges, final_instruction)

    return num_paths


if __name__ == "__main__":
    fpath = r"path_to_file.txt"
    with open(fpath, "r") as file:
        inp = file.read().strip().split("\n\n")

    parts, workflows = parse_input(inp)

    ratings = 0
    for part in parts:
        ratings += sort_part(workflows, part)

    print(f"Part 1 Solution: {ratings}")

    valid_ranges = {key: (1, 4000) for key in "xmas"}
    print(f"Part 2 Solution: {num_valid_paths(workflows, valid_ranges)}")
