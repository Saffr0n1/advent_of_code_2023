import numpy as np
import sympy

MIN_BOUND, MAX_BOUND = 0, 0


def find2DIntersection(l1, l2):
    global MIN_BOUND, MAX_BOUND
    p1, v1, p2, v2 = np.array(l1[0]), np.array(l1[1]), np.array(l2[0]), np.array(l2[1])
    n, d = np.cross(p2 - p1, v2), np.cross(v1, v2)
    if d == 0:
        return False
    m = n / d
    i = p1 + m * v1
    if i[0] < MIN_BOUND or i[0] > MAX_BOUND or i[1] < MIN_BOUND or i[1] > MAX_BOUND:
        return False
    c1, c2 = (i - p1), (i - p2)
    if np.sign(c1[0] * v1[0]) == 1 and np.sign(c2[0] * v2[0]) == 1:
        return True
    return False


def getCoefficients(l1, l2, l3):
    """
    Each coefficient array is of the form [p_x, p_y, p_z, v_x, v_y, v_z, C]
    Each pair of lines yields three linear equations
    For each pair of lines, each equation is of the form
    AX + BY + CZ + DdX + DdY + EdZ = F where (X,Y,Z,dX,dY,dZ) is the line for our rock
    Note that we have 3 pairs of X, Y, Z, resulting in our 3 equations
    """

    l1 = tuple(element for tup in l1 for element in tup)
    l2 = tuple(element for tup in l2 for element in tup)
    l3 = tuple(element for tup in l3 for element in tup)

    coefficients = []
    # l1, l2
    coefficients.append(
        [
            l2[4] - l1[4],
            l1[3] - l2[3],
            0,
            l1[1] - l2[1],
            l2[0] - l1[0],
            0,
            l2[0] * l2[4] - l2[1] * l2[3] - l1[0] * l1[4] + l1[1] * l1[3],
        ]
    )
    coefficients.append(
        [
            l2[5] - l1[5],
            0,
            l1[3] - l2[3],
            l1[2] - l2[2],
            0,
            l2[0] - l1[0],
            l2[0] * l2[5] - l2[2] * l2[3] - l1[0] * l1[5] + l1[2] * l1[3],
        ]
    )
    coefficients.append(
        [
            0,
            l1[5] - l2[5],
            l2[4] - l1[4],
            0,
            l2[2] - l1[2],
            l1[1] - l2[1],
            -l2[1] * l2[5] + l2[2] * l2[4] + l1[1] * l1[5] - l1[2] * l1[4],
        ]
    )

    # l1, l3
    coefficients.append(
        [
            l3[4] - l1[4],
            l1[3] - l3[3],
            0,
            l1[1] - l3[1],
            l3[0] - l1[0],
            0,
            l3[0] * l3[4] - l3[1] * l3[3] - l1[0] * l1[4] + l1[1] * l1[3],
        ]
    )
    coefficients.append(
        [
            l3[5] - l1[5],
            0,
            l1[3] - l3[3],
            l1[2] - l3[2],
            0,
            l3[0] - l1[0],
            l3[0] * l3[5] - l3[2] * l3[3] - l1[0] * l1[5] + l1[2] * l1[3],
        ]
    )
    coefficients.append(
        [
            0,
            l1[5] - l3[5],
            l3[4] - l1[4],
            0,
            l3[2] - l1[2],
            l1[1] - l3[1],
            -l3[1] * l3[5] + l3[2] * l3[4] + l1[1] * l1[5] - l1[2] * l1[4],
        ]
    )

    return coefficients


if __name__ == "__main__":
    fpath = r"path_to_input.txt"
    lines = []
    for line in open(fpath, "r"):
        pos, vel = line.split(" @ ")
        pos, vel = tuple(map(int, pos.strip().split(", "))), tuple(
            map(int, vel.strip().split(", "))
        )
        lines.append([pos, vel])
    lines = tuple(tuple(line) for line in lines)
    lines2D = tuple(((t[0][0], t[0][1]), (t[1][0], t[1][1])) for t in lines)
    MIN_BOUND, MAX_BOUND = 200000000000000, 400000000000000

    intersections = 0
    for i in range(len(lines2D)):
        for j in range(i + 1, len(lines2D)):
            l1, l2 = lines2D[i], lines2D[j]
            if find2DIntersection(l1, l2):
                intersections += 1

    print(f"Part 1 Solution: {intersections}")

    system_of_equations = getCoefficients(lines[0], lines[1], lines[2])
    coefficients_matrix = np.array([row[:-1] for row in system_of_equations])
    constants_vector = np.array([row[-1] for row in system_of_equations])

    solution = np.linalg.solve(coefficients_matrix, constants_vector)
    print(f"Part 2 Solution: {int(np.round(solution[0] + solution[1] + solution[2]))}")
