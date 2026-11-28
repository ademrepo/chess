# The wooden pixel-art kit of the "Cavalier Jack" style: panels, ribbons, bars, buttons, board
# frame, squares and icons, all DRAWN BY THIS CODE (no piece is cut out of an image, so nothing
# is blurry or badly cropped and every piece can have any size).
# Method: each piece is drawn on a small surface (1 art pixel = P screen pixels) and enlarged
# without smoothing, which gives the pixel-art look. Colours were sampled on assets/ui.png.

import math
import random

import pygame

P = 3                                        # screen pixels per art pixel

OUTLINE = (30, 15, 11)
WOOD, WOOD_LIGHT, WOOD_DARK = (108, 67, 48), (132, 84, 58), (82, 48, 36)
EDGE_HI, EDGE_LO = (158, 104, 70), (60, 32, 27)
RECESS, RECESS_DARK, RECESS_LIGHT = (62, 30, 19), (40, 18, 12), (88, 50, 35)
BRASS, BRASS_HI, BRASS_LO = (176, 128, 68), (222, 174, 100), (112, 72, 38)
PLANK, PLANK_LIGHT, PLANK_DARK, PLANK_HI, PLANK_LO = (166, 101, 53), (188, 120, 64), (142, 84, 44), (214, 152, 92), (110, 64, 34)
TAIL = (122, 72, 40)
CREAM, CREAM_HI, CREAM_LO = (235, 209, 160), (247, 230, 190), (205, 172, 124)
DARK_SQ, DARK_SQ_LIGHT, DARK_SQ_DARK = (56, 36, 35), (74, 50, 43), (42, 27, 27)
TRAY = (44, 36, 33)
TEXT = (245, 230, 190)

_cache = {}


def cached(key, build):
    if key not in _cache:
        _cache[key] = build()
    return _cache[key]


