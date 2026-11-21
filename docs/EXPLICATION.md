# EXPLICATION — how the project works (for the oral)

## 1. The problem in one sentence

Find a sequence of 63 knight moves, starting at (0, 0), that visits all 64 squares once. The path
does not matter for the algorithm's design, only the final quality of the sequence: that is exactly the
kind of problem Chapter 2 solves with a **metaheuristic**. We use the **genetic algorithm**
(population-based, nature-inspired, stochastic, section 2.3.6).

## 2. Chapter 2 -> code

| Chapter 2 (genetic algorithm, Fig. 2.23) | Where in the code |
|------------------------------------------|-------------------|
| Individual / chromosome = array of genes | `Chromosome.genes`: 63 integers in 1..8 (integer representation) |
| Fitness function, higher = better | `Knight.evaluate_fitness()`: number of valid squares, max 64 |
| Initial population, random | `Population.__init__`: 50 knights with random chromosomes |
| Selection | `Population.tournament_selection(3)` |
| Crossover (single point, probability 1) | `Chromosome.crossover(partner)` |
| Mutation (low probability per gene) | `Chromosome.mutation(p)` |
| Replace the population, repeat | `Population.create_new_generation()` and the `while` loop in `genetic_algorithm.py` |
| Stopping condition | fitness == 64 (the interface also has a Cancel button and a 10 000 generations limit) |
| Best-so-far | `best_so_far` in `run_genetic_algorithm` |

## 3. The files

- `board.py`: constants and the table `MOVES`. Direction 1 = up-right = (+1, -2), then clockwise
  (2: (+2,-1), 3: (+2,+1), 4: (+1,+2), 5: (-1,+2), 6: (-2,+1), 7: (-2,-1), 8: (-1,-2)). The y axis goes
  down, (0, 0) is the top-left square (a8).
- `chromosome.py`: the genes. `crossover` cuts both parents at one random point and swaps the tails
  (two offspring). `mutation` replaces each gene by a random move with a small probability.
- `knight.py`: one candidate solution.
  - `move_forward(d)` adds the new position to `path`; `move_backward(d)` removes it.
  - `check_moves()` replays the chromosome from (0, 0). A random chromosome almost always leaves the
    board or revisits a square; the repair makes every knight start with a long legal path.
  - `evaluate_fitness()` counts the path until the first invalid square.
- `population.py`: the 50 knights, `check_population`, `evaluate`, `tournament_selection`,
  `create_new_generation`.
- `genetic_algorithm.py`: the statement's `main` loop, as a function (so the console and the interface
  use the same code).
- `game.py`: manual play. It **reuses `Knight`** (`move_forward` / `move_backward`) so the human and the
  algorithm obey the same rules. One knight only.
- `gui/`: pygame. `theme.py` (colours), `assets_loader.py` (SVG knight), `widgets.py` (button),
  `home_screen.py`, `game_screen.py`, `ga_job.py` (thread), `app.py` (window and loop).

## 4. `check_moves` in detail

For each gene (move) in order:

1. Apply it with `move_forward`. If the new square is on the board and unvisited, keep it.
2. Otherwise cancel it with `move_backward` and try the other directions by **cycling** from the
   current one: forward (d+1, d+2, ...) or backward (d-1, d-2, ...). The cycle direction is drawn
   **once per chromosome** and kept for all genes (as the statement says).
3. The first legal move found is kept. If none of the 7 other moves is legal, the **last tried move is
   retained** (so the path becomes invalid there and the fitness stops counting).
4. The gene is **overwritten** with the move really played, so the chromosome describes its own path.
   (Our choice: the statement says "corrects it". Consequence: the offspring inherit repaired moves.)

## 5. Selection, crossover, mutation

- **Tournament of size 3**: draw 3 different knights at random, sort by fitness, the two best are the
  parents. Fitter knights are more likely to reproduce, but a weak knight can still win a tournament
  against two weaker ones: this keeps diversity (diversification vs intensification, section 2.2.6).
- **Single-point crossover**: cut point between 1 and 62. Child 1 = start of parent 1 + end of parent 2;
  child 2 = the opposite. The statement uses it because the representation is not a permutation: any
  mix of moves is a valid chromosome (the repair fixes the legality afterwards), unlike the TSP where
  PMX / OX are needed (section 2.3.6, Example 3).
- **Mutation**: each gene becomes a random move with probability 0.01 (about 0.6 gene per chromosome).

## 6. Parameters and what we measured

Chapter 2 says the mutation probability is "typically very low, such as 0.001". The statement leaves
it free. Measures made on 2026-11-20 with `run_genetic_algorithm` (random seeds 0, 1, 2...):

| Population | Mutation | Result |
|------------|----------|--------|
| 50 | 0.01 | **30 runs out of 30 solved**, median **74** generations, maximum 195 (about 0.5 s per run) |
| 50 | 0.001 | 6 runs, cap 1500 generations: 4 solved in 36-58 generations, **2 never solved** (stuck) |
| 20 | 0.01 | 6 runs: 51 to 434 generations |
| 100 | 0.01 | 6 runs: 6 to 99 generations |

Reading: with 0.001 the population often loses its diversity and converges to a local optimum
("the algorithm can get stuck at a local optimum", section 2.3.6, Mutation): that is why we use 0.01.
A bigger population needs fewer generations but each generation costs more. The interface has no
control for these two values (the statement does not ask for one): it uses 50 and 0.01. To try other
values from the terminal: `python main.py --console --population 100 --mutation 0.02`.

## 7. The interface and the genetic algorithm button

- The window never freezes: `GAJob` runs `run_genetic_algorithm` in a **background thread** and the
  interface waits for its result. The calculation is not drawn.
- When it ends, the path is **replayed** move by move with the same `KnightGame.move_to`, which proves
  the solution respects the game rules. The speed button changes the replay speed (1x = 0.45 s per move).
- The algorithm always starts at (0, 0), as in the statement. It does not continue from the squares the
  human already played: pressing the button starts a new game.

## 8. Likely questions

**Why does `check_moves` write the genes back?** So that the chromosome matches the path actually
walked; otherwise the same illegal move would be repaired again, differently, each generation.

**Is crossover with probability 1 a problem?** No, it is the value of Chapter 2. Parents are not kept
unchanged (no elitism, not required), so the best fitness can go down from one generation to the next
(visible in the chart); the algorithm keeps the best-so-far.

**Is the algorithm guaranteed to stop?** Not in theory (it is stochastic). In practice it stopped in
all our runs with mutation 0.01. The interface adds a limit of 10 000 generations and a Cancel button;
the console mode follows the statement exactly (no limit).

**Why can two runs give different tours?** The algorithm is stochastic (random initial population,
selection, crossover point, mutation, cycle direction). `--seed` makes a run reproducible.

**Complexity of one generation?** `population_size x 63` moves for the repair and the evaluation, plus
`population_size` tournaments and crossovers of 63 genes: linear in `population_size x 63`.

**Why those pieces and not chess.com's?** chess.com assets are proprietary. We use the open **cburnett**
set (GPLv2+), see `specs/ASSETS.md` for author, URL, licence and file hashes. The colours of the board
only imitate the chess.com green theme.

## 9. Rules of programming followed

- Names and structure from the statement; one class per file.
- No logic in the interface: `gui/` only draws and calls `KnightGame` / `GAJob`.
- Tests of the core without pygame (`python test_core.py`).
- Every asset is documented before use.
