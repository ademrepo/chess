# The main loop of the statement (def main) as a reusable function. It is used by the console
# mode and by the "Solve with Genetic Algorithm" button of the interface.

from board import NB_SQUARES
from population import Population


def run_genetic_algorithm(population_size=50, mutation_probability=0.01, max_generations=None,
                          on_generation=None, should_stop=None):
    # Returns (best knight found, number of generations, True if a full tour was found).
    # on_generation(generation, best_of_generation, average_fitness) is called after each
    # evaluation (used to draw the progress). should_stop() lets the interface cancel the run.

    # Create the initial population
    population = Population(population_size, mutation_probability)
    best_so_far = None

    while True:
        # Check the validity of the current population
        population.check_population()

        # Evaluate the current generation and get the best knight with its fitness value
        max_fit, best_solution = population.evaluate()
        if best_so_far is None or max_fit > best_so_far.fitness:
            best_so_far = best_solution
        if on_generation is not None:
            average = sum(k.fitness for k in population.knights) / len(population.knights)
            on_generation(population.generation, best_solution, average)
        if max_fit == NB_SQUARES:
            return best_solution, population.generation, True
        if should_stop is not None and should_stop():
            return best_so_far, population.generation, False
        if max_generations is not None and population.generation >= max_generations:
            return best_so_far, population.generation, False

        # Generate the new population
        population.create_new_generation()
