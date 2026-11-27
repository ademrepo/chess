import random
from board import NB_GENES, NB_MOVES


class Chromosome:
    def __init__(self, genes=None):
        #chromosome de la population initiale on fabrique randomly 
        if genes is None:
            self.genes = [random.randint(1, NB_MOVES) for _ in range(NB_GENES)]
        else:
            # on copie et range dans sa liste 
            self.genes = list(genes)


        self.last_cut = None            # cut point of the last crossover (shown by the interface)

    def crossover(self, partner):

# endroit coupure entre 1 et 62
        point = random.randint(1, NB_GENES - 1)


        self.last_cut = point

# on colle les deux morceaux echangés de listes a partir de la coupure 
        child1 = Chromosome(self.genes[:point] + partner.genes[point:])
        child2 = Chromosome(partner.genes[:point] + self.genes[point:])
        return child1, child2

    def mutation(self, mutation_probability=0.01):

        mutated = []

        # parc le s 63 genes 
        for i in range(NB_GENES):
            # si un nb entre 0 et 1 est < 0.01 alors ya mutation 
            if random.random() < mutation_probability:
                self.genes[i] = random.randint(1, NB_MOVES)

# juste pour interface 
                mutated.append(i) 
        return mutated
