# Intelligent Route Planner

SOFE 3720 — Introduction to Artificial Intelligence  
Group 4 Course Project

## Overview

We are developing a route-planning agent for a simulated campus environment. The project will compare how different search algorithms find routes and balance route cost against computational effort.

**Status:** UCS, Greedy and A* working with a simple window and a text interface, some basic tests and a first experiment runner.

## Planned Algorithms

- **Uniform Cost Search (UCS):** Prioritises accumulated path cost.
- **Greedy Best-First Search:** Prioritises estimated remaining cost.
- **A* Search:** Prioritises accumulated cost plus estimated remaining cost.

We will implement the core search algorithms ourselves. Supporting libraries may assist with graph representation, visualisation, and data analysis.

## Proposed Environment

- A weighted campus grid with walkable cells and obstacles.
- Movement up, down, left, and right.
- Positive movement costs, with optional nonnegative terrain or crowding penalties.
- User-selected or generated maps, start locations, and goals.

Our proposed heuristic is Manhattan distance multiplied by the minimum movement cost. These design choices will be confirmed during implementation.

## Planned Output

The system will display the route, or report that no route exists, and record:

- Total path cost
- Number of expanded nodes
- Search execution time
- Whether a route was found

## Evaluation Plan

We will compare all algorithms on identical problem instances while varying map size, obstacle density, movement costs, and start–goal separation.

Experiments will include simple maps with known answers, difficult layouts, and unreachable goals.

## Repository Structure

- `algorithms/` — Search algorithm implementations and heuristics
- `environment/` — Grid representation, map generation, and movement costs
- `visualization/` — Map and route display
- `experiments/` — Experiment runner and performance comparisons
- `tests/` — Correctness tests and small example cases
- `docs/` — Design notes and project documentation

## Setup and Running

Needs Python 3.10 or newer. No extra packages are needed. Run everything from the project folder.

```
python3 -m visualization.gui                 # window version (dropdowns, grid animation, instructions)
python3 main.py                              # text version
python3 -m unittest discover -v tests        # run the tests
python3 -m experiments.run_experiments       # 10 maps per condition (default)
python3 -m experiments.run_experiments 100   # 100 maps per condition
```

Map symbols: `.` normal cell (cost 1), `2`-`9` slower cells (stairs or crowded areas), `#` wall, and in the output `S` start, `G` goal, `*` route.
Positions are `(row, col)` starting from `(0, 0)` at the top left. Moving into a cell costs that cell's cost, and the start cell is free.
The heuristic is Manhattan distance × 1 (the cheapest move), so it never overestimates.
"Nodes expanded" counts each cell taken off the queue and expanded (duplicate queue entries are skipped and not counted).

Experiment results are saved to `experiments/results.csv`.

## Team

- Ates
- Sam
- Daphne
- Nadia
- Yumna

Algorithms, interface and code: Ates, Daphne, Sam  
Testing: Nadia, Yumna

## Working Together

1. Create a branch for your task.
2. Make and test your changes.
3. Open a pull request explaining the changes.
4. Ask a teammate to review before merging into `main`.

Keep each pull request focused on one task. Update setup instructions when adding dependencies or changing how the project runs.
