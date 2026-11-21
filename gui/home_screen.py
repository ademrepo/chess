import pygame

from gui import theme
from gui.assets_loader import knight_image
from gui.widgets import Button


class HomeScreen:
    def __init__(self, app):
        self.app = app
        cx = theme.WIDTH // 2
        self.play_button = Button((cx - 170, 420, 340, 68), "Play", lambda: app.goto("game"),
                                  theme.BTN_PRIMARY, 30)
        self.quit_button = Button((cx - 170, 510, 340, 52), "Quit", app.quit,
                                  theme.BTN_SECONDARY, 22)
        self.buttons = [self.play_button, self.quit_button]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.app.goto("game")
            elif event.key == pygame.K_ESCAPE:
                self.app.quit()
        for button in self.buttons:
            if button.handle_event(event):
                return

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(theme.BG)
        mouse = pygame.mouse.get_pos()
        cx = theme.WIDTH // 2

        image = knight_image("w", 170)
        surface.blit(image, image.get_rect(midtop=(cx, 90)))
        theme.draw_text(surface, "Knight's Tour Game", 60, theme.TEXT, (cx, 285), bold=True,
                        anchor="midtop")
        for button in self.buttons:
            button.draw(surface, mouse)
