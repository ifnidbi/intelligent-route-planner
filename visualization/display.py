def print_grid(grid, path=None, start=None, goal=None):
    on_path = set()
    if path:
        on_path = set(path)

    header = "    "
    for c in range(len(grid[0])):
        header += str(c % 10)
    print(header)

    for r in range(len(grid)):
        line = ""
        for c in range(len(grid[0])):
            if (r, c) == start:
                line += "S"
            elif (r, c) == goal:
                line += "G"
            elif (r, c) in on_path:
                line += "*"
            else:
                line += grid[r][c]
        print(f"{r:3} {line}")


def print_result(algo, result):
    print("Algorithm:", algo)
    if result["found"]:
        print("Route found: yes")
        print("Path:", " -> ".join(str(p) for p in result["path"]))
        print("Total cost:", result["cost"])
    else:
        print("Route found: no (goal cant be reached)")
    print("Nodes expanded:", result["expanded"])
    print(f"Time: {result['time'] * 1000:.3f} ms")
