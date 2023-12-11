from collections import defaultdict, Counter
from functools import cmp_to_key


def break_ties(x, y, part):
    card_strength = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }

    if part == 2:
        card_strength["J"] = 0

    for i in range(len(x)):
        if card_strength[x[i]] > card_strength[y[i]]:
            return -1
        elif card_strength[y[i]] > card_strength[x[i]]:
            return 1
    return 0


def rank_hand(hand):
    char_count = Counter(hand)

    if 5 in char_count.values():
        return 7
    elif 4 in char_count.values():
        return 6
    elif set(char_count.values()) == {3, 2} or set(char_count.values()) == {2, 3}:
        return 5
    elif 3 in char_count.values():
        return 4
    elif list(char_count.values()).count(2) == 2:
        return 3
    elif 2 in char_count.values():
        return 2
    elif max(char_count.values()) == 1:
        return 1


def wildcard_hand(hand):
    if "J" not in hand:
        return hand

    counter = Counter(hand).most_common(2)
    if counter[0][0] == "J":
        if counter[0][1] == 5:
            most_common = "A"
        else:
            most_common = counter[1][0]
    else:
        most_common = counter[0][0]

    hand = hand.replace("J", most_common)
    return hand


def score_hands(hand_score, part):
    ranked_hands = defaultdict(list)

    for hand in hand_score:
        if part == 2:
            ranked_hands[rank_hand(wildcard_hand(hand[0]))].append(hand)
        else:
            ranked_hands[rank_hand(hand[0])].append(hand)

    for key in ranked_hands.keys():
        ranked_hands[key] = sorted(
            ranked_hands[key], key=cmp_to_key(lambda x, y: break_ties(x[0], y[0], part)) # type: ignore
        )

    max_score = len(hand_score)
    tot_score = 0
    for key in sorted(ranked_hands.keys(), reverse=True):
        for value in ranked_hands[key]:
            tot_score += max_score * value[1]
            max_score -= 1

    return tot_score


if __name__ == "__main__":
    fpath = r"C:\Users\Abi\Documents\GitHub\advent_of_code_2023\day7\input.txt"
    with open(fpath, "r") as file:
        input = [(line[:-1] if "\n" in line else line) for line in file.readlines()]
    hand_score = [[num.split()[0], int(num.split()[1])] for num in input]

    # Part 1
    print(f"Part 1 solution: {score_hands(hand_score, 1)}")

    # Part 2
    print(f"Part 2 solution: {score_hands(hand_score, 2)}")
