# Loads the piece images from specs/assets/pieces (cburnett knight, GPLv2+, see specs/ASSETS.md).
# The SVG files are rasterised by pygame at the exact size needed, so they stay sharp.

import os

import pygame

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES_DIR = os.path.join(ROOT, "specs", "assets", "pieces")

_cache = {}


def knight_image(color, size):
    # color: "w" (white knight) or "b" (black knight).
    key = (color, size)
    if key not in _cache:
        path = os.path.join(PIECES_DIR, color + "N.svg")
        _cache[key] = pygame.image.load_sized_svg(path, (size, size))
    return _cache[key]
