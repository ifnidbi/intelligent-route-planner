import random

# '.' is a normal cell (cost 1), '#' is a wall, digits 2-9 are slower cells
# like stairs or crowded hallways
WALL = "#"
MIN_COST = 1


def make_grid(lines):
    grid = []
    for line in lines:
        grid.append(list(line))
    return grid


def in_bounds(grid, pos):
    r, c = pos
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def is_open(grid, pos):
    return in_bounds(grid, pos) and grid[pos[0]][pos[1]] != WALL


# cost of moving INTO this cell
def cell_cost(grid, pos):
    ch = grid[pos[0]][pos[1]]
    if ch == ".":
        return 1
    return int(ch)


def get_neighbors(grid, pos):
    r, c = pos
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_pos = (r + dr, c + dc)
        if is_open(grid, new_pos):
            neighbors.append(new_pos)
    return neighbors


def path_cost(grid, path):
    total = 0
    for pos in path[1:]:
        total += cell_cost(grid, pos)
    return total


def random_map(rows, cols, wall_chance, seed, max_cost=1):
    rng = random.Random(seed)
    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            if rng.random() < wall_chance:
                row.append(WALL)
            else:
                cost = rng.randint(1, max_cost)
                if cost == 1:
                    row.append(".")
                else:
                    row.append(str(cost))
        grid.append(row)
    return grid


def random_open_cell(grid, rng):
    open_cells = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] != WALL:
                open_cells.append((r, c))
    if len(open_cells) == 0:
        return None
    return rng.choice(open_cells)
