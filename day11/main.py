def expand_universe(universe, scale_factor):
    expanded_universe = [row for row in universe]
    rows = []
    badCols = set()
    for row in range(len(expanded_universe)):
        emptyRow = True
        for col in range(len(expanded_universe[0])):
            if expanded_universe[row][col] == "#":
                emptyRow = False
                badCols.add(col)
        if emptyRow:
            rows.append(row)

    cols = [col for col in range(len(expanded_universe[0])) if col not in badCols]

    dotRow = "." * (len(expanded_universe[0]) + len(cols) * (scale_factor - 1))
    for col in sorted(cols, reverse=True):
        for row in range(len(expanded_universe)):
            expanded_universe[row] = (
                expanded_universe[row][:col]
                + "." * scale_factor
                + expanded_universe[row][col + 1 :]
            )

    insertRows = [dotRow] * scale_factor

    for row in sorted(rows, reverse=True):
        expanded_universe = (
            expanded_universe[:row] + insertRows + expanded_universe[row + 1 :]
        )

    return expanded_universe, sorted(rows), sorted(cols)


def get_initial_galaxies(universe):
    galaxies = []
    for row in range(len(universe)):
        for col in range(len(universe[0])):
            if universe[row][col] == "#":
                galaxies.append([row, col])
    return galaxies


def get_galaxies(initial_galaxies, rows, cols, scale_factor):
    galaxies = []
    for galaxy in initial_galaxies:
        gal_x, gal_y = galaxy[0], galaxy[1]
        for row in rows:
            if galaxy[0] > row:
                gal_x += scale_factor - 1
        for col in cols:
            if galaxy[1] > col:
                gal_y += scale_factor - 1
        galaxies.append([gal_x, gal_y])

    return galaxies


def all_pairs_galaxy_distances(galaxies):
    totDist = 0
    for gal_1 in range(len(galaxies)):
        for gal_2 in range(gal_1 + 1, len(galaxies)):
            totDist += abs(galaxies[gal_1][0] - galaxies[gal_2][0]) + abs(
                galaxies[gal_1][1] - galaxies[gal_2][1]
            )

    return totDist


if __name__ == "__main__":
    fpath = r"path_to_file.txt"
    with open(fpath, "r") as file:
        input = [(line[:-1] if "\n" in line else line) for line in file.readlines()]

    initial_galaxies = get_initial_galaxies(input)

    # PART 1
    SCALE_FACTOR = 2
    universe, rows, cols = expand_universe(input, SCALE_FACTOR)
    galaxies = get_galaxies(initial_galaxies, rows, cols, SCALE_FACTOR)
    print(f"Part 1 solution: {all_pairs_galaxy_distances(galaxies)}")

    # PART 2
    SCALE_FACTOR = 1_000_000
    universe, rows, cols = expand_universe(input, SCALE_FACTOR)
    galaxies = get_galaxies(initial_galaxies, rows, cols, SCALE_FACTOR)
    print(f"Part 2 solution: {all_pairs_galaxy_distances(galaxies)}")
