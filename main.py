import argparse
import random

from board import NB_SQUARES, square_name
from population import Population


def main(population_size=50, mutation_probability=0.001, tournament_size=3):
    # Create the initial population
    population = Population(population_size, mutation_probability, tournament_size)
    
    while True:
        # repare cavalier et reecrit genes 
        population.check_population()
# note cavaliers et rend bet fitness et best cavalier 
        maxFit, bestSolution = population.evaluate()
    #    tt les cases parc on sort de la boucle 
        if maxFit == NB_SQUARES:
            break
        # Generate the new population sinn
        population.create_new_generation()
# affichage num gen et leilleur chemin 

    print("Solution found after %d generations (fitness %d)" % (population.generation, maxFit))
    print("Path:", " ".join(square_name(p) for p in bestSolution.path))


# pt dentree , val par def , hasard fixe , desactivation interfce 
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
