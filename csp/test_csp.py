# Tests of objective 1.  python test_csp.py
import sys

from backtracking import backtracking
from knight_csp import Knight, legal_knight_moves

sys.setrecursionlimit(10000)


def test_start_is_x0():
    assert Knight().assignment == [(0, 0)]


def test_domain_of_x1_from_corner():
    # From (0, 0) only (1, 2) and (2, 1) are on the board.
    assert sorted(Knight().possibleMoves()) == [(1, 2), (2, 1)]


def test_legal_moves_are_l_shaped_and_on_board():
    for i in range(8):
        for j in range(8):
            for (a, b) in legal_knight_moves((i, j)):
                assert 0 <= a < 8 and 0 <= b < 8
                assert sorted((abs(a - i), abs(b - j))) == [1, 2]


def test_consistent_checks_the_three_constraints():
    k = Knight()
    assert k.consistent((1, 2))            # legal, free, on board
    assert not k.consistent((0, 0))        # all-different (already visited)
    assert not k.consistent((1, 1))        # not an L move
    assert not k.consistent((-1, 2))       # outside the board
    assert not k.consistent((8, 1))        # outside the board


def test_add_and_remove_move():
    k = Knight()
    k.addMove((1, 2))
    assert k.assignment == [(0, 0), (1, 2)]
    assert (1, 2) not in k.possibleMoves()
    k.removeMove()
    assert k.assignment == [(0, 0)]


def known_tour():
    # A full tour from (0, 0) built with Warnsdorff's rule, only used to prepare the tests.
    k = Knight()
    while len(k.assignment) < 64:
        k.addMove(min(k.possibleMoves(), key=lambda m: len(
            [n for n in legal_knight_moves(m) if n not in k.assignment])))
    return k.assignment


def check_tour(a):
    assert len(a) == 64 and a[0] == (0, 0)
    assert len(set(a)) == 64                                                 # all-different
    assert all(0 <= i < 8 and 0 <= j < 8 for i, j in a)                      # boundaries
    assert all(a[k] in legal_knight_moves(a[k - 1]) for k in range(1, 64))  # knight moves


def test_backtracking_completes_a_partial_tour():
    # The plain backtracking on the full 8x8 board is very slow (see README), so we start
    # from the first 45 moves of a known tour and let it find the 19 remaining ones.
    knight = Knight()
    knight.assignment = known_tour()[:45]
    result = backtracking(knight)
    assert result is not None
    check_tour(result.assignment)


def test_backtracking_returns_none_when_blocked():
    # The knight is on (0, 0) and both squares it can reach are already visited: no move.
    knight = Knight()
    knight.assignment = [(1, 2), (2, 1), (0, 0)]
    assert backtracking(knight) is None


if __name__ == "__main__":
    tests = [t for name, t in sorted(globals().items()) if name.startswith("test_")]
    for t in tests:
        t()
        print("ok", t.__name__)
    print(len(tests), "tests passed")
