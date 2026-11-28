# Main menu of the chosen style: "Play" on top, then two columns, the old project (Project 2,
# genetic algorithm) on the left and the new one (Project 3, CSP backtracking) on the right.
# Both styles offer the same features; "Cavalier Jack" also has the cat replays that show the
# result panel of a run.

import math

import pygame

from gui import theme, wood
from gui.widgets import Button

COLUMN_W, COLUMN_GAP = 380, 40

# The cat of the menu walks about: it stays in the middle (looking at us), walks to the right,
# turns round, comes back, stays, then does the same to the left. Each step is
# (seconds, start x, end x, direction): direction 0 = standing still, 1 = to the right, -1 = left.
RANGE = 320
PATROL = [(2.2, 0, 0, 0), (2.8, 0, RANGE, 1), (2.8, RANGE, 0, -1),
          (2.2, 0, 0, 0), (2.8, 0, -RANGE, -1), (2.8, -RANGE, 0, 1)]
STEPS_PER_SECOND = 3                          # bounces of the walk
BOUNCE_PX = 5
BUTTON_H, BUTTON_GAP = 46, 12
HEADER_H = 58


class HomeScreen:
    def __init__(self, app):
        self.app = app
        jack = theme.is_jack()
        cx = theme.WIDTH // 2
        self.left_x = cx - COLUMN_GAP // 2 - COLUMN_W
        self.right_x = cx + COLUMN_GAP // 2
        width = 2 * COLUMN_W + COLUMN_GAP
        row_y = 266 + 56 + 12                       # the row of 3 buttons, just under "Play"
        self.headers_y = row_y + 44 + 22
        first_y = self.headers_y + HEADER_H + 16

        left = [("Algorithm lab (step by step)", lambda: app.goto("lab"), theme.BTN_PRIMARY)]
        right = [("CSP backtracking (step by step)", lambda: app.goto("csp"), theme.BTN_PRIMARY)]
        if jack:
            left.append(("Watch the algorithm (cat)", lambda: self.watch("ga"), theme.BTN_SECONDARY))
            right.append(("Watch the backtracking (cat)", lambda: self.watch("csp"), theme.BTN_SECONDARY))

        self.buttons = [Button((self.left_x, 266, width, 56), "Play",
                               lambda: app.goto("game"), theme.BTN_PRIMARY, 28)]
        small = (width - 2 * 16) // 3
        for i, (label, action) in enumerate((("Settings", lambda: app.goto("settings")),
                                             ("Change style", lambda: app.goto("style")),
                                             ("Quit", app.quit))):
            self.buttons.append(Button((self.left_x + i * (small + 16), row_y, small, 44), label,
                                       action, theme.BTN_SECONDARY, 20))
        for x, entries in ((self.left_x, left), (self.right_x, right)):
            for i, (label, action, style) in enumerate(entries):
                self.buttons.append(Button((x, first_y + i * (BUTTON_H + BUTTON_GAP), COLUMN_W, BUTTON_H),
                                           label, action, style, 20))

    def watch(self, algo):
        # The cat replay shows the tour of the chosen algorithm: "ga" or "csp".
        self.app.replay_algo = algo
        self.app.goto("replay")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.app.goto("game")
            elif event.key == pygame.K_ESCAPE:
                self.app.goto("style")
        for button in self.buttons:
            if button.handle_event(event):
                return

    def update(self):
        pass

    @staticmethod
    def patrol(seconds):
        # Where the cat is `seconds` after the start: (x offset, direction, bounce in pixels).
        t = seconds % sum(step[0] for step in PATROL)
        for duration, x0, x1, direction in PATROL:
            if t < duration:
                u = t / duration
                u = u * u * (3 - 2 * u)                       # gentle start and stop
                bounce = BOUNCE_PX * abs(math.sin(math.pi * STEPS_PER_SECOND * seconds)) if direction else 0
                return x0 + (x1 - x0) * u, direction, round(bounce)
            t -= duration
        return 0, 0, 0

    def _header(self, surface, x, title, subtitle):
        rect = pygame.Rect(x, self.headers_y, COLUMN_W, HEADER_H)
        if theme.is_jack():
            surface.blit(wood.ribbon(rect.w, rect.h), rect)
            title_color = theme.TEXT
        else:
            pygame.draw.rect(surface, theme.CARD, rect, border_radius=8)
            title_color = theme.TEXT
        theme.draw_text(surface, title, 20, title_color, (rect.centerx, rect.y + 7), bold=True,
                        anchor="midtop")
        theme.draw_text(surface, subtitle, 13, theme.GOLD if not theme.is_jack() else (255, 226, 160),
                        (rect.centerx, rect.y + 30), anchor="midtop")

    def draw(self, surface):
        surface.fill(theme.BG)
        mouse = pygame.mouse.get_pos()
        cx = theme.WIDTH // 2
        if theme.is_jack():
            offset, direction, bounce = self.patrol(pygame.time.get_ticks() / 1000)
            theme.draw_piece(surface, (cx + offset, 96), 128, (direction, 0) if direction else None,
                             None, None if direction else "front", bounce)
        else:
            theme.draw_piece(surface, (cx, 96), 128)
        theme.draw_text(surface, "Knight's Tour Game", 54, theme.TEXT, (cx, 164), bold=True,
                        anchor="midtop")
        theme.draw_text(surface, theme.STYLES[theme.STYLE], 20, theme.GOLD, (cx, 234), bold=True,
                        anchor="midtop")
        self._header(surface, self.left_x, "Project 2", "Genetic algorithm")
        self._header(surface, self.right_x, "Project 3", "CSP backtracking")
        for button in self.buttons:
            button.draw(surface, mouse)
