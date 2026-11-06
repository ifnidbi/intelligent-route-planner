# small maps we made by hand for testing and the demo
# positions are (row, col)

MAPS = {
    "open": {
        "grid": [
            ".....",
            ".....",
            ".....",
            ".....",
            ".....",
        ],
        "start": (0, 0),
        "goal": (4, 4),
    },
    "detour": {
        "grid": [
            ".......",
            ".#####.",
            ".....#.",
            ".....#.",
        ],
        "start": (3, 0),
        "goal": (3, 6),
    },
    # going straight is fewer steps but goes through the expensive cells
    "greedy_trap": {
        "grid": [
            ".999.",
            ".....",
        ],
        "start": (0, 0),
        "goal": (0, 4),
    },
    "u_shape": {
        "grid": [
            "..........",
            "..........",
            "..#######.",
            "........#.",
            "........#.",
            "..#######.",
            "..........",
        ],
        "start": (3, 0),
        "goal": (3, 9),
    },
    "no_route": {
        "grid": [
            ".....",
            "...#.",
            "..#.#",
            "...#.",
        ],
        "start": (0, 0),
        "goal": (2, 3),
    },
}
