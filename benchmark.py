# Runs the genetic algorithm many times and prints the median / mean / max number of generations.
# Usage: python benchmark.py [runs] [mutation_probability]     (default: 50 runs, 0.01)

import random
import statistics
import sys
import time

from genetic_algorithm import run_genetic_algorithm

runs = int(sys.argv[1]) if len(sys.argv) > 1 else 50
mutation = float(sys.argv[2]) if len(sys.argv) > 2 else 0.01
generations, seconds = [], []
for seed in range(runs):
    random.seed(seed)
    start = time.perf_counter()
    _, g, found = run_genetic_algorithm(50, mutation)
    seconds.append(time.perf_counter() - start)
    generations.append(g)
print("mutation %.3f, %d runs" % (mutation, runs))
print("generations: median %d, mean %d, max %d" % (
    statistics.median(generations), statistics.mean(generations), max(generations)))
print("time: median %.2f s, max %.2f s" % (statistics.median(seconds), max(seconds)))
