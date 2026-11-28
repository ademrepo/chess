# Algorithm lab: runs the genetic algorithm one generation at a time and shows every calculation
# (repair, fitness, tournament, crossover, mutation) so the algorithm can be explained live.
# It uses the real Population / Knight / Chromosome classes; nothing is simulated.

import random
import time

import pygame

from board import NB_GENES, NB_SQUARES, on_board, square_name
from gui import theme
from gui.widgets import Button
from population import Population

SIZE = (1280, 760)
SQ = 72
BOARD_X, BOARD_Y = 30, 70
RIGHT_X, RIGHT_W = 650, 600
SPEEDS = [("1 gen/s", 1), ("5 gen/s", 5), ("30 gen/s", 30), ("max", None)]
MAX_SPEED_BUDGET = 0.012           # seconds of calculation per frame at "max" speed
CHART_POINTS = 560
STRIP_X, STRIP_W = RIGHT_X + 120, 470

BEST_COLOR, AVERAGE_COLOR, CUT_COLOR, MUTATION_COLOR = (129, 182, 76), (255, 200, 60), (255, 255, 255), (230, 70, 60)
# One colour per move (1..8) to read the chromosomes at a glance.
GENE_COLORS = [(230, 90, 80), (240, 150, 60), (240, 210, 70), (140, 200, 80),
               (70, 190, 170), (80, 150, 230), (140, 110, 220), (210, 100, 190)]
DIRECTIONS = ["up-right", "right-up", "right-down", "down-right",
              "down-left", "left-down", "left-up", "up-left"]


