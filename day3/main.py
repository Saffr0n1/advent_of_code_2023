import re
from dataclasses import dataclass


non_symbols = re.compile(r"[^.\d]+")
digits = re.compile(r"\d+")


@dataclass
class Number:
    num: str
    start_pos: int
    row: int
    checked: bool = False


@dataclass
class Symbol:
    sym: str
    pos: int
    row: int


def parse_input(fpath):
    nums = []
    symbols = []

    with open(fpath, "r") as file:
        input = [(line[:-1] if "\n" in line else line) for line in file.readlines()]

    for r in range(len(input)):
        digit_matches = [
            (match.group(), match.start()) for match in digits.finditer(input[r])
        ]
        symbol_matches = [
            (match.group(), match.start()) for match in non_symbols.finditer(input[r])
        ]
        for num, start_pos in digit_matches:
            nums.append(Number(num, start_pos, r))
        for sym, start_pos in symbol_matches:
            symbols.append(Symbol(sym, start_pos, r))

    return nums, symbols


def part1(nums, symbols):
    part_num_sum = 0
    for num in nums:
        if not num.checked:
            for sym in symbols:
                if sym.row in [num.row - 1, num.row, num.row + 1] and (
                    sym.pos >= num.start_pos - 1
                    and sym.pos <= num.start_pos + len(num.num)
                ):
                    part_num_sum += int(num.num)
                    num.checked = True
                    break
    return part_num_sum


def part2(nums, symbols):
    star_symbols = [symbol for symbol in symbols if symbol.sym == "*"]

    gear_ratio = 0
    for star in star_symbols:
        seen, curr_ratio = 0, 1
        star_cols = {star.pos - 1, star.pos, star.pos + 1}
        for num in nums:
            num_cols = set(
                [r for r in range(num.start_pos, num.start_pos + len(num.num))]
            )
            if num.row in [star.row - 1, star.row, star.row + 1] and (
                star_cols.intersection(num_cols)
            ):
                seen += 1
                curr_ratio *= int(num.num)
        if seen == 2:
            gear_ratio += curr_ratio
        seen, curr_ratio = 0, 1

    return gear_ratio


if __name__ == "__main__":
    fpath = r"C:\Users\Abi\Documents\GitHub\advent_of_code_2023\day3\input.txt"
    nums, symbols = parse_input(fpath)

    # Part 1
    print(f"Part 1 solution: {part1(nums, symbols)}")

    # Part 2
    print(f"Part 2 solution: {part2(nums, symbols)}")
