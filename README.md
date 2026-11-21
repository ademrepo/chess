# Knight's Tour — genetic algorithm (Problem Solving, M1 Visual Computing, USTHB)

The knight must visit the 64 squares of a chessboard exactly once. You can play it yourself with one
knight, or press **Solve with Genetic Algorithm** and watch the algorithm of Chapter 2 find a tour.

## Run

```
pip install -r requirements.txt     # pygame-ce (once)
python main.py                      # home screen -> "Play" or "Watch the algorithm"
python main.py --console --seed 1   # only the algorithm, in the terminal
python test_core.py                 # tests of the core
python benchmark.py 50              # statistics over 50 runs
```

Python 3 required (tested with 3.14).

## How to play

| Action | Mouse | Key |
|--------|-------|-----|
| Move the knight | click a square marked with a grey dot | |
| Undo | button *Undo* | `Z` |
| New game | button *New game* | `R` |
| Solve with the genetic algorithm | green button (becomes *Cancel*) | `G` |
| Back to the home screen | button *Menu* | `Esc` |

The algorithm uses the statement's values (population 50, mutation probability 0.01). When it finds a
full tour (fitness 64) the tour is replayed move by move; the **replay speed** button changes the
speed and *Path* shows or hides the line drawn by the knight.

## Structure

```
main.py               entry point
board.py              constants and helpers
chromosome.py         class Chromosome   (63 genes, single-point crossover, mutation)
knight.py             class Knight       (move_forward, move_backward, check_moves, evaluate_fitness)
population.py         class Population   (tournament selection, new generation)
genetic_algorithm.py  the loop of the statement's main()
game.py               manual game with one knight
gui/                  pygame interface (home, manual game, replay with the cat, GA thread)
assets/               sprite sheets of the replay screen (cat, wooden UI)
benchmark.py          generations / time over many runs
test_core.py          tests
specs/                statement, Chapter 2, assets and their sources
docs/                 EXPLICATION.md (notes for the oral)
```

## Where things come from

- Algorithm: the statement `specs/Project 2.pdf` and Chapter 2 `specs/Chapter 2.pdf`
  (summary in `specs/SPEC.md`).
- Cat and wooden interface of the replay screen: `assets/` (source and licence in `specs/ASSETS.md`).
- Chess pieces: **cburnett** set by Colin M.L. Burnett, GPLv2+, taken from the Lichess repository.
  Full sources, licence and file hashes: **`specs/ASSETS.md`**. Nothing comes from chess.com; the
  green look is only imitated with colours and shapes drawn by the code.
- Explanations for the oral: `docs/EXPLICATION.md`.

## Replay screen

`Space` play / pause, `R` new run (history of the runs is kept), `Esc` menu; the gear button changes
the speed. The calculation runs in a background thread and shows the generation counter.
