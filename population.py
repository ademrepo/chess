# Class 3 of the statement: Population.

import random

from knight import Knight


class Population:
    def __init__(self, population_size=50, mutation_probability=0.01):
        self.population_size = population_size
        self.mutation_probability = mutation_probability
        self.generation = 1
        self.knights = [Knight() for _ in range(population_size)]

    def check_population(self):
        # Repair the moves of every knight (Knight.check_moves).
        for knight in self.knights:
            knight.check_moves()

    def evaluate(self):
        # Fitness of every knight; returns the best fitness and the best knight.
        best = None
        for knight in self.knights:
            knight.evaluate_fitness()
            if best is None or knight.fitness > best.fitness:
                best = knight
        return best.fitness, best

    def tournament_selection(self, size=3):
        # Sample `size` knights at random, the two fittest become the parents.
        sample = random.sample(self.knights, size)
        sample.sort(key=lambda knight: knight.fitness, reverse=True)
        return sample[0], sample[1]

    def create_new_generation(self):
        # Selection -> crossover -> mutation until the new population has the same size.
        new_knights = []
        while len(new_knights) < self.population_size:
            parent1, parent2 = self.tournament_selection(3)
            child1, child2 = parent1.chromosome.crossover(parent2.chromosome)
            child1.mutation(self.mutation_probability)
            child2.mutation(self.mutation_probability)
            new_knights.append(Knight(child1))
            if len(new_knights) < self.population_size:
                new_knights.append(Knight(child2))
        self.knights = new_knights
        self.generation += 1
