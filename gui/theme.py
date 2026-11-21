# Colours, fonts and drawing helpers. The palette imitates the chess.com "green" look
# (dark page, green/cream board, green 3D buttons). Only colours are imitated, no chess.com
# file is used (see specs/ASSETS.md).

import pygame

# Window and board geometry
WIDTH, HEIGHT = 1060, 730
SQUARE = 80
BOARD_X, BOARD_Y = 40, 40
BOARD_PIXELS = SQUARE * 8
PANEL_X, PANEL_W = 720, 300

# Page
BG = (49, 46, 43)
PANEL = (38, 36, 33)
CARD = (44, 42, 39)

# Board (chess.com green theme)
LIGHT = (238, 238, 210)
DARK = (118, 150, 86)
VISITED_LIGHT = (245, 246, 130)
VISITED_DARK = (185, 202, 67)

# Text
TEXT = (255, 255, 255)
MUTED = (160, 158, 155)

# Buttons: (face, hover, bottom shadow)
BTN_PRIMARY = ((129, 182, 76), (149, 200, 94), (69, 117, 60))
BTN_SECONDARY = ((69, 66, 63), (84, 81, 77), (45, 43, 40))
BTN_DANGER = ((201, 79, 66), (220, 98, 84), (134, 46, 38))
BTN_DISABLED = ((58, 56, 53), (58, 56, 53), (45, 43, 40))

ARROW = (255, 170, 0, 150)
GOLD = (255, 200, 60)

_fonts = {}


def font(size, bold=False):
    key = (size, bold)
    if key not in _fonts:
        _fonts[key] = pygame.font.SysFont("segoeui,helveticaneue,arial", size, bold=bold)
    return _fonts[key]


def draw_text(surface, text, size, color, pos, bold=False, anchor="topleft"):
    # Draws text and returns its rectangle. `anchor` is any pygame.Rect attribute
    # ("topleft", "center", "midtop", "topright"...).
    image = font(size, bold).render(text, True, color)
    rect = image.get_rect(**{anchor: pos})
    surface.blit(image, rect)
    return rect
