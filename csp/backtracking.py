# Objective 1: Knight's Tour solved by plain backtracking (pseudo-code of the statement).

from knight_csp import Knight


def backtracking(knight):

    if len(knight.assignment) == 64:
        return knight

    all_possible_moves = knight.possibleMoves()

    for move in all_possible_moves:
        if knight.consistent(move):
            knight.addMove(move)
            result = backtracking(knight)
            if result is not None:
                return result
            knight.removeMove()

    return None
