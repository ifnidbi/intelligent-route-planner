import random

from environment.grid import make_grid, random_map, random_open_cell
from environment.maps import MAPS
from algorithms.search import search, ALGORITHMS
from visualization.display import print_grid, print_result


def ask(prompt, default):
    text = input(f"{prompt} [{default}]: ").strip()
    if text == "":
        return default
    return text


def ask_position(prompt, default):
    while True:
        text = ask(prompt + " (row col)", f"{default[0]} {default[1]}")
        parts = text.split()
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return (int(parts[0]), int(parts[1]))
        print("type it like: 3 4")


def main():
    print("=== Campus Route Planner ===")
    names = list(MAPS.keys())
    for i in range(len(names)):
        print(f"{i + 1}. {names[i]}")
    print(f"{len(names) + 1}. random map")

    choice = int(ask("Pick a map", 1))
    if 1 <= choice <= len(names):
        m = MAPS[names[choice - 1]]
        grid = make_grid(m["grid"])
        default_start = m["start"]
        default_goal = m["goal"]
    else:
        rows = int(ask("Rows", 20))
        cols = int(ask("Cols", 20))
        walls = float(ask("Wall chance (0 to 1)", 0.2))
        max_cost = int(ask("Max cell cost (1 to 9)", 5))
        seed = int(ask("Seed", random.randint(0, 9999)))
        grid = random_map(rows, cols, walls, seed, max_cost)
        rng = random.Random(seed)
        default_start = random_open_cell(grid, rng)
        default_goal = random_open_cell(grid, rng)
        if default_start is None:
            print("map is all walls, try again")
            return

    print()
    print_grid(grid)
    print()

    start = ask_position("Start", default_start)
    goal = ask_position("Goal", default_goal)
    algo = ask("Algorithm (ucs, greedy, astar, all)", "all").lower()

    if algo == "all":
        algos = ALGORITHMS
    else:
        algos = [algo]

    results = {}
    for a in algos:
        try:
            result = search(grid, start, goal, a)
        except ValueError as e:
            print("Error:", e)
            return
        results[a] = result
        print()
        print_grid(grid, result["path"], start, goal)
        print_result(a, result)

    if len(algos) > 1:
        print()
        print(f"{'algo':<8}{'found':<8}{'cost':<8}{'expanded':<10}{'time (ms)':<10}")
        for a in algos:
            r = results[a]
            print(f"{a:<8}{str(r['found']):<8}{str(r['cost']):<8}{r['expanded']:<10}{r['time'] * 1000:<10.3f}")


if __name__ == "__main__":
    main()
