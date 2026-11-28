# The cat of the "Cavalier Jack" style: it is the piece. Frames cut from assets/cat_sprite.png
# (pixel rectangles measured on the sheet), drawn with a shadow and an optional jump arc.

import math
import os

import pygame

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_CAT = os.path.join(ROOT, "assets", "cat_sprite.png")

CAT_FRAMES = {                     # 4 idle frames per row (x, y, width, height)
    "front": [(84, 50, 208, 213), (417, 51, 207, 212), (755, 51, 204, 213), (1083, 51, 205, 213)],
    "side": [(88, 294, 242, 216), (419, 296, 244, 214), (766, 295, 242, 216), (1086, 295, 241, 214)],
    "back": [(113, 534, 201, 214), (427, 538, 213, 210), (758, 534, 233, 214), (1101, 533, 217, 215)],
}
CAT_SCALE = 0.32                   # size of the cat on a 64 px square
IDLE_FRAME_MS = 180
JUMP_HEIGHT = 46                   # jump height on a 64 px square
SHADOW_ALPHA = 90
TILT_DEGREES = 12                  # how much the nose goes up / down during a jump

_sheet = None
_images = {}


def frame(row, index, square, flip=False):
    # One idle frame, scaled for squares of `square` pixels.
    global _sheet
    key = (row, index, square, flip)
    if key not in _images:
        if _sheet is None:
            _sheet = pygame.image.load(IMAGE_CAT).convert_alpha()
        x, y, w, h = CAT_FRAMES[row][index]
        scale = CAT_SCALE * square / 64
        image = pygame.transform.smoothscale(_sheet.subsurface((x, y, w, h)).copy(),
                                             (round(w * scale), round(h * scale)))
        _images[key] = pygame.transform.flip(image, True, False) if flip else image
    return _images[key]


def orientation_for(facing):
    # How the cat is seen when it looks towards facing = (dx, dy): ("front", False) at rest, or
    # ("side", mirrored) for any jump: a knight's move is always shown in profile, the side
    # sprite looks to the right and is mirrored when the move goes to the left.
    if facing is None:
        return "front", False
    return "side", facing[0] < 0


_current = {"view": ("front", False)}        # the view the cat is shown in now


def look(facing, view=None):
    # Asks the cat to face `facing` (or to show a given view: "front" or "back").
    _current["view"] = (view, False) if view else orientation_for(facing)


def draw(surface, center, square, facing=None, phase=None, view=None, lift=0):
    # Cat standing on the square whose centre is `center`. facing = (dx, dy) of the move it
    # looks towards (None = it keeps the view it has); phase in 0..1 is the progress of a jump
    # (None = not jumping): the cat rises and falls along an arc and tilts its nose with it.
    # view = "front" or "back" forces that view (the sprite rows of the sheet), whatever facing is.
    # lift = pixels the cat is raised above its shadow (the bounce of a walking step).
    if facing is not None or view is not None:
        look(facing, view)
    row, flip = _current["view"]
    index = pygame.time.get_ticks() // IDLE_FRAME_MS % 4
    image = frame(row, index, square, flip)
    hop = 0.0
    if phase is not None:
        hop = math.sin(math.pi * min(max(phase, 0.0), 1.0))
        tilt = TILT_DEGREES * math.cos(math.pi * min(max(phase, 0.0), 1.0))
        image = pygame.transform.rotate(image, -tilt if flip else tilt)    # nose up, then down
    k = square / 64
    feet = (round(center[0]), round(center[1]) + square // 2 - round(6 * k))
    shadow = pygame.Surface((round(40 * k), round(12 * k)), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 0, 0, SHADOW_ALPHA), shadow.get_rect())
    surface.blit(shadow, shadow.get_rect(center=(feet[0], feet[1] - round(4 * k))))
    surface.blit(image, image.get_rect(midbottom=(feet[0], feet[1] - round(hop * JUMP_HEIGHT * k) - lift)))
