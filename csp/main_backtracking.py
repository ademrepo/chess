# Runs objective 1 (plain backtracking) in the terminal and prints the tour.
#   python main_backtracking.py

import sys
import time

from backtracking import backtracking
from knight_csp import Knight

sys.setrecursionlimit(10000)


def print_tour(knight):
    # Board where each square shows the number of the move (X0 = 1 ... X63 = 64).
    order = {pos: k + 1 for k, pos in enumerate(knight.assignment)}
    for i in range(8):
        print(" ".join(f"{order[(i, j)]:2d}" for j in range(8)))


if __name__ == "__main__":
    start = time.time()
    result = backtracking(Knight())
    elapsed = time.time() - start
    if result is None:
        print("No tour found.")
    else:
        print(f"Tour found in {elapsed:.2f} s ({len(result.assignment)} squares):")
        print_tour(result)
