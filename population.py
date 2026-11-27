import random
from knight import Knight

class Population:
    def __init__(self, population_size=50, mutation_probability=0.05, tournament_size=3):
        # rangement parametres 
        self.population_size = population_size
        self.mutation_probability = mutation_probability
        self.tournament_size = tournament_size

# cpt generation 
        self.generation = 1
        # on fab 50 cavaliers ,chacun nayant pas darg crée son chromosome  
        self.knights = [Knight() for _ in range(population_size)]


# interface lab 
        self.repaired_genes = 0       # genes corrected by check_population
        self.trace = None             #exemple de croiseme,t 
        self.mutated_genes = 0        # combien de genes mutes 
        self.last_sample = []         # fitness of the last tournament sample, best first

    def check_population(self):
# pour chaque cvalier on apl check moves , on add nb genes corriges  on range dasn self repaired 
        self.repaired_genes = sum(knight.check_moves() for knight in self.knights)

    def evaluate(self):

        for knight in self.knights:
            # chaquze cavalier compte cases valides 
            knight.evaluate_fitness()
            # prend fitness la plus grande parmi cavaliers
        best = max(self.knights, key=lambda knight: knight.fitness)
        return best.fitness, best  #meilleure note et best cavalier 


    def tournament_selection(self, size=3):
# tire 3 cavaliers au hasard ;trie fitness decroissant ; ;on rend les deux premiers  
        sample = random.sample(self.knights, size)
        sample.sort(key=lambda knight: knight.fitness, reverse=True)
        self.last_sample = [knight.fitness for knight in sample]
        return sample[0], sample[1]

    def create_new_generation(self):
        # Selection , crossover ,mutation until the new population has the same size.
        new_knights = []
# cpt daffichage 
        self.trace = None
        self.mutated_genes = 0
        # tant quon n a pas 50 cavaliers 
        while len(new_knights) < self.population_size:
            # on pren les deux leilleurs aprents et on leur cree des enfants avec crossover 
            parent1, parent2 = self.tournament_selection(self.tournament_size)
            child1, child2 = parent1.chromosome.crossover(parent2.chromosome)
            # sauvegarde avant 
            before_mutation = child1.genes[:]
            # chaque enfant subit mutation 
            mutated1 = child1.mutation(self.mutation_probability)
            mutated2 = child2.mutation(self.mutation_probability)

# cpt genes mutés et prendn premiere paire; on affiche le nb total de genes mutes  
            self.mutated_genes += len(mutated1) + len(mutated2) #pos des genes mutes 
            if self.trace is None:
                self._keep_example(parent1, parent2, before_mutation, child1, mutated1)

        
            # nv cavalie r pour chaque enfant et on ajt (knight cree cavalier qui va de 0 ), ajt a new knights
            new_knights += [Knight(child1), Knight(child2)]
    #    remplace anciens cavaliers par nv 
        self.knights = new_knights[:self.population_size]
        # cpt de generation 
        self.generation += 1











# ecran du laboratoire 
    def _keep_example(self, parent1, parent2, before_mutation, child, mutated):
        # Only for the interface: the first pair of the generation is kept as a worked example.
        self.trace = {
            "sample": self.last_sample,
            "parent1": parent1.chromosome.genes[:], "parent2": parent2.chromosome.genes[:],
            "cut": parent1.chromosome.last_cut,
            "child": child.genes[:], "child_before_mutation": before_mutation,
            "mutated": mutated,
        }
