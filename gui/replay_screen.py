# Replay screen: a cat jumps along the tour found by the genetic algorithm, with a result panel
# and the history of the runs. The animation, the sprite sheets and the layout come from the
# `adem` branch; the calculation runs in a GAJob thread (from the `nesrine` branch) so the
# window never freezes and the run can be cancelled.
# The sprite sheets were cut with the pixel rectangles measured below (x, y, width, height).

import math
import os

import pygame

from board import BOARD_SIZE, NB_SQUARES
from gui.ga_job import GAJob
from gui.game_screen import MAX_GENERATIONS, MUTATION_PROBABILITY, POPULATION_SIZE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_UI = os.path.join(ROOT, "assets", "ui.png")
IMAGE_CAT = os.path.join(ROOT, "assets", "cat_sprite.png")

# --- Animation settings ---
JUMP_SECONDS = 0.5                 # duration of one jump at speed x1
SPEEDS = (0.5, 1, 2, 4)
START_SPEED = 1                    # index in SPEEDS
JUMP_HEIGHT = 46                   # height of the jump arc, in pixels
IDLE_FRAME_MS = 180                # milliseconds per idle frame of the cat
FPS = 60
RUNS_SHOWN = 4

# --- Window and layout ---
SIZE = (1220, 740)
BOARD_POS = (20, 50)
SQUARE = 64
COLUMN_X, COLUMN_W = 660, 540
TITLE_PLATE = pygame.Rect(COLUMN_X, 20, COLUMN_W, 80)
PANEL = pygame.Rect(COLUMN_X, 110, COLUMN_W, 540)
RIBBON_SIZE = (260, 62)
BAR_SIZE = (480, 101)
BUTTON_SIZE = (68, 68)
BACK_BUTTON_SIZE = (96, 68)
BUTTONS_Y = 664
BUTTONS_GAP = 24
PLAY_RECT = pygame.Rect((COLUMN_X, BUTTONS_Y), BUTTON_SIZE)
AGAIN_RECT = pygame.Rect((PLAY_RECT.right + BUTTONS_GAP, BUTTONS_Y), BACK_BUTTON_SIZE)
SPEED_RECT = pygame.Rect((AGAIN_RECT.right + BUTTONS_GAP, BUTTONS_Y), BUTTON_SIZE)
PANEL_TOP_MARGIN = 22
LINE_HEIGHT = 26
SECTION_GAP = 8
COORD_RADIUS = 11
COORD_OFFSET = 26                  # distance between the grid and the 1..8 labels

# --- Rectangles measured on the images of assets/ ---
BOARD_RECT = (45, 42, 643, 690)
GRID_ORIGIN = (99, 100)            # top-left corner of the first square, in ui.png
GRID_SIZE = (535, 565)             # the 8 squares, not square (about 66.9 x 70.6)
DARK_FRAME_RECT = (710, 47, 321, 324)
PLATE_RECT = (1055, 50, 277, 141)
PLAY_IMG, PAUSE_IMG = (1054, 198, 80, 80), (1141, 290, 78, 82)
GEAR_IMG, BACK_IMG = (1141, 198, 78, 80), (1227, 296, 106, 76)
RIBBON_IMG = (1051, 394, 276, 73)
BAR_IMG = (727, 603, 610, 129)
BAR_COMPARTMENTS = ((0.03, 0.26), (0.28, 0.72), (0.74, 0.97))   # fractions of the bar width
BAR_CENTER_Y = 0.40
CAT_FRAMES = {                     # 4 idle frames per row
    "front": [(84, 50, 208, 213), (417, 51, 207, 212), (755, 51, 204, 213), (1083, 51, 205, 213)],
    "side": [(88, 294, 242, 216), (419, 296, 244, 214), (766, 295, 242, 216), (1086, 295, 241, 214)],
    "back": [(113, 534, 201, 214), (427, 538, 213, 210), (758, 534, 233, 214), (1101, 533, 217, 215)],
}
CAT_SCALE = 0.32
SHADOW_SIZE = (40, 12)
SHADOW_ALPHA = 90

