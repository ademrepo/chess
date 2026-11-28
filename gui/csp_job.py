# Runs the CSP backtracking (csp/backtracking.py, the statement's pseudo-code) in a background
# thread, with the same interface as GAJob so the screens can use either of them.

import os
import sys
import threading
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "csp"))
sys.setrecursionlimit(max(sys.getrecursionlimit(), 2000))

from backtracking import backtracking      # noqa: E402  (csp/backtracking.py)
from knight_csp import Knight              # noqa: E402  (csp/knight_csp.py)


class Cancelled(Exception):
    pass


class WatchedKnight(Knight):
    # Same knight, but it reports its progress and can be stopped; backtracking() itself is
    # not modified.
    def __init__(self, job):
        super().__init__()
        self.job = job

    def addMove(self, move):
        if self.job.stop_event.is_set():
            raise Cancelled()
        super().addMove(move)
        self.job.generation = self.nodes
        if self.job.events is not None:
            self.job.events.append((True, move))

    def removeMove(self):
        move = self.assignment[-1]
        super().removeMove()
        if self.job.events is not None:
            self.job.events.append((False, move))


class CSPJob(threading.Thread):
    def __init__(self, record=False):
        super().__init__(daemon=True)
        # record=True keeps every addMove / removeMove of the search, (True, square) or
        # (False, square), in (row, column): the "CSP search" screen plays them back.
        self.events = [] if record else None
        self.stop_event = threading.Event()
        self.done = False
        self.result = None             # (path, moves tried, found), path in (x, y) = (column, row)
        self.duration = 0.0            # seconds
        self.average_fitness = 0.0     # not used by backtracking
        self.generation = 0            # progress: moves tried so far

    def cancel(self):
        self.stop_event.set()

    def run(self):
        start = time.perf_counter()
        knight = WatchedKnight(self)
        try:
            found = backtracking(knight) is not None
        except Cancelled:
            found = False
        self.duration = time.perf_counter() - start
        # csp/ uses (row, column), the interface uses (x, y) = (column, row)
        path = [(j, i) for i, j in knight.assignment]
        self.result = (path, knight.nodes, found)
        self.done = True
