def score_boxes(boxes):
    score = 0
    for pos in range(len(boxes)):
        for key_pos in enumerate(boxes[pos].keys()):
            score += (pos + 1) * (key_pos[0] + 1) * int(boxes[pos][key_pos[1]])

    return score


def seq_parse(inp):
    parsed_seq = []
    for item in inp:
        if "-" in item:
            parsed_seq.append(item.split("-") + ["-"])
        else:
            parsed_seq.append(item.split("=") + ["="])
    return parsed_seq


def hash(inp):
    cv = 0
    for item in inp:
        cv += ord(item)
        cv *= 17
        cv %= 256
    return cv


if __name__ == "__main__":
    fpath = r"path_to_file.txt"
    with open(fpath, "r") as file:
        seq = file.read().strip().split(",")

    # PART 1
    verif = 0
    for inp in seq:
        verif += hash(inp)
    print(f"Part 1 solution: {verif}")

    # PART 2
    boxes = [{} for _ in range(256)]
    parsed_seq = seq_parse(seq)
    for item in parsed_seq:
        box = hash(item[0])
        if item[2] == "-" and item[0] in boxes[box]:
            boxes[box].pop(item[0])
        if item[2] == "=":
            boxes[box][item[0]] = item[1]

    print(f"Part 2 solution: {score_boxes(boxes)}")
