# A single reusable widget: a 3D button, drawn by the current style (see gui/theme.py).

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
        self.selected = False           # lit with a border: the action this button started is running

    def draw(self, surface, mouse_pos):
        face, hover, shadow = self.style if self.enabled else theme.BTN_DISABLED
        hovered = self.enabled and self.rect.collidepoint(mouse_pos)
        theme.draw_button(surface, self.rect, self.label, hover if hovered else face, shadow,
                          self.size, self.enabled)
        if self.selected:
            pygame.draw.rect(surface, theme.SELECT, self.rect.inflate(8, 8), 3, border_radius=10)

    def handle_event(self, event):
        # Returns True if the click was consumed by this button.
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.enabled
                and self.rect.collidepoint(event.pos)):
            self.on_click()
            return True
        return False
