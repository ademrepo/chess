# Class 1 of the statement: Chromosome.
# Integer representation (Chapter 2, "Solution representation"): 63 genes, each gene is one of
# the 8 knight moves.

import random

from board import NB_GENES, NB_MOVES


class Chromosome:
    def __init__(self, genes=None):
        # Without genes (initial population) the chromosome is random.
        if genes is None:
            self.genes = [random.randint(1, NB_MOVES) for _ in range(NB_GENES)]
        else:
            self.genes = list(genes)
        self.last_cut = None            # cut point of the last crossover (shown by the interface)

    def crossover(self, partner):
        # Single-point crossover (Figure 2.23 of Chapter 2, crossover probability = 1).
        # Returns the two offspring.
        point = random.randint(1, NB_GENES - 1)
        self.last_cut = point
        child1 = Chromosome(self.genes[:point] + partner.genes[point:])
        child2 = Chromosome(partner.genes[:point] + self.genes[point:])
        return child1, child2

    def mutation(self, mutation_probability=0.01):
        # Each gene has a small probability to become a random move (diversification).
        # Returns the positions of the mutated genes.
        mutated = []
        for i in range(NB_GENES):
            if random.random() < mutation_probability:
                self.genes[i] = random.randint(1, NB_MOVES)
                mutated.append(i)
        return mutated
