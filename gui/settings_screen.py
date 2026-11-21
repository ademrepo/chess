# Settings screen: the parameters of the genetic algorithm. They are shared by the lab, the cat
# replay and the "Solve with Genetic Algorithm" button (App.settings).

import pygame

from gui import theme
from gui.game_screen import DEFAULT_SETTINGS
from gui.widgets import Button

# key, title, allowed values, format, explanation
PARAMETERS = [
    ("population", "Population size", [10, 20, 30, 50, 75, 100, 150, 200], "%d",
     "Knights per generation. More knights = more diversity, but each generation costs more."),
    ("mutation", "Mutation probability", [0.001, 0.005, 0.01, 0.02, 0.05, 0.1], "%g",
     "Chance that each of the 63 genes becomes a random move. Too low: stagnation. Too high: random search."),
    ("tournament", "Tournament size", [2, 3, 4, 5, 7, 10], "%d",
     "Knights drawn at random; the 2 fittest become the parents. Bigger = stronger selection pressure."),
    ("max_generations", "Generation limit", [500, 1000, 5000, 10000, 50000], "%d",
     "Safety stop of the interface (the statement's loop runs until fitness 64)."),
]
FIXED = ("Fixed by the statement: 63 genes (moves 1 to 8), single-point crossover, "
         "fitness = number of valid squares (max 64).")
ROW_Y, ROW_H = 130, 100


class SettingsScreen:
    def __init__(self, app):
        self.app = app
        cx = theme.WIDTH // 2
        self.buttons = []
        self.steppers = []
        for row, (key, *_rest) in enumerate(PARAMETERS):
            y = ROW_Y + row * ROW_H
            minus = Button((cx + 110, y + 4, 46, 46), "-", lambda k=key: self.step(k, -1), size=26)
            plus = Button((cx + 290, y + 4, 46, 46), "+", lambda k=key: self.step(k, 1), size=26)
            self.steppers += [minus, plus]
        self.buttons = self.steppers + [
            Button((cx - 350, 560, 220, 52), "Defaults", self.defaults, size=20),
            Button((cx - 110, 560, 220, 52), "Back", lambda: app.goto("home"), size=20),
            Button((cx + 130, 560, 220, 52), "Open the lab", lambda: app.goto("lab"),
                   theme.BTN_PRIMARY, 20),
        ]

    def step(self, key, delta):
        values = next(p[2] for p in PARAMETERS if p[0] == key)
        index = values.index(self.app.settings[key])
        self.app.settings[key] = values[max(0, min(len(values) - 1, index + delta))]

    def defaults(self):
        self.app.settings.update(DEFAULT_SETTINGS)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.goto("home")
            return
        for button in self.buttons:
            if button.handle_event(event):
                return

    def update(self):
        for i, (key, _title, values, _fmt, _help) in enumerate(PARAMETERS):
            value = self.app.settings[key]
            self.steppers[2 * i].enabled = value != values[0]
            self.steppers[2 * i + 1].enabled = value != values[-1]

    def draw(self, surface):
        surface.fill(theme.BG)
        mouse = pygame.mouse.get_pos()
        cx = theme.WIDTH // 2
        theme.draw_text(surface, "Settings", 44, theme.TEXT, (cx, 40), bold=True, anchor="midtop")
        theme.draw_text(surface, "Parameters of the genetic algorithm", 18, theme.MUTED,
                        (cx, 94), anchor="midtop")
        for row, (key, title, _values, fmt, help_text) in enumerate(PARAMETERS):
            y = ROW_Y + row * ROW_H
            pygame.draw.rect(surface, theme.CARD, (cx - 400, y - 8, 800, ROW_H - 12), border_radius=8)
            theme.draw_text(surface, title, 24, theme.TEXT, (cx - 380, y + 6), bold=True)
            theme.draw_text(surface, fmt % self.app.settings[key], 30, theme.GOLD,
                            (cx + 233, y + 27), bold=True, anchor="center")
            theme.draw_text(surface, help_text, 15, theme.MUTED, (cx - 380, y + 52))
        theme.draw_text(surface, FIXED, 15, theme.MUTED, (cx, 520), anchor="midtop")
        for button in self.buttons:
            button.draw(surface, mouse)
