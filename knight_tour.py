"""Problème du cavalier résolu par un algorithme génétique (sujet du Projet 2)."""

import random
import time

TAILLE_PLATEAU = 8
NB_GENES = TAILLE_PLATEAU * TAILLE_PLATEAU - 1  # 63 coups pour visiter 64 cases
FITNESS_MAX = TAILLE_PLATEAU * TAILLE_PLATEAU
NB_DIRECTIONS = 8

TAILLE_POPULATION = 50
TAILLE_TOURNOI = 3
# Le cours cite 0.001, mais avec 63 gènes les runs essayés (0.001 et 0.005) ne se terminaient
# pas en temps raisonnable. Sur 50 runs, 0.01 donne la médiane (59) et la durée (0,56 s) les
# plus basses, contre 120 / 0,94 s pour 0.02 et 132 / 1,03 s pour 0.03.
TAUX_MUTATION = 0.01
PAS_AFFICHAGE_CONSOLE = 50  # on affiche une génération sur 50 pour ne pas ralentir

# Décalages (dx, dy) des directions 1 à 8, dans le sens horaire.
# (0, 0) est en haut à gauche et y descend : « up » = y - 1.
DECALAGES = {
    1: (1, -2),   # up-right
    2: (2, -1),   # right-up
    3: (2, 1),    # right-down
    4: (1, 2),    # down-right
    5: (-1, 2),   # down-left
    6: (-2, 1),   # left-down
    7: (-2, -1),  # left-up
    8: (-1, -2),  # up-left
}


def dans_le_plateau(position):
    x, y = position
    return 0 <= x < TAILLE_PLATEAU and 0 <= y < TAILLE_PLATEAU


def coup_aleatoire():
    return random.randint(1, NB_DIRECTIONS)


def coups_a_essayer(gene, sens_du_cycle):
    """Le coup d'origine, puis les 7 autres dans l'ordre du cycle."""
    return [(gene - 1 + sens_du_cycle * pas) % NB_DIRECTIONS + 1 for pas in range(NB_DIRECTIONS)]


class Chromosome:
    """Les 63 coups d'un cavalier."""

    def __init__(self, genes=None):
        if genes is None:
            genes = [coup_aleatoire() for _ in range(NB_GENES)]
        self.genes = genes

    def crossover(self, partner):
        """Croisement à un point, toujours appliqué : retourne deux enfants."""
        point = random.randint(1, NB_GENES - 1)
        enfant1 = Chromosome(self.genes[:point] + partner.genes[point:])
        enfant2 = Chromosome(partner.genes[:point] + self.genes[point:])
        return enfant1, enfant2

    def mutation(self):
        """Chaque gène a TAUX_MUTATION chances de devenir un coup aléatoire."""
        for i in range(NB_GENES):
            if random.random() < TAUX_MUTATION:
                self.genes[i] = coup_aleatoire()


class Knight:
    """Un cavalier : son chromosome, le chemin qu'il parcourt et sa fitness."""

    def __init__(self, chromosome=None):
        self.position = (0, 0)
        self.chromosome = chromosome if chromosome is not None else Chromosome()
        self.path = [self.position]
        self.fitness = 0

    def move_forward(self, direction):
        dx, dy = DECALAGES[direction]
        x, y = self.position
        self.position = (x + dx, y + dy)
        self.path.append(self.position)

    def move_backward(self, direction):  # direction : signature imposée par le sujet
        self.path.pop()
        self.position = self.path[-1]

    def check_moves(self):
        """Rejoue le chromosome en corrigeant les coups illégaux.

        Le sens du cycle est tiré une seule fois pour tout le chromosome.
        Les gènes corrigés sont réécrits pour que les enfants en héritent.
        """
        self.position = (0, 0)
        self.path = [self.position]
        cases_visitees = {self.position}
        sens_du_cycle = random.choice([1, -1])

        genes = self.chromosome.genes
        for i, gene_initial in enumerate(genes):
            for gene in coups_a_essayer(gene_initial, sens_du_cycle):
                if self.essayer_coup(gene, cases_visitees):
                    break
            else:  # aucun coup valide : on garde le dernier essayé, même invalide
                genes[i] = gene
                self.move_forward(gene)
                return
            genes[i] = gene
            cases_visitees.add(self.position)

    def essayer_coup(self, direction, cases_visitees):
        """Applique le coup ; l'annule s'il est illégal. Retourne s'il est valide."""
        self.move_forward(direction)
        valide = dans_le_plateau(self.position) and self.position not in cases_visitees
        if not valide:
            self.move_backward(direction)
        return valide

    def evaluate_fitness(self):
        """Compte les positions valides du path jusqu'au premier coup invalide."""
        cases_visitees = set()
        self.fitness = 0
        for position in self.path:
            if not dans_le_plateau(position) or position in cases_visitees:
                break
            cases_visitees.add(position)
            self.fitness += 1
        return self.fitness


class Population:
    """Une génération de cavaliers."""

    def __init__(self, population_size):
        self.population_size = population_size
        self.generation = 1
        self.knights = [Knight() for _ in range(population_size)]

    def check_population(self):
        for knight in self.knights:
            knight.check_moves()

    def evaluate(self):
        for knight in self.knights:
            knight.evaluate_fitness()
        meilleur_cavalier = max(self.knights, key=lambda knight: knight.fitness)
        return meilleur_cavalier.fitness, meilleur_cavalier

    def tournament_selection(self, size):
        participants = random.sample(self.knights, size)
        participants.sort(key=lambda knight: knight.fitness, reverse=True)
        return participants[0], participants[1]

    def create_new_generation(self):
        nouveaux_cavaliers = []
        while len(nouveaux_cavaliers) < self.population_size:
            parent1, parent2 = self.tournament_selection(TAILLE_TOURNOI)
            enfants = parent1.chromosome.crossover(parent2.chromosome)
            for enfant in enfants:
                enfant.mutation()
                nouveaux_cavaliers.append(Knight(enfant))
        self.knights = nouveaux_cavaliers
        self.generation += 1


def lancer_run(population_size=TAILLE_POPULATION):
    """Un run complet. Retourne (meilleur cavalier, générations, durée, fitness moyenne)."""
    debut = time.perf_counter()
    population = Population(population_size)
    while True:
        # Vérifie la validité de la population courante
        population.check_population()
        # Évalue la génération et récupère le meilleur cavalier
        maxFit, bestSolution = population.evaluate()
        if population.generation % PAS_AFFICHAGE_CONSOLE == 0:
            print(f"génération {population.generation} : meilleure fitness {maxFit}")
        if maxFit == FITNESS_MAX:
            break
        # Génère la nouvelle population
        population.create_new_generation()

    duree = time.perf_counter() - debut
    fitness_moyenne = sum(k.fitness for k in population.knights) / population_size
    return bestSolution, population.generation, duree, fitness_moyenne

