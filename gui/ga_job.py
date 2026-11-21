# Runs the genetic algorithm in a background thread so the window never freezes.

import threading

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

    def cancel(self):
        self.stop_event.set()

    def run(self):
        best, generations, found = run_genetic_algorithm(
            self.population_size, self.mutation_probability, self.max_generations,
            should_stop=self.stop_event.is_set)
        self.result = (best.path[:best.fitness], generations, found)
        self.done = True