# --- Colours ---
CREAM = (245, 230, 190)
DARK_BROWN = (74, 44, 26)
GOLD = (255, 205, 80)
TINT = (230, 150, 60)
TINT_ALPHA = 120
LABEL_BG = (38, 22, 14)
WHITE_CREAM = (255, 248, 225)
START_BLUE = (70, 140, 255)
CURRENT_YELLOW = (255, 215, 40)
BACKGROUND = (28, 18, 14)

# Stretch factors that make the squares of the board image square (64 x 64)
SCALE_X = SQUARE / (GRID_SIZE[0] / BOARD_SIZE)
SCALE_Y = SQUARE / (GRID_SIZE[1] / BOARD_SIZE)
SCREEN_ORIGIN = (
    BOARD_POS[0] + round((GRID_ORIGIN[0] - BOARD_RECT[0]) * SCALE_X),
    BOARD_POS[1] + round((GRID_ORIGIN[1] - BOARD_RECT[1]) * SCALE_Y),
)


def cut(sheet, rect, size=None):
    # Extracts a piece of the sheet, optionally resized (smooth).
    piece = sheet.subsurface(rect).copy()
    return pygame.transform.smoothscale(piece, size) if size else piece


def square_rect(square):
    x, y = square
    return pygame.Rect(SCREEN_ORIGIN[0] + x * SQUARE, SCREEN_ORIGIN[1] + y * SQUARE, SQUARE, SQUARE)


def write(surface, text, font, color, **anchor):
    # anchor is center=(x, y), topleft=(x, y), midright=(x, y)...
    image = font.render(text, True, color)
    surface.blit(image, image.get_rect(**anchor))


