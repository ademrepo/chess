# Class 2 of the statement: Knight.
# One knight = one candidate solution: its chromosome, the path it walks and its fitness.

import random

from board import MOVES, NB_MOVES, on_board
from chromosome import Chromosome


class Knight:
    def __init__(self, chromosome=None):
        # Without chromosome (initial population) the knight creates a random one.
        self.chromosome = chromosome if chromosome is not None else Chromosome()
        self.position = (0, 0)
        self.path = [self.position]
        self.fitness = 0

    def move_forward(self, direction):
        # Apply one move (1..8): the new position is added to the path.
        dx, dy = MOVES[direction]
        self.position = (self.position[0] + dx, self.position[1] + dy)
        self.path.append(self.position)

    def move_backward(self, direction):
        # Cancel the move `direction` that was just applied: go back and forget the position.
        dx, dy = MOVES[direction]
        self.position = (self.position[0] - dx, self.position[1] - dy)
        self.path.pop()

    def check_moves(self):
        # Replays the whole chromosome from (0, 0). An illegal move (outside the board or on an
        # already visited square) is cancelled with move_backward and replaced by the next legal
        # move found by cycling forward or backward through the 8 directions.
        # The cycle direction is drawn once and is the same for the whole chromosome.
        # If no direction is legal, the last tried move is kept.
        # The genes are corrected with the moves really applied; returns how many were corrected.
        self.position = (0, 0)
        self.path = [self.position]
        visited = {self.position}              # set: fast "already visited?" test
        step = random.choice((1, -1))          # +1: cycle forward, -1: cycle backward
        genes = self.chromosome.genes
        corrected = 0

        for i, direction in enumerate(genes):
            for k in range(NB_MOVES):          # k = 0: the gene itself, then the cycle
                chosen = (direction - 1 + step * k) % NB_MOVES + 1
                self.move_forward(chosen)
                if (on_board(self.position) and self.position not in visited) or k == NB_MOVES - 1:
                    break                      # legal move (or last try, which is retained)
                self.move_backward(chosen)
            if chosen != genes[i]:
                corrected += 1
            genes[i] = chosen
            visited.add(self.position)
        return corrected

    def evaluate_fitness(self):
        # Walk along the path and count squares until an invalid one (outside the board or
        # already visited). Maximum value: 64.
        seen = set()
        for pos in self.path:
            if not on_board(pos) or pos in seen:
                break
            seen.add(pos)
        self.fitness = len(seen)
        return self.fitness
