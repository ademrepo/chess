# Manual game: ONE knight moved by the player. It reuses the Knight class of the statement
# (move_forward / move_backward), so the human and the genetic algorithm follow the same rules.

from board import MOVES, NB_SQUARES, on_board
from knight import Knight


class KnightGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.knight = Knight()
        self.directions = []              # directions played, used by undo()

    @property
    def path(self):
        return self.knight.path

    @property
    def position(self):
        return self.knight.position

    @property
    def visited_count(self):
        return len(self.knight.path)

    def legal_squares(self):
        # Squares reachable now: inside the board and never visited.
        squares = []
        for direction, (dx, dy) in MOVES.items():
            target = (self.position[0] + dx, self.position[1] + dy)
            if on_board(target) and target not in self.knight.path:
                squares.append((direction, target))
        return squares

    def move_to(self, square):
        # Plays the move leading to `square` if it is legal. Returns True if the knight moved.
        for direction, target in self.legal_squares():
            if target == square:
                self.knight.move_forward(direction)
                self.directions.append(direction)
                return True
        return False

    def undo(self):
        if not self.directions:
            return False
        self.knight.move_backward(self.directions.pop())
        return True

    def is_complete(self):
        return self.visited_count == NB_SQUARES

    def is_stuck(self):
        return not self.is_complete() and not self.legal_squares()
