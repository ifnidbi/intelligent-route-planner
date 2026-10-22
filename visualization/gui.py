import random
import tkinter as tk

from environment.grid import make_grid, random_map, random_open_cell, WALL
from environment.maps import MAPS
from algorithms.search import search, ALGORITHMS

BG = "#c0c0c0"
CANVAS_SIZE = 600

EXPANDED_COLOR = "#99ccff"
PATH_COLOR = "#ff00ff"
START_COLOR = "#00cc00"
GOAL_COLOR = "red"


def cell_color(ch):
    if ch == WALL:
        return "black"
    if ch == ".":
        return "white"
    # more expensive = more orange
    cost = int(ch)
    return f"#ff{255 - cost * 15:02x}{255 - cost * 25:02x}"


class App:
    def __init__(self, root):
        self.root = root
        root.title("Campus Route Planner")
        root.configure(bg=BG)

        self.maps = []
        self.current = 0
        self.rects = {}
        self.anim_job = None

        left = tk.Frame(root, bg=BG, relief="groove", bd=2, padx=8, pady=8)
        left.pack(side="left", fill="y", padx=6, pady=6)

        tk.Label(left, text="SETTINGS", bg=BG, font=("Courier", 12, "bold")).pack(anchor="w")
        self.map_var = self.dropdown(left, "Map", ["random"] + list(MAPS.keys()))
        self.size_var = self.dropdown(left, "Grid size", ["5", "10", "25", "50", "100"], "10")
        self.walls_var = self.dropdown(left, "Walls", ["0%", "10%", "20%", "30%", "40%"], "20%")
        self.cost_var = self.dropdown(left, "Max cell cost", ["1", "3", "5", "9"], "5")
        self.ends_var = self.dropdown(left, "Start/Goal", ["random", "corners"])
        self.count_var = self.dropdown(left, "Number of maps", ["1", "5", "10", "20"], "10")
        self.seed_var = self.dropdown(left, "First seed", ["0", "100", "200", "300", "400", "500"])
        self.speed_var = self.dropdown(left, "Speed", ["instant", "fast", "slow"], "fast")

        tk.Button(left, text="Run", width=12, command=self.run).pack(pady=8)

        tk.Label(left, text="VIEW", bg=BG, font=("Courier", 12, "bold")).pack(anchor="w", pady=(10, 0))
        self.view_var = tk.StringVar(value="")
        row = tk.Frame(left, bg=BG)
        row.pack(anchor="w")
        tk.Button(row, text="<", command=self.prev_map).pack(side="left")
        self.map_menu = tk.OptionMenu(row, self.view_var, "")
        self.map_menu.config(width=12)
        self.map_menu.pack(side="left")
        tk.Button(row, text=">", command=self.next_map).pack(side="left")

        self.algo_var = self.dropdown(left, "Show algorithm", ALGORITHMS, "astar", self.draw)
        tk.Button(left, text="Replay", width=12, command=self.draw).pack(pady=8)

        self.info = tk.Label(left, text="press Run", bg=BG, font=("Courier", 11), justify="left")
        self.info.pack(anchor="w", pady=6)

        tk.Label(left, bg=BG, justify="left", font=("Courier", 10),
                 text="green = start\nred = goal\nblack = wall\norange = costs more\n"
                      "blue = expanded\npink = route\n\nleft click = move start\nright click = move goal").pack(anchor="w")

        self.canvas = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="white",
                                relief="sunken", bd=2, highlightthickness=0)
        self.canvas.pack(side="left", padx=6, pady=6)
        self.canvas.bind("<Button-1>", self.set_start)
        self.canvas.bind("<Button-2>", self.set_goal)
        self.canvas.bind("<Button-3>", self.set_goal)

    def dropdown(self, parent, label, options, default=None, command=None):
        tk.Label(parent, text=label, bg=BG).pack(anchor="w")
        var = tk.StringVar(value=default or options[0])
        if command:
            menu = tk.OptionMenu(parent, var, *options, command=lambda x: command())
        else:
            menu = tk.OptionMenu(parent, var, *options)
        menu.config(width=12)
        menu.pack(anchor="w")
        return var

    def run(self):
        self.maps = []
        name = self.map_var.get()

        if name != "random":
            m = MAPS[name]
            self.maps.append({"name": name, "grid": make_grid(m["grid"]), "start": m["start"], "goal": m["goal"]})
        else:
            size = int(self.size_var.get())
            walls = int(self.walls_var.get().strip("%")) / 100
            max_cost = int(self.cost_var.get())
            first_seed = int(self.seed_var.get())
            for i in range(int(self.count_var.get())):
                seed = first_seed + i
                grid = random_map(size, size, walls, seed, max_cost)
                if self.ends_var.get() == "random":
                    rng = random.Random(seed)
                    start = random_open_cell(grid, rng)
                    goal = random_open_cell(grid, rng)
                    if start is None:
                        continue
                else:
                    start = (0, 0)
                    goal = (size - 1, size - 1)
                    # make sure the corners arent walls
                    grid[0][0] = "."
                    grid[size - 1][size - 1] = "."
                self.maps.append({"name": f"seed {seed}", "grid": grid, "start": start, "goal": goal})

        for m in self.maps:
            self.solve(m)

        menu = self.map_menu["menu"]
        menu.delete(0, "end")
        for i in range(len(self.maps)):
            menu.add_command(label=self.maps[i]["name"], command=lambda i=i: self.show_map(i))
        self.show_map(0)

    def solve(self, m):
        m["results"] = {}
        for algo in ALGORITHMS:
            m["results"][algo] = search(m["grid"], m["start"], m["goal"], algo)

    def show_map(self, i):
        if len(self.maps) == 0:
            return
        self.current = i % len(self.maps)
        self.view_var.set(self.maps[self.current]["name"])
        self.draw()

    def prev_map(self):
        self.show_map(self.current - 1)

    def next_map(self):
        self.show_map(self.current + 1)

    def update_info(self):
        m = self.maps[self.current]
        text = f"{m['name']}\nstart {m['start']}\ngoal  {m['goal']}\n\n"
        text += "algo   found cost  expanded\n"
        for algo in ALGORITHMS:
            r = m["results"][algo]
            found = "yes" if r["found"] else "no"
            cost = r["cost"] if r["found"] else "-"
            text += f"{algo:<7}{found:<6}{str(cost):<6}{r['expanded']}\n"
        text += "\ntime (ms)\n"
        for algo in ALGORITHMS:
            text += f"{algo:<7}{m['results'][algo]['time'] * 1000:.3f}\n"
        self.info.config(text=text)

    def draw(self):
        if len(self.maps) == 0:
            return
        if self.anim_job:
            self.root.after_cancel(self.anim_job)
            self.anim_job = None

        m = self.maps[self.current]
        grid = m["grid"]
        rows = len(grid)
        cols = len(grid[0])
        size = CANVAS_SIZE // max(rows, cols)

        self.canvas.delete("all")
        self.rects = {}
        self.cell_size = size
        for r in range(rows):
            for c in range(cols):
                x = c * size + 2
                y = r * size + 2
                outline = "gray" if size > 6 else ""
                self.rects[(r, c)] = self.canvas.create_rectangle(x, y, x + size, y + size,
                                                                  fill=cell_color(grid[r][c]), outline=outline)
                if size >= 20 and grid[r][c] not in (".", WALL):
                    self.canvas.create_text(x + size / 2, y + size / 2, text=grid[r][c])

        self.color(m["start"], START_COLOR)
        self.color(m["goal"], GOAL_COLOR)
        self.update_info()

        result = m["results"][self.algo_var.get()]
        self.to_color = list(result["order"])
        if result["path"]:
            self.path = list(result["path"])
        else:
            self.path = []

        # how many cells to color each tick
        total = len(self.to_color) + len(self.path)
        speed = self.speed_var.get()
        if speed == "instant":
            self.step = total
            self.delay = 1
        elif speed == "fast":
            self.step = max(1, total // 100)
            self.delay = 10
        else:
            self.step = max(1, total // 300)
            self.delay = 60
        self.animate()

    def color(self, pos, fill):
        self.canvas.itemconfig(self.rects[pos], fill=fill)

    def animate(self):
        m = self.maps[self.current]
        for i in range(self.step):
            if self.to_color:
                pos = self.to_color.pop(0)
                fill = EXPANDED_COLOR
            elif self.path:
                pos = self.path.pop(0)
                fill = PATH_COLOR
            else:
                break
            if pos != m["start"] and pos != m["goal"]:
                self.color(pos, fill)

        if self.to_color or self.path:
            self.anim_job = self.root.after(self.delay, self.animate)
        else:
            self.anim_job = None

    def click_to_cell(self, event):
        if len(self.maps) == 0:
            return None
        r = (event.y - 2) // self.cell_size
        c = (event.x - 2) // self.cell_size
        grid = self.maps[self.current]["grid"]
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] != WALL:
            return (r, c)
        return None

    def set_start(self, event):
        pos = self.click_to_cell(event)
        if pos:
            self.maps[self.current]["start"] = pos
            self.solve(self.maps[self.current])
            self.draw()

    def set_goal(self, event):
        pos = self.click_to_cell(event)
        if pos:
            self.maps[self.current]["goal"] = pos
            self.solve(self.maps[self.current])
            self.draw()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
