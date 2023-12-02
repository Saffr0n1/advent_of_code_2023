import time 
from collections import defaultdict

def part1(line):
    l, r = 0, len(line) - 1
    l_done, r_done = False, False
    line_sum = 0
    while l <= r and not (l_done and r_done):
        if line[l].isdigit() and not l_done:
            line_sum += int(line[l])*10
            l_done = True
        elif not l_done:
            l += 1
        if line[r].isdigit() and not r_done:
            line_sum += int(line[r])
            r_done = True
        elif not r_done:
            r -= 1
    return line_sum

def part2(line):
    digits = {
     "one": 1,
     "two": 2,
     "three": 3,
     "four": 4,
     "five": 5,
     "six": 6,
     "seven": 7,
     "eight": 8,
     "nine": 9,
     "1":1, 
     "2":2,
     "3":3,
     "4":4,
     "5":5,
     "6":6,
     "7":7,
     "8":8,
     "9":9
    }
    digit_dict = defaultdict(list)
    for d in digits:
        l = line.find(d)
        while l != -1:
            digit_dict[d].append(l)
            l = line.find(d, l+1)
    return 10*digits[min(digit_dict, key=lambda k: min(digit_dict[k]))] + digits[max(digit_dict, key=lambda k: max(digit_dict[k]))]

if __name__ == "__main__":
    fpath = r"path_to_file.txt"

    # Part 1
    sol1 = 0
    with open(fpath, 'r') as file:
        for line in file:
            sol1 += part1(line)
        
    print(f"Part 1 solution: {sol1}")

    # Part 2
    sol2 = 0
    with open(fpath, 'r') as file:
        for line in file:
            sol2 += part2(line)

    print(f"Part 2 solution: {sol2}")