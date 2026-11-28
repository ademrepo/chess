# Knight's Tour (Problem Solving, M1 Visual Computing, USTHB)

The knight visits the 64 squares exactly once, starting from (0,0). Two projects, one interface:

- **Project 2**: a genetic algorithm (Chapter 2) finds the tour.
- **Project 3**: the tour as a CSP, solved by backtracking (objective 1, see `csp/README.md`).
  The backtracking with CSP heuristics (objective 2) is not done yet.

```
pip install -r requirements.txt     # pygame-ce (interface only)
python main.py                      # interface: choose a style, then menu, games, labs, replays
python main.py --console --seed 1   # genetic algorithm in the terminal, reproducible
python main.py --console --population 100 --mutation 0.02 --tournament 5
python test_core.py                 # tests of project 2 (12)
python csp/test_csp.py              # tests of project 3 (7)
python csp/main_backtracking.py     # backtracking in the terminal
```

## Interface

At the start you choose a style; both have the same features.

- **Chess Classic**: green board, white knight.
- **Cavalier Jack**: wooden board and panels (drawn by `gui/wood.py`), a cat is the piece.

Menu: **Play**, then Settings / Change style / Quit, then two columns.

- **Play**: solve the tour by hand, or press "Solve with Genetic Algorithm" or "Solve with CSP
  (Backtracking)"; the one that runs stays lit with a border.
- **Project 2 column** (genetic algorithm):
  - **Algorithm lab**: runs the algorithm generation by generation (Space = step, A = auto, R = new run).
    It shows the best knight's path and why it stops, the fitness curves, and the calculations of the
    last generation: tournament sample, single-point crossover and mutation drawn gene by gene,
    number of genes repaired, fitness.
  - **Watch the algorithm (cat)** (Cavalier Jack): the cat jumps along the tour found.
  - **Settings**: population size, mutation probability, tournament size, generation limit.
- **Project 3 column** (CSP backtracking):
  - **CSP backtracking (step by step)**: the search move by move, with the dead ends and the
    backtracks (Space = play, arrows = step, E = end, R = restart).
  - **Watch the backtracking (cat)** (Cavalier Jack): the cat replays the tour found.

## Structure

```
main.py               console mode and entry point of the interface
board.py              constants and helpers
chromosome.py         class Chromosome   (63 genes, single-point crossover, mutation)
knight.py             class Knight       (move_forward, move_backward, check_moves, evaluate_fitness)
population.py         class Population   (tournament selection, new generation)
genetic_algorithm.py  the statement's main loop as a function
game.py               manual game (reuses Knight)
gui/                  pygame screens (style choice, home, settings, labs, game, replays) in two styles;
                      theme.py (colours, style helpers), wood.py (wooden kit), cat.py (the cat)
csp/                  project 3: knight's tour as a CSP, objective 1 (README.md, TODO.md)
test_core.py          tests
specs/                statement, Chapter 2, knight image (licence in specs/ASSETS.md)
```
