def one_diff(s1, s2):
    num_diffs = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            num_diffs += 1
        if num_diffs > 1:
            return False
    return True


def validate_reflection(mat, l, r, smudge=False):
    num_diffs = 0
    while l >= 0 and r < len(mat):
        if mat[l] != mat[r]:
            if smudge:
                if num_diffs > 1 or not one_diff(mat[l], mat[r]):
                    return False
                else:
                    num_diffs += 1
            else:
                return False
        l -= 1
        r += 1
    return num_diffs == 1 if smudge else True


def reflection_score(mat_rows, mat_cols, smudge=False):
    score = 0
    for i in range(len(mat_rows) - 1):
        score += 100 * (i + 1) if validate_reflection(mat_rows, i, i + 1, smudge) else 0

    for i in range(len(mat_cols) - 1):
        score += i + 1 if validate_reflection(mat_cols, i, i + 1, smudge) else 0

    return score


if __name__ == "__main__":
    fpath = r"path_to_file.txt"
    with open(fpath, "r") as file:
        input_matrices = file.read().strip().split("\n\n")

    mat_rows = [mat.strip().split("\n") for mat in input_matrices]
    mat_cols = [["".join(col) for col in zip(*row)] for row in mat_rows]

    mat_zip = list(zip(mat_rows, mat_cols))

    # PART 1
    part1 = 0
    for mat_row, mat_col in mat_zip:
        part1 += reflection_score(mat_row, mat_col)

    print(f"Part 1 solution: {part1}")

    # PART 2
    part2 = 0
    for mat_row, mat_col in mat_zip:
        part2 += reflection_score(mat_row, mat_col, smudge=True)

    print(f"Part 2 solution: {part2}")
