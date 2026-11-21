# Class 3 of the statement: Population.

import random

from knight import Knight


class Population:
    def __init__(self, population_size=50, mutation_probability=0.01, tournament_size=3):
        self.population_size = population_size
        self.mutation_probability = mutation_probability
        self.tournament_size = tournament_size
        self.generation = 1
        self.knights = [Knight() for _ in range(population_size)]
        # Figures of the last calculations, only read by the interface to explain the algorithm.
        self.repaired_genes = 0       # genes corrected by check_population
        self.trace = None             # first selection + crossover + mutation of the last generation
        self.mutated_genes = 0        # genes mutated while building the last generation
        self.last_sample = []         # fitness of the last tournament sample, best first

    def check_population(self):
        # Repair the moves of every knight (Knight.check_moves).
        self.repaired_genes = sum(knight.check_moves() for knight in self.knights)

    def evaluate(self):
        # Fitness of every knight; returns the best fitness and the best knight.
        for knight in self.knights:
            knight.evaluate_fitness()
        best = max(self.knights, key=lambda knight: knight.fitness)
        return best.fitness, best

    def tournament_selection(self, size=3):
        # Sample `size` knights at random, the two fittest become the parents.
        sample = random.sample(self.knights, size)
        sample.sort(key=lambda knight: knight.fitness, reverse=True)
        self.last_sample = [knight.fitness for knight in sample]
        return sample[0], sample[1]

    def create_new_generation(self):
        # Selection -> crossover -> mutation until the new population has the same size.
        new_knights = []
        self.trace = None
        self.mutated_genes = 0
        while len(new_knights) < self.population_size:
            parent1, parent2 = self.tournament_selection(self.tournament_size)
            child1, child2 = parent1.chromosome.crossover(parent2.chromosome)
            before_mutation = child1.genes[:]
            mutated1 = child1.mutation(self.mutation_probability)
            mutated2 = child2.mutation(self.mutation_probability)
            self.mutated_genes += len(mutated1) + len(mutated2)
            if self.trace is None:
                self._keep_example(parent1, parent2, before_mutation, child1, mutated1)
            new_knights += [Knight(child1), Knight(child2)]
        self.knights = new_knights[:self.population_size]
        self.generation += 1

    def _keep_example(self, parent1, parent2, before_mutation, child, mutated):
        # Only for the interface: the first pair of the generation is kept as a worked example.
        self.trace = {
            "sample": self.last_sample,
            "parent1": parent1.chromosome.genes[:], "parent2": parent2.chromosome.genes[:],
            "cut": parent1.chromosome.last_cut,
            "child": child.genes[:], "child_before_mutation": before_mutation,
            "mutated": mutated,
        }
