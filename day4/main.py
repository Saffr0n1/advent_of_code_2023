from collections import defaultdict


def get_matches(input):
    matches = []
    for line in input:
        winners = set(line.split("|")[0].split()[2:])
        yours = set(line.split("|")[1].split())
        matches.append(len(winners & yours))

    return matches


def part1(input):
    matches = get_matches(input)
    return sum([2 ** (match - 1) if match > 0 else 0 for match in matches])


def part2(input):
    cards = defaultdict(int)
    rows = len(input)
    matches = get_matches(input)

    for i in range(rows):
        cards[i] += 1
        for j in range(i + 1, min(rows, i + matches[i] + 1)):
            cards[j] += cards[i]

    return sum(cards.values())


if __name__ == "__main__":
    fpath = r"C:\Users\Abi\Documents\GitHub\advent_of_code_2023\day4\input.txt"
    with open(fpath, "r") as file:
        input = [(line[:-1] if "\n" in line else line) for line in file.readlines()]

    # Part 1
    print(f"Part 1 solution: {part1(input)}")

    # Part 2
    print(f"Part 2 solution: {part2(input)}")
