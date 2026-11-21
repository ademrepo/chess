# Knight's Tour — genetic algorithm (Problem Solving, M1 Visual Computing, USTHB)

A genetic algorithm (Chapter 2) finds a knight's tour: the knight visits the 64 squares exactly once.
An interface lets you play, change the parameters and watch every calculation of the algorithm.

```
pip install -r requirements.txt     # pygame-ce (interface only)
python main.py                      # interface: menu, settings, algorithm lab, game, cat replay
python main.py --console --seed 1   # terminal only, reproducible
python main.py --console --population 100 --mutation 0.02 --tournament 5
python test_core.py                 # tests
```

## Interface

- **Settings**: population size, mutation probability, tournament size, generation limit.
- **Algorithm lab**: runs the algorithm generation by generation (Space = step, A = auto, R = new run).
  It shows the best knight's path and why it stops, the fitness curves, and the calculations of the
  last generation: tournament sample, single-point crossover and mutation drawn gene by gene,
  number of genes repaired, fitness.
- **Play**: solve the tour by hand, or press "Solve with Genetic Algorithm".
- **Watch the algorithm**: a cat jumps along the tour found.

## Structure

```
main.py               console mode and entry point of the interface
board.py              constants and helpers
chromosome.py         class Chromosome   (63 genes, single-point crossover, mutation)
knight.py             class Knight       (move_forward, move_backward, check_moves, evaluate_fitness)
population.py         class Population   (tournament selection, new generation)
genetic_algorithm.py  the statement's main loop as a function
game.py               manual game (reuses Knight)
gui/                  pygame screens: home, settings, lab, game, replay
test_core.py          tests
specs/                statement, Chapter 2, knight image (licence in specs/ASSETS.md)
```
