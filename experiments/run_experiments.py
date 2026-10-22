import csv
import random
import sys

from environment.grid import random_map, random_open_cell
from algorithms.search import search, ALGORITHMS, manhattan

SIZES = [20, 50, 100]
WALL_CHANCES = [0.0, 0.2, 0.4]
MAX_COSTS = [1, 5]

OUTPUT_FILE = "experiments/results.csv"


def run_all(runs):
    rows = []
    for size in SIZES:
        for walls in WALL_CHANCES:
            for max_cost in MAX_COSTS:
                for seed in range(runs):
                    # same map + start + goal for every algorithm
                    grid = random_map(size, size, walls, seed, max_cost)
                    rng = random.Random(seed)
                    start = random_open_cell(grid, rng)
                    goal = random_open_cell(grid, rng)

                    for algo in ALGORITHMS:
                        result = search(grid, start, goal, algo)
                        rows.append({
                            "size": size,
                            "walls": walls,
                            "max_cost": max_cost,
                            "seed": seed,
                            "start": start,
                            "goal": goal,
                            "distance": manhattan(start, goal),
                            "algo": algo,
                            "found": result["found"],
                            "cost": result["cost"],
                            "expanded": result["expanded"],
                            "time_ms": round(result["time"] * 1000, 4),
                        })
    return rows


def save_csv(rows):
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def print_summary(rows):
    # ucs cost for each map so we can see how much worse greedy is
    best_cost = {}
    for row in rows:
        if row["algo"] == "ucs" and row["found"]:
            best_cost[(row["size"], row["walls"], row["max_cost"], row["seed"])] = row["cost"]

    print(f"{'size':<6}{'walls':<7}{'cost':<6}{'algo':<8}{'found':<8}{'avg cost':<10}{'vs ucs':<9}{'avg expanded':<14}{'avg ms':<8}")
    for size in SIZES:
        for walls in WALL_CHANCES:
            for max_cost in MAX_COSTS:
                for algo in ALGORITHMS:
                    group = []
                    for row in rows:
                        if row["size"] == size and row["walls"] == walls and row["max_cost"] == max_cost and row["algo"] == algo:
                            group.append(row)

                    found = [r for r in group if r["found"]]
                    avg_expanded = sum(r["expanded"] for r in group) / len(group)
                    avg_time = sum(r["time_ms"] for r in group) / len(group)

                    # only average cost over runs where a route exists (not counting them as 0)
                    if len(found) > 0:
                        avg_cost = sum(r["cost"] for r in found) / len(found)
                        ratios = []
                        for r in found:
                            best = best_cost[(size, walls, max_cost, r["seed"])]
                            if best > 0:
                                ratios.append(r["cost"] / best)
                        if len(ratios) > 0:
                            vs_ucs = f"{sum(ratios) / len(ratios):.2f}x"
                        else:
                            vs_ucs = "-"
                        avg_cost = f"{avg_cost:.1f}"
                    else:
                        avg_cost = "-"
                        vs_ucs = "-"

                    found_str = f"{len(found)}/{len(group)}"
                    print(f"{size:<6}{walls:<7}{max_cost:<6}{algo:<8}{found_str:<8}{avg_cost:<10}{vs_ucs:<9}{avg_expanded:<14.1f}{avg_time:<8.3f}")
                print()


if __name__ == "__main__":
    runs = 10
    if len(sys.argv) > 1:
        runs = int(sys.argv[1])
    print(f"running {runs} maps per condition...")
    rows = run_all(runs)
    save_csv(rows)
    print_summary(rows)
    print("saved results to", OUTPUT_FILE)
