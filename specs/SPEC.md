# SPEC — Knight's Tour with a genetic algorithm (Problem Solving, M1 Visual Computing, USTHB)

Source of truth of the project. Section 1 is the project statement (`specs/Project 2.pdf`, Dr. Meriem
SEBAI, 2026/2027), section 2 lists what Chapter 2 (`specs/Chapter 2.pdf`) provides, section 3 lists
what was added on top of the statement. Never contradict section 1.

---

## 1. Project statement (Project 2)

**Solving the Knight's Tour problem using the genetic algorithm**

A knight moves in an "L-shaped" pattern: two squares in one direction, then one square to the left or
to the right (8 possible moves, Figure 1 of the statement). A knight's tour is a sequence of moves that
visits every square of the chessboard exactly once.

Objective: tackle the knight's tour with a genetic algorithm, with these classes.

### 1.1 Chromosome class
- attribute `genes`: array of length **63**, each gene is one of the **8** possible moves.
- `init(genes)`: creates a chromosome; without genes (initial population) it generates random genes.
- `crossover(partner)`: combines the genes of both chromosomes into new offspring, **single-point
  crossover**.
- `mutation()`: each gene has a probability to mutate into a random move (to explore new moves).

### 1.2 Knight class
Variables:
- `position`: coordinates (x, y) of the current position.
- `chromosome`: the sequence of moves.
- `path`: list of the positions after applying the moves of the chromosome.
- `fitness`: value of the fitness function, **maximum 64** (number of squares).

Functions:
- `init(chromosome)`: creates a knight; without chromosome it generates one. Sets position to **(0, 0)**,
  fitness to 0 and saves the initial position in `path`.
- `move_forward(direction)`: moves the knight in one of the 8 directions (1: up-right, 2: right-up,
  3: right-down, 4: down-right, 5: down-left, 6: left-down, 7: left-up, 8: up-left) and gives the new
  position.
- `move_backward(direction)`: traces back if the applied move is illegal.
- `check_moves()`: checks every move of the chromosome. A move is invalid if it places the knight
  outside the board or on an already visited square. An illegal move is cancelled with
  `move_backward`, then other moves are tried by **cycling forward or backward**. The cycle direction
  is **random and the same for the whole chromosome**. If no valid move is found, the last move is
  retained. Example: current move 4 (down-right) illegal, forward cycle -> 5, 6, 7, 8, 1, 2, 3;
  backward cycle -> 3, 2, 1, 8, 7, 6, 5.
- `evaluate_fitness()`: loops through `path` and increments the fitness until an invalid move is met.
  If all squares are visited the fitness is 64.

### 1.3 Population class
Attributes: `population_size` (e.g. 50), `generation` (initially 1), `knights` (list of knights).

Functions:
- `init(population_size)`: generates the initial list of knights, generation = 1.
- `check_population()`: calls `check_moves()` on every knight.
- `evaluate()`: calls `evaluate_fitness()` on every knight, returns the best knight with its fitness.
- `tournament_selection(size)`: n knights are sampled at random, the **two best** are chosen. **Sample
  size 3.**
- `create_new_generation()`: new population of the same size; in each iteration two parents come from
  `tournament_selection(size)`, crossover gives two offspring, mutation is applied to each offspring;
  increments the generation counter.

(The statement numbers its classes 1, 2, 3 then 5: there is no item 4. The main function is item 5.)

### 1.4 Main function
Applies a run of the genetic algorithm and displays the optimal solution on an interface (Figure 2 of
the statement: board with the visited squares numbered and the knight drawn).

```python
def main():
    population_size = 50
    population = Population(population_size)          # initial population
    while True:
        population.check_population()                 # validity of the current population
        maxFit, bestSolution = population.evaluate()  # best knight and its fitness
        if maxFit == 64:
            break
        population.create_new_generation()
    # create the user interface to display the solution
if __name__ == "__main__":
    main()
```

---

## 2. What Chapter 2 (Metaheuristics) gives us

- Metaheuristics = algorithms for problems where the *goal state* matters, not the path (section 2.1);
  the knight's tour is a combinatorial, NP-hard-like search (section 2.2.2).
- Genetic algorithm = population-based, nature-inspired, stochastic, iterative (section 2.2.5).
- Figure 2.23: initial population -> (selection -> crossover -> mutation) until the new population is
  full -> replace -> keep the best-so-far -> stop when the stopping condition is met.
- Representation: integer genes (section 2.3.6 "Solution representation").
- Selection: tournament selection among the listed strategies (random, roulette wheel, tournament, rank,
  Boltzmann).
- Crossover: single-point (probability 1); mutation: probability per gene, "very low" (0.001 in the
  chapter's examples) because it keeps diversity but slows convergence.
- Exploration vs exploitation (section 2.2.6): mutation and the population give diversification,
  selection gives intensification.
- Elitism is optional; the statement does not ask for it, so it is **not** used.

---

## 3. Additions requested by the team (2026-11-20)

These do not change section 1; they extend the "interface" part of the statement.

1. `main.py` entry point and a readable file structure (one file per class of the statement).
2. A **home screen** with a "Play" button shown before the game.
3. A **manual mode**: the user plays the tour with **one knight**, clicking the highlighted squares.
4. A **button "Solve with Genetic Algorithm"** that runs the statement's algorithm and replays the
   solution on the same board. The algorithm runs in a background thread (the window never freezes) and
   can be cancelled. The calculation itself is not drawn; only the final tour is replayed, at a speed
   the user can change. The statement does not ask for controls on the population size or the mutation
   probability, so there are none: the interface uses population 50 and mutation 0.01.
5. Look inspired by chess.com (green board, dark page, 3D green buttons, move dots) **without using any
   chess.com file**. Every asset is listed with its source and licence in `specs/ASSETS.md`.
6. Project documentation in the style of the Sokoban project: `CLAUDE.md`, `docs/PLAN.md`,
   `docs/EXPLICATION.md`, `docs/logs/`, assets in `specs/`.

Parameters not fixed by the statement (our choices, see `docs/EXPLICATION.md`):
mutation probability 0.01; safety limit of 10 000 generations in the interface only (the statement's
loop has none); a gene corrected by `check_moves` is written back into the chromosome.