class ReplayScreen:
    SIZE = SIZE

    def __init__(self, app):
        self.app = app
        self.img = self._load_images()
        self.speed_i = START_SPEED
        self.job = None
        self.path = []
        self.stats = None              # (generations, seconds, fitness, average fitness, found)
        self.progress = 0.0            # number of jumps already done (fractional)
        self.playing = False
        self.start_run()

    # ------------------------------------------------------------------ resources
    def _load_images(self):
        ui = pygame.image.load(IMAGE_UI).convert_alpha()
        cat_sheet = pygame.image.load(IMAGE_CAT).convert_alpha()
        board_size = (round(BOARD_RECT[2] * SCALE_X), round(BOARD_RECT[3] * SCALE_Y))
        cats = {}
        for row, rects in CAT_FRAMES.items():
            cats[row] = [cut(cat_sheet, r, (round(r[2] * CAT_SCALE), round(r[3] * CAT_SCALE)))
                         for r in rects]
        number_font = pygame.font.Font(None, 30)
        return {
            "board": cut(ui, BOARD_RECT, board_size),
            "panel": cut(ui, DARK_FRAME_RECT, PANEL.size),
            "plate": cut(ui, PLATE_RECT, TITLE_PLATE.size),
            "ribbon": cut(ui, RIBBON_IMG, RIBBON_SIZE),
            "bar": cut(ui, BAR_IMG, BAR_SIZE),
            "play": cut(ui, PLAY_IMG, BUTTON_SIZE),
            "pause": cut(ui, PAUSE_IMG, BUTTON_SIZE),
            "gear": cut(ui, GEAR_IMG, BUTTON_SIZE),
            "back": cut(ui, BACK_IMG, BACK_BUTTON_SIZE),
            "cats": cats,
            "numbers_cream": {n: number_font.render(str(n), True, CREAM) for n in range(1, NB_SQUARES + 1)},
            "numbers_brown": {n: number_font.render(str(n), True, DARK_BROWN) for n in range(1, NB_SQUARES + 1)},
            "font_title": pygame.font.Font(None, 54),
            "font_ribbon": pygame.font.Font(None, 30),
            "font": pygame.font.Font(None, 26),
            "font_small": pygame.font.Font(None, 20),
            "font_big": pygame.font.Font(None, 36),
        }

    # ------------------------------------------------------------------ run management
    def start_run(self):
        if self.job is not None:
            self.job.cancel()
        self.playing = False
        self.job = GAJob(POPULATION_SIZE, MUTATION_PROBABILITY, MAX_GENERATIONS)
        self.job.start()

    def finish_run(self):
        path, generations, found = self.job.result
        self.path = path
        self.stats = (generations, self.job.duration, len(path), self.job.average_fitness, found)
        self.app.history.append((generations, self.job.duration))
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
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if PLAY_RECT.collidepoint(event.pos):
                self.toggle_play()
            elif AGAIN_RECT.collidepoint(event.pos):
                self.start_run()
            elif SPEED_RECT.collidepoint(event.pos):
                self.speed_i = (self.speed_i + 1) % len(SPEEDS)

    def update(self):
        dt = self.app_dt()
        if self.job is not None and self.job.done:
            self.finish_run()
        if self.job is None and self.playing:
            self.progress = min(self.progress + dt * SPEEDS[self.speed_i] / JUMP_SECONDS, self.jumps())
            self.playing = self.progress < self.jumps()      # finished: the icon becomes "play"

    def app_dt(self):
        # Seconds since the previous update (the main loop runs at FPS).
        now = pygame.time.get_ticks()
        last = getattr(self, "_last_tick", now)
        self._last_tick = now
        return min((now - last) / 1000, 0.1)

    # ------------------------------------------------------------------ drawing
    def draw(self, surface):
        surface.fill(BACKGROUND)
        if self.job is not None:
            text = "Computing... generation %d   (Esc: menu)" % self.job.generation
            write(surface, text, self.img["font_big"], CREAM, center=surface.get_rect().center)
            return
        self._draw_board(surface)
        surface.blit(self.img["plate"], TITLE_PLATE)
        write(surface, "Knight's Tour", self.img["font_title"], DARK_BROWN, center=TITLE_PLATE.center)
        self._draw_panel(surface)
        self._draw_buttons(surface)

    def _draw_board(self, surface):
        img = self.img
        surface.blit(img["board"], BOARD_POS)
        for i in range(BOARD_SIZE):          # labels 1..8 on the top and left margins
            x, y = square_rect((i, i)).center
            for centre in ((x, SCREEN_ORIGIN[1] - COORD_OFFSET), (SCREEN_ORIGIN[0] - COORD_OFFSET, y)):
                pygame.draw.circle(surface, LABEL_BG, centre, COORD_RADIUS)
                write(surface, str(i + 1), img["font_small"], CREAM, center=centre)
        if len(self.path) < 2:
            return
        for number, square in enumerate(self.path):
            if self.progress >= number:
                fade = 1 if number == 0 else min(self.progress - number, 1)
                self._draw_visited(surface, square, number + 1, fade)
        pygame.draw.rect(surface, START_BLUE, square_rect(self.path[0]).inflate(-4, -4), 4, border_radius=8)
        current = self.path[int(self.progress)]
        pygame.draw.rect(surface, CURRENT_YELLOW, square_rect(current).inflate(-4, -4), 4, border_radius=8)
        self._draw_cat(surface)

    def _draw_visited(self, surface, square, number, fade):
        # Tints the square and writes its order number; fade goes from 0 to 1.
        tint = pygame.Surface((SQUARE, SQUARE), pygame.SRCALPHA)
        tint.fill((*TINT, round(TINT_ALPHA * fade)))
        rect = square_rect(square)
        surface.blit(tint, rect)
        light = sum(square) % 2 == 0
        numbers = self.img["numbers_brown"] if light else self.img["numbers_cream"]
        image = numbers[number].copy()
        image.set_alpha(round(255 * fade))
        surface.blit(image, image.get_rect(center=rect.center))

    def _draw_cat(self, surface):
        path = self.path
        jump = min(int(self.progress), len(path) - 2)
        t = min(self.progress - jump, 1)
        x1, y1 = square_rect(path[jump]).center
        x2, y2 = square_rect(path[jump + 1]).center
        x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        height = math.sin(math.pi * t) * JUMP_HEIGHT
        feet = (round(x), round(y) + SQUARE // 2 - 6)

        dx, dy = x2 - x1, y2 - y1                     # the dominant axis picks the sprite row
        if abs(dy) > abs(dx):
            row, flip = ("back" if dy < 0 else "front"), False
        else:
            row, flip = "side", dx < 0                # the side cat looks to the right
        frames = self.img["cats"][row]
        image = frames[pygame.time.get_ticks() // IDLE_FRAME_MS % len(frames)]
        if flip:
            image = pygame.transform.flip(image, True, False)

        shadow = pygame.Surface(SHADOW_SIZE, pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, SHADOW_ALPHA), shadow.get_rect())
        surface.blit(shadow, shadow.get_rect(center=(feet[0], feet[1] - 4)))
        surface.blit(image, image.get_rect(midbottom=(feet[0], feet[1] - round(height))))

    def _ribbon(self, surface, title, midtop):
        rect = self.img["ribbon"].get_rect(midtop=midtop)
        surface.blit(self.img["ribbon"], rect)
        write(surface, title, self.img["font_ribbon"], CREAM, center=rect.center)
        return rect.bottom

    def _bar(self, surface, values, midtop):
        # Bar with 3 compartments, (title, value) in each.
        rect = self.img["bar"].get_rect(midtop=midtop)
        surface.blit(self.img["bar"], rect)
        y = rect.top + rect.height * BAR_CENTER_Y
        for (start, end), (title, value) in zip(BAR_COMPARTMENTS, values):
            x = rect.left + rect.width * (start + end) / 2
            write(surface, title, self.img["font_small"], CREAM, center=(x, y - 14))
            write(surface, value, self.img["font_big"], GOLD, center=(x, y + 10))
        return rect.bottom

    def _draw_panel(self, surface):
        img = self.img
        surface.blit(img["panel"], PANEL)
        middle = PANEL.centerx
        y = PANEL.top + PANEL_TOP_MARGIN
        generations, seconds, fitness, average, found = self.stats

        y = self._ribbon(surface, "Result", (middle, y))
        y = self._bar(surface, (("Generation", str(generations)), ("Time", "%.2f s" % seconds),
                                ("Fitness", str(fitness))), (middle, y))
        y += SECTION_GAP
        write(surface, "Final average fitness: %.1f" % average, img["font"], CREAM, midtop=(middle, y))
        y += LINE_HEIGHT + SECTION_GAP

        y = self._ribbon(surface, "Parameters", (middle, y))
        write(surface, "Population: %d" % POPULATION_SIZE, img["font"], CREAM, midtop=(middle, y))
        write(surface, "Mutation probability: %s" % MUTATION_PROBABILITY, img["font"], CREAM,
              midtop=(middle, y + LINE_HEIGHT))
        y += 2 * LINE_HEIGHT + SECTION_GAP

        y = self._ribbon(surface, "History", (middle, y))
        history = self.app.history
        first = max(0, len(history) - RUNS_SHOWN)
        for line, (gens, secs) in enumerate(history[first:]):
            number = first + line + 1
            color = GOLD if number == len(history) else CREAM
            write(surface, "Run %d: %d generations, %.2f s" % (number, gens, secs), img["font"],
                  color, midtop=(middle, y + line * LINE_HEIGHT))

    def _draw_buttons(self, surface):
        img = self.img
        surface.blit(img["pause" if self.playing else "play"], PLAY_RECT)
        surface.blit(img["back"], AGAIN_RECT)
        surface.blit(img["gear"], SPEED_RECT)
        write(surface, "x%s" % SPEEDS[self.speed_i], img["font_big"], GOLD,
              midleft=(SPEED_RECT.right + 12, SPEED_RECT.centery))
        right = COLUMN_X + COLUMN_W
        for i, label in enumerate(("Space: play / pause", "R: new run", "Esc: menu")):
            write(surface, label, img["font"], WHITE_CREAM,
                  midright=(right, SPEED_RECT.centery + (i - 1) * LINE_HEIGHT))
