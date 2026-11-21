# Game screen: the board, ONE knight played by the human, and a side panel with the button
# that lets the genetic algorithm solve the tour.

from collections import deque

import pygame

from board import NB_SQUARES, square_name
from game import KnightGame
from gui import theme
from gui.assets_loader import knight_image
from gui.ga_job import GAJob
from gui.widgets import Button

POPULATION_SIZE = 50             # value of the statement's main()
MUTATION_PROBABILITY = 0.01
MAX_GENERATIONS = 10000          # safety limit for the interface (the statement loops forever)
SPEEDS = [1, 2, 4, 8]
MOVE_MS = 450                    # duration of one knight move in the replay at speed 1x


def square_center(pos):
    return (theme.BOARD_X + pos[0] * theme.SQUARE + theme.SQUARE // 2,
            theme.BOARD_Y + pos[1] * theme.SQUARE + theme.SQUARE // 2)


class GameScreen:
    def __init__(self, app):
        self.app = app
        self.game = KnightGame()
        self.job = None                  # running GAJob, or None
        self.queue = deque()             # squares still to replay after the GA finished
        self.anim = None                 # (from, to, start_ms, duration_ms)
        self.anim_is_replay = False
        self.last_run = None             # (found, generations, fitness)
        self.speed_i = 0
        self.show_path = True
        self.message = ""
        self._build_buttons()

    def _build_buttons(self):
        x, w = theme.PANEL_X, theme.PANEL_W
        half = (w - 10) // 2
        self.undo_btn = Button((x, 222, half, 44), "Undo", self.undo)
        self.reset_btn = Button((x + half + 10, 222, half, 44), "New game", self.reset)
        self.ga_btn = Button((x, 284, w, 56), "Solve with Genetic Algorithm", self.toggle_ga,
                             theme.BTN_PRIMARY, 19)
        self.speed_btn = Button((x + w - 120, 360, 120, 34), "1x", self.cycle_speed, size=16)
        self.path_btn = Button((x, 420, half, 40), "Path: on", self.toggle_path, size=16)
        self.menu_btn = Button((x + half + 10, 420, half, 40), "Menu", self.go_menu, size=16)
        self.ov_buttons = [Button((0, 0, 170, 46), "", lambda: None, theme.BTN_PRIMARY),
                           Button((0, 0, 170, 46), "", lambda: None)]
        self.buttons = [self.undo_btn, self.reset_btn, self.ga_btn, self.speed_btn,
                        self.path_btn, self.menu_btn]

    # ------------------------------------------------------------------ state
    @property
    def running(self):
        return self.job is not None

    @property
    def replaying(self):
        return bool(self.queue) or (self.anim is not None and self.anim_is_replay)

    @property
    def busy(self):
        return self.running or self.replaying

    def overlay_kind(self):
        if self.busy or self.anim is not None:
            return None
        if self.game.is_complete():
            return "complete"
        if self.game.is_stuck():
            return "stuck"
        return None

    # ------------------------------------------------------------------ actions
    def start_anim(self, source, target, replay=False):
        duration = MOVE_MS / SPEEDS[self.speed_i] if replay else 140
        self.anim = (source, target, pygame.time.get_ticks(), duration)
        self.anim_is_replay = replay

    def undo(self):
        if not self.busy and self.game.undo():
            self.anim = None

    def reset(self):
        if self.running:
            self.job.cancel()
            self.job = None
        self.queue.clear()
        self.anim = None
        self.game.reset()
        self.last_run = None
        self.message = ""

    def toggle_ga(self):
        if self.running:
            self.job.cancel()
            return
        if self.busy:
            return
        self.game.reset()
        self.anim = None
        self.last_run = None
        self.job = GAJob(POPULATION_SIZE, MUTATION_PROBABILITY, MAX_GENERATIONS)
        self.job.start()
        self.message = "Solving..."

    def cycle_speed(self):
        self.speed_i = (self.speed_i + 1) % len(SPEEDS)

    def toggle_path(self):
        self.show_path = not self.show_path

    def go_menu(self):
        if self.running:
            self.job.cancel()
        self.app.goto("home")

    def square_at(self, pos):
        x = (pos[0] - theme.BOARD_X) // theme.SQUARE
        y = (pos[1] - theme.BOARD_Y) // theme.SQUARE
        if pos[0] >= theme.BOARD_X and pos[1] >= theme.BOARD_Y and 0 <= x < 8 and 0 <= y < 8:
            return (x, y)
        return None

    # ------------------------------------------------------------------ events
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.go_menu()
            elif event.key == pygame.K_z:
                self.undo()
            elif event.key == pygame.K_r:
                self.reset()
            elif event.key == pygame.K_g:
                self.toggle_ga()
            return

        if self.overlay_kind():
            for button in self.ov_buttons:
                if button.handle_event(event):
                    return
        for button in self.buttons:
            if button.handle_event(event):
                return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            square = self.square_at(event.pos)
            if square and not self.busy and self.anim is None:
                source = self.game.position
                if self.game.move_to(square):
                    self.start_anim(source, square)

    # ------------------------------------------------------------------ update
    def update(self):
        now = pygame.time.get_ticks()

        if self.running and self.job.done:
            path, generations, found = self.job.result
            self.last_run = (found, generations, len(path))
            self.job = None
            self.message = ""
            self.game.reset()
            self.queue = deque(path[1:])

        if self.anim and now - self.anim[2] >= self.anim[3]:
            self.anim = None
        if self.anim is None and self.queue:
            target = self.queue.popleft()
            source = self.game.position
            if self.game.move_to(target):
                self.start_anim(source, target, replay=True)
            else:
                self.queue.clear()

        busy = self.busy
        self.undo_btn.enabled = not busy and self.game.visited_count > 1
        self.ga_btn.label = "Cancel" if self.running else "Solve with Genetic Algorithm"
        self.ga_btn.style = theme.BTN_DANGER if self.running else theme.BTN_PRIMARY
        self.ga_btn.enabled = not self.replaying
        self.speed_btn.label = "%dx" % SPEEDS[self.speed_i]
        self.path_btn.label = "Path: on" if self.show_path else "Path: off"

    # ------------------------------------------------------------------ drawing
    def draw(self, surface):
        surface.fill(theme.BG)
        mouse = pygame.mouse.get_pos()
        kind = self.overlay_kind()
        self._draw_board(surface, self.game.path, mouse, kind)
        self._draw_panel(surface, self.game.path, mouse)
        if kind:
            self._draw_overlay(surface, kind, mouse)

    def _draw_board(self, surface, path, mouse, kind):
        visited = set(path)
        sq = theme.SQUARE
        hover = self.square_at(mouse)
        legal = {}
        if not self.busy and self.anim is None and not kind:
            legal = {target for _, target in self.game.legal_squares()}

        for y in range(8):
            for x in range(8):
                dark = (x + y) % 2 == 1
                if (x, y) in visited:
                    color = theme.VISITED_DARK if dark else theme.VISITED_LIGHT
                else:
                    color = theme.DARK if dark else theme.LIGHT
                rect = pygame.Rect(theme.BOARD_X + x * sq, theme.BOARD_Y + y * sq, sq, sq)
                pygame.draw.rect(surface, color, rect)
                label_color = theme.LIGHT if dark and (x, y) not in visited else (96, 120, 60)
                if x == 0:                                   # ranks 8..1, top-left corner
                    theme.draw_text(surface, str(8 - y), 14, label_color,
                                    (rect.x + 4, rect.y + 3), bold=True)
                if y == 7:                                   # files a..h, bottom-right corner
                    theme.draw_text(surface, "abcdefgh"[x], 14, label_color,
                                    (rect.right - 4, rect.bottom - 3), bold=True,
                                    anchor="bottomright")

        if self.show_path and len(path) > 1:
            lines = pygame.Surface((theme.WIDTH, theme.HEIGHT), pygame.SRCALPHA)
            pygame.draw.lines(lines, theme.ARROW, False, [square_center(p) for p in path], 4)
            surface.blit(lines, (0, 0))

        for index, pos in enumerate(path):
            if pos != path[-1]:
                theme.draw_text(surface, str(index + 1), 16, (96, 120, 60),
                                square_center(pos), bold=True, anchor="center")

        dots = pygame.Surface((sq, sq), pygame.SRCALPHA)
        pygame.draw.circle(dots, (0, 0, 0, 55), (sq // 2, sq // 2), 12)
        for target in legal:
            surface.blit(dots, (theme.BOARD_X + target[0] * sq, theme.BOARD_Y + target[1] * sq))
        if hover in legal:
            pygame.draw.rect(surface, (255, 255, 255),
                             (theme.BOARD_X + hover[0] * sq, theme.BOARD_Y + hover[1] * sq, sq, sq),
                             4)

        if self.anim:
            source, target, start, duration = self.anim
            t = min(1.0, (pygame.time.get_ticks() - start) / duration)
            t = 1 - (1 - t) ** 3
            sx, sy = square_center(source)
            tx, ty = square_center(target)
            centre = (sx + (tx - sx) * t, sy + (ty - sy) * t)
        else:
            centre = square_center(path[-1])
        image = knight_image("w", sq)
        surface.blit(image, image.get_rect(center=centre))

    def _draw_panel(self, surface, path, mouse):
        x, w = theme.PANEL_X, theme.PANEL_W
        theme.draw_text(surface, "Knight's Tour", 28, theme.TEXT, (x, 40), bold=True)

        pygame.draw.rect(surface, theme.CARD, (x, 110, w, 96), border_radius=8)
        theme.draw_text(surface, "Squares visited", 15, theme.MUTED, (x + 16, 120))
        theme.draw_text(surface, "%d / %d" % (len(path), NB_SQUARES), 34, theme.TEXT,
                        (x + 16, 138), bold=True)
        theme.draw_text(surface, square_name(path[-1]), 16, theme.MUTED,
                        (x + w - 16, 152), anchor="topright")
        if self.message:
            theme.draw_text(surface, self.message, 14, theme.MUTED, (x + 16, 182))

        theme.draw_text(surface, "Replay speed", 16, theme.MUTED, (x, 367))
        for button in self.buttons:
            button.draw(surface, mouse)

    def _draw_overlay(self, surface, kind, mouse):
        board = pygame.Rect(theme.BOARD_X, theme.BOARD_Y, theme.BOARD_PIXELS, theme.BOARD_PIXELS)
        dim = pygame.Surface(board.size, pygame.SRCALPHA)
        dim.fill((0, 0, 0, 80))
        surface.blit(dim, board)

        card = pygame.Rect(0, 0, 420, 210)
        card.center = board.center
        pygame.draw.rect(surface, theme.PANEL, card, border_radius=12)
        if kind == "complete":
            title = "Tour complete!"
            sub = "64 / 64 squares"
            if self.last_run and self.last_run[0]:
                sub = "Found in %d generations" % self.last_run[1]
            first = ("New game", self.reset)
            second = ("Menu", self.go_menu)
        else:
            title = "No legal moves left"
            sub = "%d / %d squares" % (self.game.visited_count, NB_SQUARES)
            first = ("New game", self.reset)
            second = ("Undo", self.undo)
        theme.draw_text(surface, title, 32, theme.TEXT, (card.centerx, card.y + 28),
                        bold=True, anchor="midtop")
        theme.draw_text(surface, sub, 18, theme.MUTED, (card.centerx, card.y + 86),
                        anchor="midtop")
        for button, (label, action), dx in zip(self.ov_buttons, (first, second), (-1, 1)):
            button.label, button.on_click = label, action
            button.rect.centerx = card.centerx + dx * 95
            button.rect.y = card.bottom - 76
            button.draw(surface, mouse)
