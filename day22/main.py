from collections import defaultdict, deque


def check_overlap(b1, b2):
    return max(b1[0], b2[0]) <= min(b1[3], b2[3]) and max(b1[1], b2[1]) <= min(
        b1[4], b2[4]
    )


def settle_bricks(bricks):
    for index, brick in enumerate(bricks):
        curr_z_base = 1
        for lower_brick in bricks[:index]:
            if check_overlap(brick, lower_brick):
                curr_z_base = max(curr_z_base, lower_brick[5] + 1)
        brick[2], brick[5] = curr_z_base, curr_z_base + brick[5] - brick[2]
    return sorted(bricks, key=lambda x: x[2])


def get_supports(bricks):
    supports, supported = {i: set() for i in range(len(bricks))}, {
        i: set() for i in range(len(bricks))
    }
    for index, brick in enumerate(bricks):
        for lower_index, lower_brick in enumerate(bricks[:index]):
            if check_overlap(brick, lower_brick) and brick[2] == lower_brick[5] + 1:
                supports[lower_index].add(index)
                supported[index].add(lower_index)
    return supports, supported


def get_redundant(bricks, supports, supported):
    redundant = set()
    for index in range(len(bricks)):
        for base in supports[index]:
            if len(supported[base]) < 2:
                break
        else:
            redundant.add(index)
    return redundant


def cascade_destruction(non_redundant, supports, supported):
    tot_falls = 0
    for nr in non_redundant:
        falls = set([nr])
        queue = deque([nr])
        while queue:
            curr_block = queue.popleft()
            for supported_block in supports[curr_block]:
                if set(supported[supported_block]) - falls == set():
                    falls.add(supported_block)
                    queue.append(supported_block)
        tot_falls += len(falls) - 1
    return tot_falls


if __name__ == "__main__":
    fpath = r"path_to_file.txt"
    with open(fpath, "r") as file:
        bricks = sorted(
            [
                list(map(int, line.strip().replace("~", ",").split(",")))
                for line in file
            ],
            key=lambda x: x[2],
        )

    bricks = settle_bricks(bricks)
    supports, supported = get_supports(bricks)
    redundant = get_redundant(bricks, supports, supported)
    print(f"Part 1 Solution: {len(redundant)}")

    non_redundant = set(range(len(bricks))) - redundant
    print(cascade_destruction(non_redundant, supports, supported))
