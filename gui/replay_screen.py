# Replay screen ("Watch ... (cat)"): the algorithm (genetic algorithm or CSP backtracking) runs
# in a job thread, then the piece replays the tour it found. Same board, same side panel and
# same buttons as the other screens; the cards say what the algorithm did and how to read it.

import pygame

from board import NB_SQUARES
from gui import theme
from gui.csp_job import CSPJob
from gui.ga_job import GAJob
from gui.widgets import Button

# --- Animation settings ---
JUMP_SECONDS = 0.85                # duration of one jump at speed x1
SPEEDS = (0.5, 1, 2, 4)
START_SPEED = 1                    # index in SPEEDS
RUNS_SHOWN = 8

START_BLUE = (70, 140, 255)
CURRENT_YELLOW = (255, 215, 40)


def center(square):
    return (theme.BOARD_X + square[0] * theme.SQUARE + theme.SQUARE // 2,
            theme.BOARD_Y + square[1] * theme.SQUARE + theme.SQUARE // 2)


def cell(square):
    return pygame.Rect(theme.BOARD_X + square[0] * theme.SQUARE, theme.BOARD_Y + square[1] * theme.SQUARE,
                       theme.SQUARE, theme.SQUARE)


class ReplayScreen:
    def __init__(self, app):
        self.app = app
        self.is_csp = app.replay_algo == "csp"          # CSP backtracking or genetic algorithm
        self.history = app.history_csp if self.is_csp else app.history
        self.speed_i = START_SPEED
        self.job = None
        self.path = []
        self.stats = None              # (generations or moves tried, seconds, squares, average fitness, found)
        self.progress = 0.0            # number of jumps already done (fractional)
        self.playing = False
        self.last_tick = pygame.time.get_ticks()
        self._build_buttons()
        self.start_run()

    def _build_buttons(self):
        x, w = theme.PANEL_X, theme.PANEL_W
        half = (w - 10) // 2
        self.play_btn = Button((x, 534, w, 44), "Play", self.toggle_play, theme.BTN_PRIMARY, 19)
        self.speed_btn = Button((x, 588, half, 38), "", self.cycle_speed, size=16)
        self.again_btn = Button((x + half + 10, 588, half, 38), "New run (R)", self.start_run, size=16)
        self.menu_btn = Button((x, 636, w, 38), "Menu (Esc)", self.go_menu, size=16)
        self.buttons = [self.play_btn, self.speed_btn, self.again_btn, self.menu_btn]

    # ------------------------------------------------------------------ run management
    def start_run(self):
        if self.job is not None:
            self.job.cancel()
        self.playing = False
        self.path, self.stats, self.progress = [], None, 0.0
        self.job = CSPJob() if self.is_csp else GAJob(*self.app.job_settings())
        self.job.start()

    def finish_run(self):
        path, count, found = self.job.result
        self.path = path
        self.stats = (count, self.job.duration, len(path), self.job.average_fitness, found)
        self.history.append((count, self.job.duration))
        self.job = None
        self.progress = 0.0
        self.playing = len(path) > 1

    def jumps(self):
        return max(len(self.path) - 1, 0)

    def toggle_play(self):
        if self.job is not None or self.jumps() == 0:
            return
        self.playing = not self.playing
        if self.playing and self.progress >= self.jumps():
            self.progress = 0.0        # replay from the start

    def cycle_speed(self):
        self.speed_i = (self.speed_i + 1) % len(SPEEDS)

    def go_menu(self):
        if self.job is not None:
            self.job.cancel()
        self.app.goto("home")

    # ------------------------------------------------------------------ events and update
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.go_menu()
            elif event.key == pygame.K_SPACE:
                self.toggle_play()
            elif event.key == pygame.K_r:
                self.start_run()
            elif event.key == pygame.K_UP:
                self.speed_i = min(self.speed_i + 1, len(SPEEDS) - 1)
            elif event.key == pygame.K_DOWN:
                self.speed_i = max(self.speed_i - 1, 0)
            return
        for button in self.buttons:
            if button.handle_event(event):
                return

    def update(self):
        now = pygame.time.get_ticks()
        dt = min((now - self.last_tick) / 1000, 0.1)
        self.last_tick = now
        if self.job is not None and self.job.done:
            self.finish_run()
        if self.job is None and self.playing:
            self.progress = min(self.progress + dt * SPEEDS[self.speed_i] / JUMP_SECONDS, self.jumps())
            self.playing = self.progress < self.jumps()      # finished: the button becomes "Replay"
        ready = self.job is None and self.jumps() > 0
        finished = ready and self.progress >= self.jumps()
        self.play_btn.label = "Pause (Space)" if self.playing else ("Replay (Space)" if finished else "Play (Space)")
        self.play_btn.enabled = ready
        self.speed_btn.label = "Speed: x%s" % SPEEDS[self.speed_i]

    # ------------------------------------------------------------------ drawing
    def draw(self, surface):
        surface.fill(theme.BG)
        mouse = pygame.mouse.get_pos()
        self._draw_board(surface)
        self._draw_panel(surface, mouse)

    def _draw_board(self, surface):
        sq = theme.SQUARE
        done = int(self.progress)                      # squares already reached: path[0..done]
        visited = set(self.path[:done + 1])
        theme.draw_board_frame(surface, pygame.Rect(theme.BOARD_X, theme.BOARD_Y, theme.BOARD_PIXELS,
                                                    theme.BOARD_PIXELS), 16)
        for y in range(8):
            for x in range(8):
                dark = (x + y) % 2 == 1
                rect = cell((x, y))
                theme.draw_square(surface, rect, dark, (x, y) in visited)
                label = theme.COORD_DARK if dark and (x, y) not in visited else theme.COORD_LIGHT
                if x == 0:                                   # ranks 8..1, top-left corner
                    theme.draw_text(surface, str(8 - y), 14, label, (rect.x + 4, rect.y + 3), bold=True)
                if y == 7:                                   # files a..h, bottom-right corner
                    theme.draw_text(surface, "abcdefgh"[x], 14, label, (rect.right - 4, rect.bottom - 3),
                                    bold=True, anchor="bottomright")
        if self.job is not None:
            veil = pygame.Surface((sq * 8, sq * 8), pygame.SRCALPHA)
            veil.fill((0, 0, 0, 150))
            surface.blit(veil, (theme.BOARD_X, theme.BOARD_Y))
            what = "moves tried" if self.is_csp else "generations"
            theme.draw_text(surface, "Computing...  %d %s" % (self.job.generation, what), 26, theme.TEXT,
                            (theme.BOARD_X + sq * 4, theme.BOARD_Y + sq * 4), bold=True, anchor="center")
            return
        if len(self.path) < 2:
            return
        points = [center(p) for p in self.path[:done + 1]]
        jump = min(done, len(self.path) - 2)
        t = min(self.progress - jump, 1)
        (x1, y1), (x2, y2) = center(self.path[jump]), center(self.path[jump + 1])
        here = (x1 + (x2 - x1) * t, y1 + (y2 - y1) * t) if self.progress < self.jumps() else center(self.path[-1])
        if len(points) > 1 or self.progress > done:
            lines = pygame.Surface((theme.WIDTH, theme.HEIGHT), pygame.SRCALPHA)
            pygame.draw.lines(lines, theme.ARROW, False, points + [here], 4)
            surface.blit(lines, (0, 0))
        for number, square in enumerate(self.path[:done]):       # the square under the cat is hidden
            theme.draw_text(surface, str(number + 1), 16, theme.NUMBER, center(square), bold=True,
                            anchor="center")
        pygame.draw.rect(surface, START_BLUE, cell(self.path[0]).inflate(-4, -4), 4, border_radius=6)
        pygame.draw.rect(surface, CURRENT_YELLOW, cell(self.path[min(done, len(self.path) - 1)]).inflate(-4, -4),
                         4, border_radius=6)
        moving = self.progress < self.jumps()
        facing = (x2 - x1, y2 - y1)
        # forward: the piece is seen in profile; at rest (end of the tour): the cat looks at us
        theme.draw_piece(surface, here, sq, facing, t if moving else None, None if moving else "front")

    def _draw_panel(self, surface, mouse):
        x, w = theme.PANEL_X, theme.PANEL_W
        theme.draw_side_panel(surface, (x - 16, 16, w + 32, 698))
        title = "Backtracking replay" if self.is_csp else "Genetic algorithm replay"
        theme.draw_text(surface, title, 24, theme.TEXT, (x, 50), bold=True)

        # 1. where the cat is in the tour
        theme.draw_card(surface, (x, 92, w, 96))
        reached = min(int(self.progress) + 1, len(self.path)) if self.path else 0
        theme.draw_text(surface, "Squares visited by the cat", 14, theme.MUTED, (x + 16, 102))
        theme.draw_text(surface, "%d / %d" % (reached, NB_SQUARES), 36, theme.TEXT, (x + 16, 128), bold=True)

        # 2. what the algorithm did
        theme.draw_card(surface, (x, 200, w, 130))
        theme.draw_text(surface, "What the algorithm did", 14, theme.MUTED, (x + 16, 210))
        if self.stats is None:
            theme.draw_text(surface, "Computing...", 20, theme.GOLD, (x + 16, 250), bold=True)
        else:
            count, seconds, squares, _average, found = self.stats
            names = ("Moves tried" if self.is_csp else "Generations", "Time", "Squares")
            values = (str(count), "%.2f s" % seconds, str(squares))
            for i, (name, value) in enumerate(zip(names, values)):
                cx = x + 16 + i * (w - 16) // 3
                theme.draw_text(surface, name, 13, theme.MUTED, (cx, 242))
                theme.draw_text(surface, value, 24, theme.GOLD if found else theme.TEXT, (cx, 262), bold=True)
            theme.draw_text(surface, "Tour found!" if found else "No full tour found", 15,
                            theme.TEXT, (x + 16, 298), bold=True)

        # 3. history
        theme.draw_card(surface, (x, 342, w, 180))
        theme.draw_text(surface, "Runs watched", 14, theme.MUTED, (x + 16, 352))
        unit = "moves" if self.is_csp else "generations"
        first = max(0, len(self.history) - RUNS_SHOWN)
        for line, (count, secs) in enumerate(self.history[first:]):
            number = first + line + 1
            color = theme.GOLD if number == len(self.history) else theme.TEXT
            theme.draw_text(surface, "Run %d: %d %s, %.2f s" % (number, count, unit, secs), 14, color,
                            (x + 16, 378 + line * 17))

        for button in self.buttons:
            button.draw(surface, mouse)
