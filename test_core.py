# Tests of the core (no interface). Run: python test_core.py

import random

from board import MOVES, NB_GENES, NB_SQUARES, on_board, square_name
from chromosome import Chromosome
from game import KnightGame
from genetic_algorithm import run_genetic_algorithm
from knight import Knight
from population import Population


def is_knight_move(a, b):
    return sorted((abs(a[0] - b[0]), abs(a[1] - b[1]))) == [1, 2]


def test_moves_table():
    assert sorted(MOVES) == [1, 2, 3, 4, 5, 6, 7, 8]
    assert all(is_knight_move((0, 0), m) for m in MOVES.values())
    assert square_name((0, 0)) == "a8" and square_name((7, 7)) == "h1"


def test_chromosome():
    c = Chromosome()
    assert len(c.genes) == NB_GENES and all(1 <= g <= 8 for g in c.genes)
    a, b = Chromosome([1] * NB_GENES), Chromosome([2] * NB_GENES)
    c1, c2 = a.crossover(b)
    assert len(c1.genes) == len(c2.genes) == NB_GENES
    assert set(c1.genes) == {1, 2} and set(c2.genes) == {1, 2}   # single point: both parents used
    assert c1.genes[0] == 1 and c1.genes[-1] == 2                # a prefix then a suffix
    m = Chromosome([1] * NB_GENES)
    m.mutation(0)
    assert m.genes == [1] * NB_GENES
    m.mutation(1)
    assert all(1 <= g <= 8 for g in m.genes)


def test_knight_forward_backward():
    k = Knight()
    assert k.position == (0, 0) and k.path == [(0, 0)] and k.fitness == 0
    k.move_forward(4)                    # down-right = (+1, +2)
    assert k.position == (1, 2) and k.path == [(0, 0), (1, 2)]
    k.move_backward(4)
    assert k.position == (0, 0) and k.path == [(0, 0)]


def test_check_moves_gives_legal_prefix():
    for _ in range(200):
        k = Knight()
        k.check_moves()
        k.evaluate_fitness()
        valid = k.path[:k.fitness]
        assert len(valid) == len(set(valid)) and all(on_board(p) for p in valid)
        assert all(is_knight_move(a, b) for a, b in zip(k.path, k.path[1:]))
        assert 1 <= k.fitness <= NB_SQUARES
        assert len(k.chromosome.genes) == NB_GENES


def test_cycle_order_forward_and_backward():
    # Gene 8 (up-left) from (0, 0) leaves the board. Forward cycle: 1, 2 illegal, 3 legal.
    # Backward cycle: 7, 6, 5 illegal (all leave the board), 4 legal (order given in the statement).
    original = random.choice
    try:
        for step, expected in ((1, 3), (-1, 4)):
            random.choice = lambda seq, s=step: s
            k = Knight(Chromosome([8] * NB_GENES))
            k.check_moves()
            assert k.chromosome.genes[0] == expected
            assert k.path[1] == (0 + MOVES[expected][0], 0 + MOVES[expected][1])
    finally:
        random.choice = original


def test_cycle_direction_is_the_same_for_the_whole_chromosome():
    original = random.choice
    calls = []
    try:
        random.choice = lambda seq: calls.append(1) or 1
        Knight().check_moves()
    finally:
        random.choice = original
    assert len(calls) == 1          # the direction is drawn once per chromosome


def test_fitness_stops_at_first_invalid():
    k = Knight(Chromosome([8] * NB_GENES))       # up-left from (0,0) leaves the board at once
    k.move_forward(8)
    assert k.evaluate_fitness() == 1


def test_population_generation():
    random.seed(1)
    p = Population(20)
    p.check_population()
    fit, best = p.evaluate()
    assert fit == best.fitness
    a, b = p.tournament_selection(3)
    assert a.fitness >= b.fitness and a is not b
    p.create_new_generation()
    assert len(p.knights) == 20 and p.generation == 2


def test_genetic_algorithm_finds_a_tour():
    random.seed(7)
    population = Population(50, 0.01)
    for _ in range(20000):
        population.check_population()
        max_fit, best = population.evaluate()
        if max_fit == NB_SQUARES:
            break
        population.create_new_generation()
    assert best.fitness == NB_SQUARES
    assert len(best.path) == len(set(best.path)) == NB_SQUARES
    assert all(on_board(p) for p in best.path)
    assert all(is_knight_move(a, b) for a, b in zip(best.path, best.path[1:]))


def test_genetic_algorithm_function_and_cancel():
    random.seed(7)
    best, generations, found = run_genetic_algorithm(50, 0.01, max_generations=20000, tournament_size=4)
    assert found and best.fitness == NB_SQUARES
    best, generations, found = run_genetic_algorithm(10, 0.01, should_stop=lambda: True)
    assert not found and generations == 1


def test_manual_game():
    g = KnightGame()
    assert g.position == (0, 0) and g.visited_count == 1
    assert {t for _, t in g.legal_squares()} == {(1, 2), (2, 1)}
    assert not g.move_to((5, 5))                 # not a knight move
    assert g.move_to((1, 2)) and g.position == (1, 2)
    assert not g.move_to((0, 0))                 # already visited
    assert g.undo() and g.position == (0, 0) and not g.undo()


def test_instrumentation_for_the_lab():
    random.seed(3)
    c = Chromosome([1] * NB_GENES)
    assert c.mutation(0) == [] and c.mutation(1) == list(range(NB_GENES))
    a, b = Chromosome([1] * NB_GENES), Chromosome([2] * NB_GENES)
    c1, _ = a.crossover(b)
    assert c1.genes[:a.last_cut] == [1] * a.last_cut and c1.genes[a.last_cut] == 2
    k = Knight()
    before = k.chromosome.genes[:]
    assert k.check_moves() == sum(x != y for x, y in zip(before, k.chromosome.genes))
    p = Population(20, 0.05, tournament_size=5)
    p.check_population()
    p.evaluate()
    assert 0 <= p.repaired_genes <= 20 * NB_GENES
    p.create_new_generation()
    assert len(p.trace["sample"]) == 5 and p.trace["sample"] == sorted(p.trace["sample"], reverse=True)
    assert p.mutated_genes >= len(p.trace["mutated"])


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
        print("ok  ", test.__name__)
    print("All %d tests passed." % len(tests))
