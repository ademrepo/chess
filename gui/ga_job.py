# Runs the genetic algorithm in a background thread so the window never freezes.

import threading
import time

from genetic_algorithm import run_genetic_algorithm


class GAJob(threading.Thread):
    def __init__(self, population_size, mutation_probability, max_generations):
        super().__init__(daemon=True)
        self.population_size = population_size
        self.mutation_probability = mutation_probability
        self.max_generations = max_generations
        self.stop_event = threading.Event()
        self.done = False
        self.result = None             # (valid path, generations, found)
        self.duration = 0.0            # seconds
        self.average_fitness = 0.0     # average fitness of the last generation
        self.generation = 0            # progress, read by the interface

    def cancel(self):
        self.stop_event.set()

    def _on_generation(self, generation, best, average):
        self.generation = generation
        self.average_fitness = average

    def run(self):
        start = time.perf_counter()
        best, generations, found = run_genetic_algorithm(
            self.population_size, self.mutation_probability, self.max_generations,
            on_generation=self._on_generation, should_stop=self.stop_event.is_set)
        self.duration = time.perf_counter() - start
        self.result = (best.path[:best.fitness], generations, found)
        self.done = True
