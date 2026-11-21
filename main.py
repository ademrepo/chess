# Entry point of the program.
# Usage: python main.py                  -> interface (home screen, then the game)
#        python main.py --console        -> genetic algorithm only, results in the terminal
#        python main.py --console --population 100 --mutation 0.02 --seed 1

import argparse
import random

from board import square_name
from genetic_algorithm import run_genetic_algorithm


def mode_console(population_size, mutation_probability, seed):
    if seed is not None:
        random.seed(seed)

    def show_progress(generation, best, average):
        if generation % 50 == 0:
            print("Generation %5d   best fitness = %2d   average = %.1f"
                  % (generation, best.fitness, average))

    best, generations, found = run_genetic_algorithm(
        population_size, mutation_probability, on_generation=show_progress)
    print("Solution found after %d generations (fitness %d)" % (generations, best.fitness))
    print("Path:", " ".join(square_name(p) for p in best.path))


def mode_gui():
    from gui.app import App       # pygame is only needed for the interface
    App().run()


def main():
    parser = argparse.ArgumentParser(description="Knight's Tour with a genetic algorithm")
    parser.add_argument("--console", action="store_true", help="no interface, run the GA")
    parser.add_argument("--population", type=int, default=50, help="population size")
    parser.add_argument("--mutation", type=float, default=0.01, help="mutation probability")
    parser.add_argument("--seed", type=int, default=None, help="random seed (reproducible run)")
    args = parser.parse_args()
    if args.console:
        mode_console(args.population, args.mutation, args.seed)
    else:
        mode_gui()


if __name__ == "__main__":
    main()
