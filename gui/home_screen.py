import pygame

from gui import theme
from gui.assets_loader import knight_image
from gui.widgets import Button


class HomeScreen:
    def __init__(self, app):
        self.app = app
        cx = theme.WIDTH // 2
        self.play_button = Button((cx - 170, 372, 340, 62), "Play", lambda: app.goto("game"),
                                  theme.BTN_PRIMARY, 30)
        self.lab_button = Button((cx - 170, 448, 340, 52), "Algorithm lab (step by step)",
                                 lambda: app.goto("lab"), theme.BTN_PRIMARY, 21)
        self.watch_button = Button((cx - 170, 512, 340, 52), "Watch the algorithm (cat)",
                                   lambda: app.goto("replay"), theme.BTN_SECONDARY, 21)
        self.settings_button = Button((cx - 170, 576, 340, 52), "Settings",
                                      lambda: app.goto("settings"), theme.BTN_SECONDARY, 21)
        self.quit_button = Button((cx - 170, 640, 340, 48), "Quit", app.quit,
                                  theme.BTN_SECONDARY, 21)
        self.buttons = [self.play_button, self.lab_button, self.watch_button,
                        self.settings_button, self.quit_button]

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

        image = knight_image("w", 160)
        surface.blit(image, image.get_rect(midtop=(cx, 70)))
        theme.draw_text(surface, "Knight's Tour Game", 60, theme.TEXT, (cx, 275), bold=True,
                        anchor="midtop")
        for button in self.buttons:
            button.draw(surface, mouse)
