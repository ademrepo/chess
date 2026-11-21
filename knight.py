# Class 2 of the statement: Knight.
# The same class is used by the genetic algorithm (many knights in a population) and by the
# manual game (a single knight moved by the player, see game.py).

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
        # Cancel the last move (the direction is kept for symmetry with the statement).
        self.path.pop()
        self.position = self.path[-1]

    def is_position_valid(self):
        # Valid = inside the board and not visited before.
        return on_board(self.position) and self.position not in self.path[:-1]

    def check_moves(self):
        # Replays the whole chromosome from (0, 0). An illegal move is cancelled and replaced by
        # the next legal move found by cycling forward or backward through the 8 directions.
        # The cycle direction is drawn once and is the same for the whole chromosome.
        # If no direction is legal, the last tried move is kept.
        # The genes are corrected with the moves really applied.
        self.position = (0, 0)
        self.path = [self.position]
        step = random.choice((1, -1))          # +1: cycle forward, -1: cycle backward
        genes = self.chromosome.genes

        for i, direction in enumerate(genes):
            self.move_forward(direction)
            if self.is_position_valid():
                continue
            self.move_backward(direction)

            chosen = direction
            for k in range(1, NB_MOVES):
                chosen = (direction - 1 + step * k) % NB_MOVES + 1
                self.move_forward(chosen)
                if self.is_position_valid():
                    break
                if k < NB_MOVES - 1:           # the very last tried move is retained
                    self.move_backward(chosen)
            genes[i] = chosen

    def evaluate_fitness(self):
        # Walk along the path and count squares until an invalid one (outside the board or
        # already visited). Maximum value: 64.
        self.fitness = 0
        seen = set()
        for pos in self.path:
            if not on_board(pos) or pos in seen:
                break
            seen.add(pos)
            self.fitness += 1
        return self.fitness
