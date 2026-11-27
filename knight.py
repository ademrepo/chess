import random

from board import MOVES, NB_MOVES, on_board
from chromosome import Chromosome


class Knight:
    def __init__(self, chromosome=None):
# si on donne un chromosome on le garde sinn on en cree au hasard 
        self.chromosome = chromosome if chromosome is not None else Chromosome()
        self.position = (0, 0)
        self.path = [self.position]
        self.fitness = 0

    def move_forward(self, direction):
# cherche deplacement , maj pos et ajt au path 
        dx, dy = MOVES[direction]
        self.position = (self.position[0] + dx, self.position[1] + dy)
        self.path.append(self.position)

    def move_backward(self, direction):
# on soustrait la pos à enlever
        dx, dy = MOVES[direction]
        self.position = (self.position[0] - dx, self.position[1] - dy)
        self.path.pop()

    def check_moves(self):
    # on rejoue chromosone du debut 
        self.position = (0, 0)
        self.path = [self.position]
        visited = {self.position}          
        # sens au hasard     # 
        step = random.choice((1, -1))          
        genes = self.chromosome.genes  #liste des genes 


        corrected = 0

# parc les genes 
        for i, direction in enumerate(genes):
            for k in range(NB_MOVES):          # k = 0: the gene itself,1 le suivant dans le cycle 
                # num gene decalé de 4 crans en cercle 
                chosen = (direction - 1 + step * k) % NB_MOVES + 1
                # essaye mouvement
                self.move_forward(chosen)
                if (on_board(self.position) and self.position not in visited) or k == NB_MOVES - 1:
                    break                      # legal move (or last try, which is retained)
                self.move_backward(chosen)
            # apres avoir quitte boucle essais , on reecrit le gene 
            if chosen != genes[i]:

                corrected += 1#interface 

            genes[i] = chosen
            # note passage du cavalier 
            visited.add(self.position)


        return corrected #interface 

    def evaluate_fitness(self):
# cases dej comptees 
        seen = set()
        # parc cases du path dsi erreiru on sort sinn on ajt a seen 
        for pos in self.path:
            if not on_board(pos) or pos in seen:
                break
            seen.add(pos)
        self.fitness = len(seen)
        return self.fitness
