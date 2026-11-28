# Colours, fonts and drawing helpers of the two styles of the interface:
#   "classic": the chess.com-like green look (only colours are imitated, no chess.com file is
#              used, see specs/ASSETS.md), the piece is the white knight;
#   "jack":    "Cavalier Jack", the wooden look, the piece is the cat.
# use(style) switches the module-level colours; the screens read theme.X every time they draw,
# and the helpers below (squares, frame, cards, buttons, piece) draw in the current style.

import math

import pygame

# Window and board geometry
WIDTH, HEIGHT = 1060, 730
SQUARE = 80
BOARD_X, BOARD_Y = 40, 40
BOARD_PIXELS = SQUARE * 8
PANEL_X, PANEL_W = 720, 300

STYLE = "classic"
STYLES = {"classic": "Chess Classic", "jack": "Cavalier Jack"}

CLASSIC = dict(
    BG=(49, 46, 43), PANEL=(38, 36, 33), CARD=(44, 42, 39),
    LIGHT=(238, 238, 210), DARK=(118, 150, 86),
    VISITED_LIGHT=(245, 246, 130), VISITED_DARK=(185, 202, 67),
    COORD_LIGHT=(96, 120, 60), COORD_DARK=(238, 238, 210), NUMBER=(96, 120, 60),
    TEXT=(255, 255, 255), MUTED=(160, 158, 155),
    BTN_PRIMARY=((129, 182, 76), (149, 200, 94), (69, 117, 60)),
    BTN_SECONDARY=((69, 66, 63), (84, 81, 77), (45, 43, 40)),
    BTN_DANGER=((201, 79, 66), (220, 98, 84), (134, 46, 38)),
    BTN_DISABLED=((58, 56, 53), (58, 56, 53), (45, 43, 40)),
    ARROW=(255, 170, 0, 150), GOLD=(255, 200, 60), DOT=(0, 0, 0, 55), LINE=(255, 170, 0), GRID=(70, 68, 64), SELECT=(255, 255, 255),
)
JACK = dict(
    BG=(28, 18, 14), PANEL=(62, 30, 19), CARD=(48, 27, 19),
    LIGHT=(235, 209, 160), DARK=(56, 36, 35),
    VISITED_LIGHT=(236, 180, 100), VISITED_DARK=(150, 98, 48),
    COORD_LIGHT=(110, 76, 44), COORD_DARK=(214, 188, 140), NUMBER=(52, 28, 16),
    TEXT=(250, 238, 205), MUTED=(222, 194, 156),
    BTN_PRIMARY=((222, 156, 62), (240, 176, 84), (140, 84, 34)),
    BTN_SECONDARY=((158, 100, 62), (178, 118, 76), (96, 56, 36)),
    BTN_DANGER=((184, 76, 58), (204, 96, 76), (110, 40, 32)),
    BTN_DISABLED=((96, 72, 58), (96, 72, 58), (66, 46, 38)),
    ARROW=(255, 214, 130, 170), GOLD=(255, 205, 80), DOT=(255, 226, 170, 120), LINE=(255, 214, 130),
    GRID=(128, 94, 68), SELECT=(255, 226, 150),
)
globals().update(CLASSIC)


def use(style):
    # Switches the colours to "classic" or "jack".
    global STYLE
    STYLE = style
    globals().update(JACK if style == "jack" else CLASSIC)


def is_jack():
    return STYLE == "jack"


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


# ---------------------------------------------------------------------- style-aware helpers
def draw_square(surface, rect, dark, visited=False):
    # One square of the board.
    if is_jack():
        from gui import wood
        variant = (rect.x * 31 + rect.y * 17) % 4
        surface.blit(wood.square(rect.w, dark, visited, variant), rect)
        return
    if visited:
        color = VISITED_DARK if dark else VISITED_LIGHT
    else:
        color = DARK if dark else LIGHT
    pygame.draw.rect(surface, color, rect)


def draw_board_frame(surface, board_rect, margin=22):
    # Wooden frame around the board ("jack" only, the classic board has no frame).
    if is_jack():
        from gui import wood
        frame = wood.board_frame(board_rect.w, margin)
        surface.blit(frame, (board_rect.x - margin, board_rect.y - margin))


def draw_card(surface, rect):
    # Box that holds a group of numbers.
    rect = pygame.Rect(rect)
    if is_jack():
        from gui import wood
        surface.blit(wood.inset(rect.w, rect.h), rect)
    else:
        pygame.draw.rect(surface, CARD, rect, border_radius=8)


def draw_side_panel(surface, rect):
    # Big background of a column of controls ("jack": wooden frame, "classic": nothing).
    if is_jack():
        from gui import wood
        rect = pygame.Rect(rect)
        surface.blit(wood.panel(rect.w, rect.h), rect)


def draw_dialog(surface, rect):
    # Card of the pop-ups ("tour complete").
    rect = pygame.Rect(rect)
    if is_jack():
        from gui import wood
        surface.blit(wood.panel(rect.w, rect.h), rect)
    else:
        pygame.draw.rect(surface, PANEL, rect, border_radius=12)


def draw_button(surface, rect, label, face, shadow, size, enabled):
    # Draws a button of the current style; the text is centred.
    if is_jack():
        from gui import wood
        surface.blit(wood.button(rect.w, rect.h, face, shadow), rect)
        color = TEXT if enabled else MUTED
        draw_text(surface, label, size, (38, 20, 14), (rect.centerx + 1, rect.centery - 1), bold=True,
                  anchor="center")
        draw_text(surface, label, size, color, (rect.centerx, rect.centery - 2), bold=True,
                  anchor="center")
        return
    pygame.draw.rect(surface, shadow, rect.move(0, 4), border_radius=8)      # bottom shadow = 3D look
    pygame.draw.rect(surface, face, rect, border_radius=8)
    draw_text(surface, label, size, TEXT if enabled else MUTED, rect.center, bold=True, anchor="center")


def draw_piece(surface, center, size, facing=None, phase=None, view=None, lift=0):
    # The piece of the style on the square whose centre is `center`: the knight, or the cat.
    # facing = (dx, dy) direction of the move, phase = 0..1 progress of a jump, view = "front" or
    # "back" to show that side of the cat (cat only).
    if is_jack():
        from gui import cat
        cat.draw(surface, center, size, facing, phase, view, lift)
        return
    from gui.assets_loader import knight_image
    image = knight_image("w", size)
    surface.blit(image, image.get_rect(center=center))


def jump(t):
    # Height of a jump (0..1) at time t in 0..1.
    return math.sin(math.pi * min(max(t, 0.0), 1.0))
