# Entry point of the program (the statement's main).
# Usage: python main.py                  -> interface (menu, settings, lab, game)
#        python main.py --console        -> the statement's loop, result in the terminal
#        python main.py --console --population 100 --mutation 0.02 --tournament 5 --seed 1

import argparse
import random

from board import NB_SQUARES, square_name
from population import Population


def main(population_size=50, mutation_probability=0.01, tournament_size=3):
    # Create the initial population
    population = Population(population_size, mutation_probability, tournament_size)
    while True:
        # Check the validity of the current population
        population.check_population()
        # Evaluate the current generation and get the best knight with its fitness value
        maxFit, bestSolution = population.evaluate()
        if maxFit == NB_SQUARES:
            break
        # Generate the new population
        population.create_new_generation()
    print("Solution found after %d generations (fitness %d)" % (population.generation, maxFit))
    print("Path:", " ".join(square_name(p) for p in bestSolution.path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Knight's Tour with a genetic algorithm")
    parser.add_argument("--console", action="store_true", help="no interface, run the GA")
    parser.add_argument("--population", type=int, default=50, help="population size")
    parser.add_argument("--mutation", type=float, default=0.01, help="mutation probability")
    parser.add_argument("--tournament", type=int, default=3, help="tournament size")
    parser.add_argument("--seed", type=int, default=None, help="random seed (reproducible run)")
    args = parser.parse_args()
    random.seed(args.seed)
    if args.console:
        main(args.population, args.mutation, args.tournament)
    else:
        from gui.app import App       # pygame is only needed for the interface
        App().run()
