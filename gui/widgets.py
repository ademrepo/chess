# A single reusable widget: a chess.com-style 3D button.

import pygame

from gui import theme


class Button:
    def __init__(self, rect, label, on_click, style=None, size=20):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.on_click = on_click
        self.style = style or theme.BTN_SECONDARY
        self.size = size
        self.enabled = True

    def draw(self, surface, mouse_pos):
        face, hover, shadow = self.style if self.enabled else theme.BTN_DISABLED
        hovered = self.enabled and self.rect.collidepoint(mouse_pos)
        # bottom shadow gives the "3D" chess.com look
        pygame.draw.rect(surface, shadow, self.rect.move(0, 4), border_radius=8)
        pygame.draw.rect(surface, hover if hovered else face, self.rect, border_radius=8)
        color = theme.TEXT if self.enabled else theme.MUTED
        theme.draw_text(surface, self.label, self.size, color, self.rect.center, bold=True,
                        anchor="center")

    def handle_event(self, event):
        # Returns True if the click was consumed by this button.
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.enabled
                and self.rect.collidepoint(event.pos)):
            self.on_click()
            return True
        return False
