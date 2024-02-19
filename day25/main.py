from collections import defaultdict
import statistics
from typing import Dict


def get_crossings(graph, subset):
    complement = set(graph) - subset
    crossings: Dict[str, int] = defaultdict(int)
    for node in subset:
        for neighbor in graph[node]:
            if neighbor in complement:
                crossings[node] += 1

    return crossings


def rand_alg(graph):
    subset = set(graph)
    subset.pop()
    crossings = get_crossings(graph, subset)
    while sum(crossings.values()) != 3:
        try:
            max_crossing_node = max(crossings, key=lambda k: crossings[k])
        except Exception:
            return 0
        subset.remove(max_crossing_node)
        crossings = get_crossings(graph, subset)

    return len(subset) * len(set(graph) - subset)


if __name__ == "__main__":
    graph = defaultdict(set)
    fpath = r"path_to_file.txt"
    for line in open(fpath, "r"):
        k, *v_list = line.replace(":", "").split()
        for v in v_list:
            graph[k].add(v)
            graph[v].add(k)

    NUM_RUNS = 1000
    sols = []
    for _ in range(NUM_RUNS):
        sols.append(rand_alg(graph))

    print(f"Part 1 Solution: {statistics.mode(sols)}")
