import unittest

from environment.grid import make_grid
from environment.maps import MAPS
from algorithms.search import search


def load(name):
    m = MAPS[name]
    return make_grid(m["grid"]), m["start"], m["goal"]


class TestSearch(unittest.TestCase):

    def test_open_grid(self):
        grid, start, goal = load("open")
        for algo in ["ucs", "greedy", "astar"]:
            result = search(grid, start, goal, algo)
            self.assertTrue(result["found"])
            self.assertEqual(result["cost"], 8)

    def test_greedy_worse_path(self):
        grid, start, goal = load("greedy_trap")
        self.assertEqual(search(grid, start, goal, "ucs")["cost"], 6)
        self.assertEqual(search(grid, start, goal, "astar")["cost"], 6)
        self.assertEqual(search(grid, start, goal, "greedy")["cost"], 28)

    def test_no_route(self):
        grid, start, goal = load("no_route")
        result = search(grid, start, goal, "astar")
        self.assertFalse(result["found"])
        self.assertIsNone(result["cost"])


if __name__ == "__main__":
    unittest.main()
