# CSP search screen: shows the backtracking working, move by move, like the pictures of the
# statement (Figure 2): the knight goes forward, hits a dead end, goes back, tries another move.
# The real backtracking() of csp/backtracking.py runs first (CSPJob records every addMove and
# removeMove), then this screen plays the recording back at a speed you choose, or step by step.

from itertools import accumulate

import pygame

from board import NB_SQUARES, square_name
from gui import theme
from gui.csp_job import CSPJob
from gui.widgets import Button
from knight_csp import Knight          # csp/ is added to sys.path by gui/csp_job.py

# Positions of the csp package are (row, column); the board is drawn with x = column, y = row.
SPEEDS = [2, 10, 50, 250, 1000, 5000]          # moves per second (a move = forward or backward)
START_SPEED = 2
WALK_MAX_SPEED = 10                            # up to this speed the piece walks from square to square
WALK_MS = 420                                  # duration of one step of the piece (cat)
WALK_MS_CLASSIC = 220
BACK_COLOR = (230, 70, 60)
CURRENT_COLOR = (255, 215, 40)


def center(square):
    row, col = square
    return (theme.BOARD_X + col * theme.SQUARE + theme.SQUARE // 2,
            theme.BOARD_Y + row * theme.SQUARE + theme.SQUARE // 2)


def cell(square):
    row, col = square
    return pygame.Rect(theme.BOARD_X + col * theme.SQUARE, theme.BOARD_Y + row * theme.SQUARE,
                       theme.SQUARE, theme.SQUARE)


def name(square):
    return square_name((square[1], square[0]))      # square_name wants (x, y)


def free_moves(assignment):
    # Domain of the next variable, computed by the Knight class of the csp package.
    knight = Knight()
    knight.assignment = list(assignment)
    return knight.possibleMoves()


class CSPScreen:
    def __init__(self, app):
        self.app = app
        self.job = CSPJob(record=True)
        self.job.start()
        self.events = []
        self.pos = 0                       # number of events already played
        self.assignment = [(0, 0)]         # X0..Xk at this point of the search
        self.playing = False
        self.speed_i = START_SPEED
        self.credit = 0.0                  # fractional events to play (speed x time)
        self.last_tick = pygame.time.get_ticks()
        self.found = False
        self.facing = None                 # direction of the last step of the piece, (dx, dy)
        self.walk = None                   # (from, to, start_ms, duration) while the piece walks
        self._build_buttons()

    def _build_buttons(self):
        x, w = theme.PANEL_X, theme.PANEL_W
        half = (w - 10) // 2
        self.play_btn = Button((x, 430, w, 46), "Play", self.toggle_play, theme.BTN_PRIMARY, 20)
        self.back_btn = Button((x, 486, half, 40), "< Step back", lambda: self.step(-1), size=16)
        self.step_btn = Button((x + half + 10, 486, half, 40), "Step >", lambda: self.step(1), size=16)
        self.speed_btn = Button((x, 536, half, 40), "", self.cycle_speed, size=16)
        self.end_btn = Button((x + half + 10, 536, half, 40), "Jump to end", self.jump_to_end, size=16)
        self.restart_btn = Button((x, 586, half, 40), "Restart", self.restart, size=16)
        self.menu_btn = Button((x + half + 10, 586, half, 40), "Menu", self.go_menu, size=16)
        self.buttons = [self.play_btn, self.back_btn, self.step_btn, self.speed_btn, self.end_btn,
                        self.restart_btn, self.menu_btn]

    # ------------------------------------------------------------------ recording
    def _recording_ready(self):
        self.events = self.job.events
        depth = 1
        self.depths = [1]                              # depth after n events
        self.moves_tried = [0]                         # forward moves among the first n events
        for is_add, _ in self.events:
            depth += 1 if is_add else -1
            self.depths.append(depth)
            self.moves_tried.append(self.moves_tried[-1] + is_add)
        self.deepest = list(accumulate(self.depths, max))
        self.found = self.job.result[2]
        self.job = None

    # ------------------------------------------------------------------ playback
    @property
    def ready(self):
        return self.job is None

    def step(self, direction):
        if not self.ready:
            return
        self.playing = False
        self._move(direction, walk=True)

    def _move(self, direction, walk=False):
        # Plays one event forward (+1) or undoes the previous one (-1). The piece looks towards
        # the square it goes to; with walk=True it also walks there instead of jumping.
        before, length = self.assignment[-1], len(self.assignment)
        self._apply(direction)
        now = self.assignment[-1]
        if now != before:
            self.facing = (now[1] - before[1], now[0] - before[0])         # (dx, dy) = (columns, rows)
            if walk:
                self.walk = (before, now, pygame.time.get_ticks(),
                             WALK_MS if theme.is_jack() else WALK_MS_CLASSIC,
                             len(self.assignment) < length)        # True: going back to the previous square

    def _apply(self, direction):
        if direction > 0 and self.pos < len(self.events):
            is_add, square = self.events[self.pos]
            if is_add:
                self.assignment.append(square)
            else:
                self.assignment.pop()
            self.pos += 1
        elif direction < 0 and self.pos > 0:
            self.pos -= 1
            is_add, square = self.events[self.pos]
            if is_add:
                self.assignment.pop()
            else:
                self.assignment.append(square)

    def toggle_play(self):
        if not self.ready:
            return
        if self.pos >= len(self.events):
            self.restart()
        self.playing = not self.playing

    def cycle_speed(self):
        self.speed_i = (self.speed_i + 1) % len(SPEEDS)

    def jump_to_end(self):
        if not self.ready:
            return
        self.playing = False
        self.walk = None
        while self.pos < len(self.events):
            self._move(1)

    def restart(self):
        self.playing = False
        self.pos = 0
        self.assignment = [(0, 0)]
        self.facing, self.walk = None, None

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
            elif event.key == pygame.K_RIGHT:
                self.step(1)
            elif event.key == pygame.K_LEFT:
                self.step(-1)
            elif event.key == pygame.K_r:
                self.restart()
            elif event.key == pygame.K_e:
                self.jump_to_end()
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
            self._recording_ready()
        if self.ready and self.playing:
            self.credit += dt * SPEEDS[self.speed_i]
            while self.credit >= 1 and self.pos < len(self.events):
                self._move(1, walk=SPEEDS[self.speed_i] <= WALK_MAX_SPEED)
                self.credit -= 1
            if self.pos >= len(self.events):
                self.playing = False
                self.credit = 0.0
        finished = self.ready and self.pos >= len(self.events)
        self.play_btn.label = "Pause" if self.playing else ("Replay" if finished else "Play")
        self.play_btn.enabled = self.ready
        self.back_btn.enabled = self.ready and self.pos > 0
        self.step_btn.enabled = self.ready and not finished
        self.end_btn.enabled = self.ready and not finished
        self.restart_btn.enabled = self.ready and self.pos > 0
        self.speed_btn.label = "Speed: %d/s" % SPEEDS[self.speed_i]

    # ------------------------------------------------------------------ drawing
    def draw(self, surface):
        surface.fill(theme.BG)
        mouse = pygame.mouse.get_pos()
        self._draw_board(surface)
        self._draw_panel(surface, mouse)

    def last_event(self):
        return self.events[self.pos - 1] if self.ready and self.pos > 0 else None

    def _draw_board(self, surface):
        sq = theme.SQUARE
        assignment = self.assignment
        visited = set(assignment)
        last = self.last_event()
        theme.draw_board_frame(surface, pygame.Rect(theme.BOARD_X, theme.BOARD_Y,
                                                    theme.BOARD_PIXELS, theme.BOARD_PIXELS), 16)
        for row in range(8):
            for col in range(8):
                dark = (row + col) % 2 == 1
                rect = cell((row, col))
                theme.draw_square(surface, rect, dark, (row, col) in visited)
                label = theme.COORD_DARK if dark and (row, col) not in visited else theme.COORD_LIGHT
                if col == 0:                                   # row numbers 1..8, on the left
                    theme.draw_text(surface, str(row + 1), 14, label, (rect.x + 4, rect.y + 3), bold=True)
                if row == 0:                                   # column numbers 1..8, on top
                    theme.draw_text(surface, str(col + 1), 14, label, (rect.right - 4, rect.y + 3),
                                    bold=True, anchor="topright")

        if len(assignment) > 1:
            lines = pygame.Surface((theme.WIDTH, theme.HEIGHT), pygame.SRCALPHA)
            pygame.draw.lines(lines, theme.ARROW, False, [center(p) for p in assignment], 4)
            surface.blit(lines, (0, 0))
        for index, square in enumerate(assignment[:-1]):
            theme.draw_text(surface, str(index + 1), 16, theme.NUMBER, center(square), bold=True,
                            anchor="center")

        if self.ready:                       # the moves the knight can try next
            dots = pygame.Surface((sq, sq), pygame.SRCALPHA)
            pygame.draw.circle(dots, theme.DOT, (sq // 2, sq // 2), 12)
            for target in free_moves(assignment):
                surface.blit(dots, cell(target))

        if last is not None and not last[0]:               # a backtrack: the square given up
            gone = cell(last[1])
            pygame.draw.rect(surface, BACK_COLOR, gone.inflate(-4, -4), 5, border_radius=6)
            theme.draw_text(surface, "x", 34, BACK_COLOR, gone.center, bold=True, anchor="center")
        pygame.draw.rect(surface, CURRENT_COLOR, cell(assignment[-1]).inflate(-4, -4), 4, border_radius=6)
        centre, phase, view = center(assignment[-1]), None, "front"     # at rest the cat looks at us
        if self.walk:                                      # the piece walks from one square to the next
            a, b, start, duration, going_back = self.walk
            t = (pygame.time.get_ticks() - start) / duration
            if t >= 1:
                self.walk = None
            else:
                t = t * t * (3 - 2 * t)
                (ax, ay), (bx, by) = center(a), center(b)
                centre, phase = (ax + (bx - ax) * t, ay + (by - ay) * t), t
                view = "back" if going_back else None             # going back: we see its back, forward: its profile
        theme.draw_piece(surface, centre, sq, self.facing, phase, view)

        if not self.ready:
            veil = pygame.Surface((sq * 8, sq * 8), pygame.SRCALPHA)
            veil.fill((0, 0, 0, 150))
            surface.blit(veil, (theme.BOARD_X, theme.BOARD_Y))
            theme.draw_text(surface, "Searching...  %d moves tried" % self.job.generation, 26,
                            theme.TEXT, (theme.BOARD_X + sq * 4, theme.BOARD_Y + sq * 4), bold=True,
                            anchor="center")

    def _draw_panel(self, surface, mouse):
        x, w = theme.PANEL_X, theme.PANEL_W
        theme.draw_side_panel(surface, (x - 16, 16, w + 32, 698))
        theme.draw_text(surface, "CSP backtracking", 28, theme.TEXT, (x, 50), bold=True)

        theme.draw_card(surface, (x, 92, w, 92))
        theme.draw_text(surface, "Variables assigned (X0..Xk)", 14, theme.MUTED, (x + 16, 100))
        theme.draw_text(surface, "%d / %d" % (len(self.assignment), NB_SQUARES), 34, theme.TEXT,
                        (x + 16, 118), bold=True)
        theme.draw_text(surface, name(self.assignment[-1]), 16, theme.MUTED, (x + w - 16, 132),
                        anchor="topright")

        theme.draw_card(surface, (x, 194, w, 104))
        if self.ready:
            tried = self.moves_tried[self.pos]
            stats = (("Moves tried", tried), ("Backtracks", self.pos - tried),
                     ("Deepest", self.deepest[self.pos]))
            total = "%d / %d" % (self.pos, len(self.events))
        else:
            stats = (("Moves tried", self.job.generation), ("Backtracks", "-"), ("Deepest", "-"))
            total = "-"
        for i, (title, value) in enumerate(stats):
            cx = x + 16 + i * (w - 16) // 3
            theme.draw_text(surface, title, 13, theme.MUTED, (cx, 204))
            theme.draw_text(surface, str(value), 24, theme.GOLD, (cx, 224), bold=True)
        theme.draw_text(surface, "Step %s" % total, 14, theme.MUTED, (x + 16, 270))

        theme.draw_card(surface, (x, 308, w, 66))
        title, detail = self._status()
        theme.draw_text(surface, title, 18, theme.TEXT, (x + 16, 318), bold=True)
        theme.draw_text(surface, detail, 15, theme.MUTED, (x + 16, 344))
        theme.draw_text(surface, "Dots: moves the knight can try next.", 13, theme.MUTED, (x, 384))
        theme.draw_text(surface, "Red cross: dead end, the knight goes back.", 13, theme.MUTED, (x, 402))

        for button in self.buttons:
            button.draw(surface, mouse)
        theme.draw_text(surface, "Space: play   Left/Right: step   Up/Down: speed", 13, theme.MUTED,
                        (x, 638))
        theme.draw_text(surface, "R: restart   E: end   Esc: menu", 13, theme.MUTED, (x, 656))

    def _status(self):
        # (title, detail) shown in the status card.
        if not self.ready:
            return "Searching...", "Running the backtracking"
        if self.pos >= len(self.events):
            return ("Tour found!", "64 / 64 squares") if self.found else ("No tour found", "")
        last = self.last_event()
        if last is None:
            return "Start at X0 = (0,0)", "Press Play or Step"
        if last[0]:
            return "Forward to %s" % name(last[1]), "The knight tries this square"
        return "Dead end at %s" % name(last[1]), "Back, then another move"
