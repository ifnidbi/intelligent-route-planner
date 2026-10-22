import heapq
import time

from environment.grid import is_open, get_neighbors, cell_cost, MIN_COST

ALGORITHMS = ["ucs", "greedy", "astar"]


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# every move costs at least MIN_COST and we can only move up/down/left/right,
# so this can never be more than the real cost
def heuristic(pos, goal):
    return manhattan(pos, goal) * MIN_COST


def get_priority(algo, g, pos, goal):
    if algo == "ucs":
        return g
    elif algo == "greedy":
        return heuristic(pos, goal)
    else:
        return g + heuristic(pos, goal)


def make_path(parent, goal):
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path


def search(grid, start, goal, algo):
    if algo not in ALGORITHMS:
        raise ValueError("unknown algorithm: " + str(algo))
    if not is_open(grid, start):
        raise ValueError("start " + str(start) + " is a wall or off the map")
    if not is_open(grid, goal):
        raise ValueError("goal " + str(goal) + " is a wall or off the map")

    start_time = time.perf_counter()

    frontier = []
    heapq.heappush(frontier, (get_priority(algo, 0, start, goal), start))
    g = {start: 0}
    parent = {start: None}
    expanded_set = set()
    # expanded = nodes we take off the queue and look at (old duplicate entries dont count)
    expanded = 0
    order = []  # for the gui animation
    path = None

    while frontier:
        priority, node = heapq.heappop(frontier)
        if node in expanded_set:
            continue
        expanded_set.add(node)
        expanded += 1
        order.append(node)

        if node == goal:
            path = make_path(parent, goal)
            break

        for nb in get_neighbors(grid, node):
            if nb in expanded_set:
                continue
            new_g = g[node] + cell_cost(grid, nb)
            if algo == "greedy":
                # greedy doesnt care about cost so just keep the first way we found it
                if nb in g:
                    continue
            elif nb in g and new_g >= g[nb]:
                continue
            g[nb] = new_g
            parent[nb] = node
            heapq.heappush(frontier, (get_priority(algo, new_g, nb, goal), nb))

    run_time = time.perf_counter() - start_time

    result = {
        "found": path is not None,
        "path": path,
        "cost": None,
        "expanded": expanded,
        "time": run_time,
        "order": order,
    }
    if path is not None:
        result["cost"] = g[goal]
    return result