def small(w, h):
    return pygame.Surface((max(1, -(-w // P)), max(1, -(-h // P))), pygame.SRCALPHA)


def up(surface, w, h):
    return pygame.transform.scale(surface, (w, h))


def lighter(color, amount):
    return tuple(min(255, round(v + (255 - v) * amount)) for v in color)


def darker(color, amount):
    return tuple(round(v * (1 - amount)) for v in color)


def grain(surface, rect, base, light, dark, seed, vertical=False, density=0.55):
    # Wood: a flat colour with short lighter / darker streaks along the grain.
    x0, y0, w, h = rect
    surface.fill(base, rect)
    rnd = random.Random(seed)
    lines, length_max = (w, h) if vertical else (h, w)
    for i in range(lines):
        if rnd.random() > density:
            continue
        color = light if rnd.random() < 0.5 else dark
        length = rnd.randint(3, max(4, length_max // 2))
        start = rnd.randint(0, max(0, length_max - length))
        if vertical:
            surface.fill(color, (x0 + i, y0 + start, 1, length))
        else:
            surface.fill(color, (x0 + start, y0 + i, length, 1))


def round_corners(surface):
    w, h = surface.get_size()
    for x, y in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        surface.set_at((x, y), (0, 0, 0, 0))


def bevel(surface, rect, hi, lo):
    # 1 art pixel of light on the top / left edges and of shadow on the bottom / right ones.
    x, y, w, h = rect
    surface.fill(hi, (x, y, w, 1))
    surface.fill(hi, (x, y, 1, h))
    surface.fill(lo, (x, y + h - 1, w, 1))
    surface.fill(lo, (x + w - 1, y, 1, h))


def brass_plate(surface, x, y, size=6):
    surface.fill(BRASS_LO, (x, y, size, size))
    surface.fill(BRASS, (x, y, size - 1, size - 1))
    surface.fill(BRASS_HI, (x, y, size - 1, 1))
    surface.fill(BRASS_HI, (x, y, 1, size - 1))
    surface.set_at((x + size // 2, y + size // 2), EDGE_LO)


def rivet(surface, x, y):
    surface.set_at((x, y), BRASS_HI)
    surface.set_at((x + 1, y), BRASS_LO)
    surface.set_at((x, y + 1), BRASS_LO)
    surface.set_at((x + 1, y + 1), EDGE_LO)


# ---------------------------------------------------------------------- panels and bars
def panel(w, h):
    # Big wooden frame with a dark recess and a brass plate in each corner.
    def build():
        s = small(w, h)
        aw, ah = s.get_size()
        s.fill(OUTLINE)
        grain(s, (1, 1, aw - 2, ah - 2), WOOD, WOOD_LIGHT, WOOD_DARK, aw * 31 + ah)
        bevel(s, (1, 1, aw - 2, ah - 2), EDGE_HI, EDGE_LO)
        inner = pygame.Rect(5, 5, aw - 10, ah - 10)
        s.fill(OUTLINE, inner.inflate(2, 2))
        s.fill(RECESS, inner)
        bevel(s, inner, RECESS_DARK, RECESS_LIGHT)
        for x, y in ((inner.x + 1, inner.y + 1), (inner.right - 7, inner.y + 1),
                     (inner.x + 1, inner.bottom - 7), (inner.right - 7, inner.bottom - 7)):
            brass_plate(s, x, y)
        round_corners(s)
        return up(s, w, h)
    return cached(("panel", w, h), build)


def inset(w, h):
    # Card that holds numbers: a wooden frame around a dark recess, so it stands out from the page.
    def build():
        s = small(w, h)
        aw, ah = s.get_size()
        s.fill(OUTLINE)
        grain(s, (1, 1, aw - 2, ah - 2), WOOD, WOOD_LIGHT, WOOD_DARK, aw * 7 + ah, density=0.4)
        bevel(s, (1, 1, aw - 2, ah - 2), EDGE_HI, EDGE_LO)
        inner = pygame.Rect(3, 3, aw - 6, ah - 6)
        s.fill(OUTLINE, inner.inflate(2, 2))
        s.fill((56, 32, 22), inner)
        bevel(s, inner, (36, 19, 13), (84, 52, 36))
        round_corners(s)
        return up(s, w, h)
    return cached(("inset", w, h), build)


def ribbon(w, h):
    # Plank with two folded tails, for the titles of the sections.
    def build():
        s = small(w, h)
        aw, ah = s.get_size()
        tail = max(6, round(ah * 0.9))
        tail_h = ah - 3
        mid = tail_h / 2
        for x0 in (0, aw - tail):
            s.fill(OUTLINE, (x0, 3, tail, tail_h))
            s.fill(TAIL, (x0 + 1, 4, tail - 2, tail_h - 2))
        depth = min(4, tail // 2)
        for row in range(tail_h):                       # V notch at the outer end of each tail
            cut = round(depth * (1 - abs(row - mid) / mid))
            for i in range(cut):
                s.set_at((i, 3 + row), (0, 0, 0, 0))
                s.set_at((aw - 1 - i, 3 + row), (0, 0, 0, 0))
        body = pygame.Rect(tail - 3, 0, aw - 2 * tail + 6, ah - 3)
        s.fill(OUTLINE, body)
        grain(s, body.inflate(-2, -2), PLANK, PLANK_LIGHT, PLANK_DARK, aw + ah * 7)
        bevel(s, body.inflate(-2, -2), PLANK_HI, PLANK_LO)
        return up(s, w, h)
    return cached(("ribbon", w, h), build)


def tray(w, h, compartments):
    # Wooden tray with dark compartments; compartments = ((start, end), ...) as fractions of w.
    def build():
        s = small(w, h)
        aw, ah = s.get_size()
        s.fill(OUTLINE)
        grain(s, (1, 1, aw - 2, ah - 2), PLANK, PLANK_LIGHT, PLANK_DARK, aw * 5 + ah)
        bevel(s, (1, 1, aw - 2, ah - 2), PLANK_HI, PLANK_LO)
        for start, end in compartments:
            box = pygame.Rect(round(aw * start), 4, round(aw * (end - start)), ah - 10)
            s.fill(OUTLINE, box.inflate(2, 2))
            s.fill(TRAY, box)
            bevel(s, box, (22, 16, 14), (70, 56, 50))
        round_corners(s)
        return up(s, w, h)
    return cached(("tray", w, h, tuple(compartments)), build)


def button(w, h, face, shadow):
    # Raised wooden key: lit top edge, darker front band. `face` and `shadow` are colours.
    def build():
        s = small(w, h)
        aw, ah = s.get_size()
        s.fill(OUTLINE)
        top = pygame.Rect(1, 1, aw - 2, ah - 4)
        grain(s, top, face, lighter(face, 0.12), darker(face, 0.10), aw * 3 + ah, density=0.35)
        s.fill(shadow, (1, ah - 3, aw - 2, 2))
        s.fill(lighter(face, 0.35), (1, 1, aw - 2, 1))
        s.fill(lighter(face, 0.2), (1, 1, 1, ah - 4))
        s.fill(darker(face, 0.25), (aw - 2, 1, 1, ah - 4))
        round_corners(s)
        return up(s, w, h)
    return cached(("button", w, h, face, shadow), build)


def plate(w, h):
    # Cream plaque in a wooden frame (title of the screen).
    def build():
        s = small(w, h)
        aw, ah = s.get_size()
        s.fill(OUTLINE)
        grain(s, (1, 1, aw - 2, ah - 2), WOOD, WOOD_LIGHT, WOOD_DARK, aw * 13 + ah)
        bevel(s, (1, 1, aw - 2, ah - 2), EDGE_HI, EDGE_LO)
        face = pygame.Rect(5, 5, aw - 10, ah - 10)
        s.fill(OUTLINE, face.inflate(2, 2))
        grain(s, face, CREAM, CREAM_HI, CREAM_LO, aw + ah * 3, density=0.15)
        bevel(s, face, CREAM_LO, CREAM_HI)
        for x, y in ((2, 2), (aw - 4, 2), (2, ah - 4), (aw - 4, ah - 4)):
            rivet(s, x, y)
        round_corners(s)
        return up(s, w, h)
    return cached(("plate", w, h), build)


# ---------------------------------------------------------------------- board
def square(size, dark, tinted, variant=0):
    # One square of the board: cream tile or dark wood; `tinted` = already visited (orange).
    def build():
        s = small(size, size)
        aw, ah = s.get_size()
        if dark:
            grain(s, (0, 0, aw, ah), DARK_SQ, DARK_SQ_LIGHT, DARK_SQ_DARK, 100 + variant, vertical=True)
            s.fill(DARK_SQ_DARK, (0, ah - 1, aw, 1))
        else:
            grain(s, (0, 0, aw, ah), CREAM, CREAM_HI, CREAM_LO, 200 + variant, density=0.04)
            bevel(s, (1, 1, aw - 2, ah - 2), CREAM_HI, CREAM_LO)
        image = up(s, size, size)
        if tinted:
            tint = pygame.Surface((size, size), pygame.SRCALPHA)
            tint.fill((230, 150, 60, 130))
            image.blit(tint, (0, 0))
        return image
    return cached(("square", size, dark, tinted, variant), build)


def board_frame(board_px, margin):
    # Wooden frame around an 8x8 board of board_px pixels; the squares are drawn on top of it.
    total = board_px + 2 * margin

    def build():
        s = small(total, total)
        aw, ah = s.get_size()
        s.fill(OUTLINE)
        grain(s, (1, 1, aw - 2, ah - 2), WOOD, WOOD_LIGHT, WOOD_DARK, aw * 17)
        bevel(s, (1, 1, aw - 2, ah - 2), EDGE_HI, EDGE_LO)
        hole = margin // P
        s.fill(OUTLINE, (hole - 1, hole - 1, aw - 2 * hole + 2, ah - 2 * hole + 2))
        bracket = max(4, hole - 2)
        for x, y in ((2, 2), (aw - 2 - bracket, 2), (2, ah - 2 - bracket), (aw - 2 - bracket, ah - 2 - bracket)):
            brass_plate(s, x, y, bracket)
        for t in (0.35, 0.65):                          # rivets in the middle of the sides
            rivet(s, round(aw * t), 2)
            rivet(s, round(aw * t), ah - 4)
            rivet(s, 2, round(ah * t))
            rivet(s, aw - 4, round(ah * t))
        round_corners(s)
        return up(s, total, total)
    return cached(("frame", board_px, margin), build)


# ---------------------------------------------------------------------- icons
ICON_N = 15                                  # icons are drawn on a 15 x 15 grid of art pixels


def _in_triangle(px, py, a, b, c):
    def side(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    d1, d2, d3 = side((px, py), a, b), side((px, py), b, c), side((px, py), c, a)
    return not ((d1 < 0 or d2 < 0 or d3 < 0) and (d1 > 0 or d2 > 0 or d3 > 0))


def _icon_pixels(kind):
    # The art pixels (x, y) that are lit for an icon; each pixel is tested at its centre, so the
    # shapes come out clean and symmetrical.
    n, c = ICON_N, ICON_N / 2
    lit = set()
    for y in range(n):
        for x in range(n):
            px, py = x + 0.5, y + 0.5
            dx, dy = px - c, py - c
            r = math.hypot(dx, dy)
            on = False
            if kind == "play":
                on = _in_triangle(px, py, (4, 2), (4, 13), (12, 7.5))
            elif kind == "pause":
                on = 3 <= y <= 11 and (3 <= x <= 5 or 9 <= x <= 11)
            elif kind == "gear":
                on = 2.1 < r <= 5.0
                for k in range(8):                       # 8 teeth, one every 45 degrees
                    ax, ay = math.cos(k * math.pi / 4), math.sin(k * math.pi / 4)
                    along, across = dx * ax + dy * ay, abs(-dx * ay + dy * ax)
                    if 4.2 < along <= 7.2 and across <= 1.5:
                        on = True
            elif kind == "restart":
                angle = math.degrees(math.atan2(dy, dx))
                ring = 3.6 <= r <= 5.6 and not -88 <= angle <= -8        # a ring open at the top right
                tip = (c + 4.6 * math.cos(math.radians(-88)) + 3.4, c + 4.6 * math.sin(math.radians(-88)) + 0.3)
                head = _in_triangle(px, py, (tip[0] - 3.4, tip[1] - 2.6), (tip[0] - 3.4, tip[1] + 2.6), tip)
                on = ring or head
            if on:
                lit.add((x, y))
    return lit


def icon(kind, size=None):
    # Cream icon with a dark shadow on a transparent surface: play, pause, restart or gear.
    # Always (ICON_N + 1) art pixels wide, i.e. 48 screen pixels.
    def build():
        n = ICON_N + 1
        s = pygame.Surface((n, n), pygame.SRCALPHA)
        pixels = _icon_pixels(kind)
        for x, y in pixels:
            s.set_at((x + 1, y + 1), (38, 20, 14))
        for x, y in pixels:
            s.set_at((x, y), TEXT)
        return up(s, n * P, n * P)
    return cached(("icon", kind), build)
