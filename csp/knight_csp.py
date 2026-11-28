# Knight's Tour as a CSP (Project 3, Dr. Meriem SEBAI, USTHB).
#
# Formulation of the statement:
#   Variables    X0, X1, ..., X63   Xk = board position of the knight after the k-th move
#   Domains      D(X0) = {(0, 0)}
#                D(Xk) = unvisited squares reachable by a knight move from X(k-1)   (k > 0)
#   Constraints  1. Knight move     Xk in LegalKnightMoves(X(k-1))
#                2. All-different   Xi != Xj for all i != j
#                3. Board boundaries 0 <= row < 8 and 0 <= col < 8
#
# A position is (i, j) = (row, col), as in the statement; (0, 0) is the top-left square.

BOARD_SIZE = 8
NB_SQUARES = BOARD_SIZE * BOARD_SIZE     # 64 variables X0 ... X63
START = (0, 0)                           # X0

# The 8 knight moves (di, dj) of Figure 1 of the statement: two squares in one direction,
# then one square to the left or to the right.
#
# The ORDER of this list is the order in which backtracking tries the moves. Plain backtracking
# is blind, so this order decides if the tour is found in 0.3 s or never (most of the orders
# tried did not finish in 1 million nodes). This one finds the tour after about 35 000 nodes.
KNIGHT_MOVES = [
    (-1, 2), (1, 2), (2, 1), (2, -1),
    (-2, -1), (-2, 1), (-1, -2), (1, -2),
]


def legal_knight_moves(position):
    # LegalKnightMoves(X): the squares a knight can jump to from X (constraints 1 and 3).
    i, j = position
    moves = []
    for di, dj in KNIGHT_MOVES:
        target = (i + di, j + dj)
        if 0 <= target[0] < BOARD_SIZE and 0 <= target[1] < BOARD_SIZE:
            moves.append(target)
    return moves


class Knight:
    def __init__(self):
        # assignment = [X0, X1, ..., Xk]: the positions assigned so far; X0 = (0, 0).
        self.assignment = [START]
        self.nodes = 0               # number of moves assigned so far (to compare the algorithms)

    def possibleMoves(self):
        # Domain of the next variable: unvisited squares reachable from the last position.
        return [m for m in legal_knight_moves(self.assignment[-1]) if m not in self.assignment]

    def consistent(self, move):
        # Checks the 3 constraints for the value `move` of the next variable.
        i, j = move
        in_board = 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE                  # boundaries
        legal = move in legal_knight_moves(self.assignment[-1])                 # knight move
        all_different = move not in self.assignment                             # all-different
        return in_board and legal and all_different

    def addMove(self, move):
        # Assigns `move` to the next variable.
        self.assignment.append(move)
        self.nodes += 1

    def removeMove(self):
        # Un-assigns the last variable (backtrack).
        self.assignment.pop()