class LabScreen:
    SIZE = SIZE

    def __init__(self, app):
        self.app = app
        self.speed_i = 1
        self.auto = False
        self.accumulator = 0.0
        self.last_tick = pygame.time.get_ticks()
        self.limit = app.settings["max_generations"]
        self._build_buttons()
        self.new_run()

    def _build_buttons(self):
        y, h = 684, 50
        self.step_btn = Button((BOARD_X, y, 150, h), "Step (Space)", self.step, theme.BTN_PRIMARY, 18)
        self.auto_btn = Button((BOARD_X + 160, y, 130, h), "Auto (A)", self.toggle_auto, size=18)
        self.speed_btn = Button((BOARD_X + 300, y, 110, h), "", self.cycle_speed, size=17)
        self.new_btn = Button((BOARD_X + 420, y, 90, h), "New (R)", self.new_run, size=17)
        self.menu_btn = Button((BOARD_X + 520, y, 100, h), "Menu", lambda: self.app.goto("home"), size=17)
        self.buttons = [self.step_btn, self.auto_btn, self.speed_btn, self.new_btn, self.menu_btn]

    # ------------------------------------------------------------------ algorithm
    def new_run(self):
        s = self.app.settings
        self.population = Population(s["population"], s["mutation"], s["tournament"])
        self.best_history, self.average_history = [], []
        self.best_ever = 0
        self.auto = False
        self.accumulator = 0.0
        self.evaluate()

    def evaluate(self):
        # The loop body of the statement's main(), after the creation of the generation.
        pop = self.population
        pop.check_population()
        self.best_fitness, self.best = pop.evaluate()
        fitnesses = [k.fitness for k in pop.knights]
        self.average = sum(fitnesses) / len(fitnesses)
        self.worst = min(fitnesses)
        self.best_ever = max(self.best_ever, self.best_fitness)
        self.best_history.append(self.best_fitness)
        self.average_history.append(self.average)

    @property
    def found(self):
        return self.best_fitness == NB_SQUARES

    @property
    def finished(self):
        return self.found or self.population.generation >= self.limit

    def step(self):
        if self.finished:
            return
        self.population.create_new_generation()
        self.evaluate()
        if self.finished:
            self.auto = False

    def toggle_auto(self):
        if not self.finished:
            self.auto = not self.auto

    def cycle_speed(self):
        self.speed_i = (self.speed_i + 1) % len(SPEEDS)

    # ------------------------------------------------------------------ events and update
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.goto("home")
            elif event.key == pygame.K_SPACE:
                self.step()
            elif event.key == pygame.K_a:
                self.toggle_auto()
            elif event.key == pygame.K_r:
                self.new_run()
            return
        for button in self.buttons:
            if button.handle_event(event):
                return

    def update(self):
        now = pygame.time.get_ticks()
        dt = min((now - self.last_tick) / 1000, 0.1)
        self.last_tick = now
        if self.auto:
            rate = SPEEDS[self.speed_i][1]
            if rate is None:                       # as many generations as fit in the time budget
                start = time.perf_counter()
                while self.auto and time.perf_counter() - start < MAX_SPEED_BUDGET:
                    self.step()
            else:
                self.accumulator += dt * rate
                while self.accumulator >= 1 and self.auto:
                    self.accumulator -= 1
                    self.step()
        self.step_btn.enabled = not self.finished
        self.auto_btn.enabled = not self.finished
        self.auto_btn.label = "Pause (A)" if self.auto else "Auto (A)"
        self.speed_btn.label = SPEEDS[self.speed_i][0]

    # ------------------------------------------------------------------ drawing
    def draw(self, surface):
        surface.fill(theme.BG)
        mouse = pygame.mouse.get_pos()
        self._draw_board(surface)
        self._draw_stats(surface)
        self._draw_chart(surface)
        self._draw_operations(surface)
        for button in self.buttons:
            button.draw(surface, mouse)

    def _text(self, surface, text, size, color, pos, **kw):
        return theme.draw_text(surface, text, size, color, pos, **kw)

    def _draw_board(self, surface):
        best = self.best
        valid = best.path[:best.fitness]
        self._text(surface, "Algorithm lab", 28, theme.TEXT, (BOARD_X, 2), bold=True)
        self._text(surface, "Best knight of generation %d" % self.population.generation, 17,
                   theme.MUTED, (BOARD_X, 36))
        theme.draw_board_frame(surface, pygame.Rect(BOARD_X, BOARD_Y, 8 * SQ, 8 * SQ), 12)
        for y in range(8):
            for x in range(8):
                rect = pygame.Rect(BOARD_X + x * SQ, BOARD_Y + y * SQ, SQ, SQ)
                theme.draw_square(surface, rect, (x + y) % 2 == 1, (x, y) in valid)
        centers = [(BOARD_X + p[0] * SQ + SQ // 2, BOARD_Y + p[1] * SQ + SQ // 2) for p in valid]
        if len(centers) > 1:
            pygame.draw.lines(surface, theme.LINE, False, centers, 3)
        for number, center in enumerate(centers[:-1], 1):
            self._text(surface, str(number), 15, theme.NUMBER, center, bold=True, anchor="center")
        theme.draw_piece(surface, centers[-1], SQ)

        # Why the path stops: the move number `fitness` is illegal.
        if not self.found:
            nxt = best.path[best.fitness]
            if on_board(nxt):
                reason = "move %d goes back to %s (already visited)" % (best.fitness, square_name(nxt))
                x, y = nxt
                pygame.draw.rect(surface, MUTATION_COLOR,
                                 (BOARD_X + x * SQ + 2, BOARD_Y + y * SQ + 2, SQ - 4, SQ - 4), 4)
            else:
                reason = "move %d leaves the board" % best.fitness
            self._text(surface, "Stops after %d squares: %s" % (best.fitness, reason), 16,
                       theme.MUTED, (BOARD_X, BOARD_Y + 8 * SQ + 14))
        else:
            self._text(surface, "All 64 squares visited exactly once!", 18, BEST_COLOR,
                       (BOARD_X, BOARD_Y + 8 * SQ + 14), bold=True)

    def _card(self, surface, rect):
        theme.draw_card(surface, rect)

    def _draw_stats(self, surface):
        pop = self.population
        rect = pygame.Rect(RIGHT_X, 20, RIGHT_W, 96)
        self._card(surface, rect)
        cells = [("Generation", str(pop.generation)),
                 ("Best fitness", "%d / %d" % (self.best_fitness, NB_SQUARES)),
                 ("Average", "%.1f" % self.average),
                 ("Worst", str(self.worst)),
                 ("Best ever", str(self.best_ever))]
        width = RIGHT_W // len(cells)
        for i, (title, value) in enumerate(cells):
            cx = rect.x + width * i + width // 2
            self._text(surface, title, 14, theme.MUTED, (cx, rect.y + 10), anchor="midtop")
            color = BEST_COLOR if title == "Best fitness" and self.found else theme.TEXT
            self._text(surface, value, 28, color, (cx, rect.y + 30), bold=True, anchor="midtop")
        if self.found:
            note = "Tour found in %d generations" % pop.generation
        elif self.finished:
            note = "Generation limit reached (%d)" % self.limit
        else:
            note = "Parameters: population %d, mutation %g, tournament %d" % (
                pop.population_size, pop.mutation_probability, pop.tournament_size)
        self._text(surface, note, 14, AVERAGE_COLOR if self.finished else theme.MUTED,
                   (rect.centerx, rect.bottom - 26), anchor="midtop")

    def _draw_chart(self, surface):
        rect = pygame.Rect(RIGHT_X, 126, RIGHT_W, 200)
        self._card(surface, rect)
        self._text(surface, "Fitness per generation", 16, theme.TEXT, (rect.x + 16, rect.y + 8), bold=True)
        self._text(surface, "best", 14, BEST_COLOR, (rect.right - 130, rect.y + 10))
        self._text(surface, "average", 14, AVERAGE_COLOR, (rect.right - 80, rect.y + 10))
        plot = pygame.Rect(rect.x + 44, rect.y + 36, rect.w - 64, rect.h - 62)
        for value in (0, 16, 32, 48, 64):
            y = plot.bottom - plot.h * value / NB_SQUARES
            pygame.draw.line(surface, theme.GRID, (plot.x, y), (plot.right, y))
            self._text(surface, str(value), 12, theme.MUTED, (plot.x - 6, y), anchor="midright")
        count = len(self.best_history)
        stride = max(1, count // CHART_POINTS)
        indexes = list(range(0, count, stride))
        if indexes[-1] != count - 1:
            indexes.append(count - 1)
        for series, color in ((self.average_history, AVERAGE_COLOR), (self.best_history, BEST_COLOR)):
            points = [(plot.x + plot.w * i / max(count - 1, 1),
                       plot.bottom - plot.h * series[i] / NB_SQUARES) for i in indexes]
            if len(points) > 1:
                pygame.draw.lines(surface, color, False, points, 2)
            else:
                pygame.draw.circle(surface, color, points[0], 3)
        self._text(surface, "generation 1", 12, theme.MUTED, (plot.x, plot.bottom + 6))
        self._text(surface, "generation %d" % self.population.generation, 12, theme.MUTED,
                   (plot.right, plot.bottom + 6), anchor="topright")

    # ------------------------------------------------------------------ the calculations
    def _strip(self, surface, y, genes, label, cut=None, mutated=(), source=None):
        # 63 coloured cells, one per gene. `source` = (parent1, parent2) tints nothing, it only
        # lets the cells of a child be read against the parents.
        self._text(surface, label, 13, theme.MUTED, (RIGHT_X + 16, y), anchor="topleft")
        cell = STRIP_W / NB_GENES
        for i, gene in enumerate(genes):
            rect = pygame.Rect(round(STRIP_X + i * cell), y, max(round(cell) - 1, 1), 14)
            pygame.draw.rect(surface, GENE_COLORS[gene - 1], rect)
            if i in mutated:
                pygame.draw.rect(surface, MUTATION_COLOR, rect.inflate(2, 6), 2)
        if cut is not None:
            x = round(STRIP_X + cut * cell) - 1
            pygame.draw.line(surface, CUT_COLOR, (x, y - 4), (x, y + 18), 2)

    def _draw_operations(self, surface):
        pop = self.population
        rect = pygame.Rect(RIGHT_X, 336, RIGHT_W, 400)
        self._card(surface, rect)
        x, y = rect.x + 16, rect.y + 10
        trace = pop.trace

        self._text(surface, "How generation %d was calculated" % pop.generation, 16, theme.TEXT,
                   (x, y), bold=True)
        y += 30
        if trace is None:
            self._text(surface, "Generation 1: %d random chromosomes (63 genes between 1 and 8)." %
                       pop.population_size, 14, theme.MUTED, (x, y))
            y += 24
            self._text(surface, "Press Step (Space) to build the next generation.", 14, theme.MUTED, (x, y))
            y += 40
        else:
            sample = trace["sample"]
            # 1. Tournament selection
            self._text(surface, "1. Tournament selection (size %d)" % pop.tournament_size, 15,
                       AVERAGE_COLOR, (x, y), bold=True)
            y += 22
            self._text(surface, "Random sample, fitness: %s  ->  the two best are the parents (%d and %d)"
                       % (", ".join(str(f) for f in sample), sample[0], sample[1]), 14, theme.TEXT, (x, y))
            y += 30

            # 2. Single-point crossover
            self._text(surface, "2. Single-point crossover at gene %d" % trace["cut"], 15, AVERAGE_COLOR,
                       (x, y), bold=True)
            for move in range(8):                                  # legend: colour = move
                lx = rect.right - 16 - (8 - move) * 26
                pygame.draw.rect(surface, GENE_COLORS[move], (lx, y + 2, 22, 14))
                self._text(surface, str(move + 1), 11, (20, 20, 20), (lx + 11, y + 9), anchor="center")
            y += 26
            self._strip(surface, y, trace["parent1"], "parent 1", trace["cut"])
            y += 22
            self._strip(surface, y, trace["parent2"], "parent 2", trace["cut"])
            y += 22
            self._strip(surface, y, trace["child_before_mutation"], "child 1", trace["cut"])
            y += 20
            self._text(surface, "child 1 = genes 1..%d of parent 1 + genes %d..63 of parent 2"
                       % (trace["cut"], trace["cut"] + 1), 13, theme.MUTED, (x, y))
            y += 28

            # 3. Mutation
            self._text(surface, "3. Mutation (probability %g per gene)" % pop.mutation_probability, 15,
                       AVERAGE_COLOR, (x, y), bold=True)
            y += 22
            self._strip(surface, y, trace["child"], "child 1 mutated", None, trace["mutated"])
            y += 22
            self._text(surface, "This child: %d mutated gene(s) (red). Whole generation: %d of %d genes "
                       "(expected about %.0f)." % (len(trace["mutated"]), pop.mutated_genes,
                                                     pop.population_size * NB_GENES,
                                                     pop.population_size * NB_GENES * pop.mutation_probability),
                       13, theme.MUTED, (x, y))
            y += 30

        # 4. Repair, 5. fitness: done for every knight of the generation
        self._text(surface, "4. Repair (check_moves)", 15, AVERAGE_COLOR, (x, y), bold=True)
        y += 22
        self._text(surface, "%d genes of %d were illegal (off the board or square already visited) and replaced"
                   % (pop.repaired_genes, pop.population_size * NB_GENES), 14, theme.TEXT, (x, y))
        y += 20
        self._text(surface, "by the next legal move, cycling through the 8 directions.", 14, theme.TEXT, (x, y))
        y += 30
        self._text(surface, "5. Fitness (evaluate_fitness)", 15, AVERAGE_COLOR, (x, y), bold=True)
        y += 22
        self._text(surface, "Valid squares of each path, from (0, 0): best %d, average %.1f, worst %d."
                   % (self.best_fitness, self.average, self.worst), 14, theme.TEXT, (x, y))
