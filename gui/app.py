# Window and main loop: switches between the home, game and replay screens.

import pygame

from gui import theme
from gui.assets_loader import knight_image
from gui.game_screen import DEFAULT_SETTINGS, GameScreen
from gui.home_screen import HomeScreen
from gui.lab_screen import LabScreen
from gui.replay_screen import ReplayScreen
from gui.settings_screen import SettingsScreen

SCREENS = {"home": HomeScreen, "game": GameScreen, "replay": ReplayScreen,
           "settings": SettingsScreen, "lab": LabScreen}


class App:
    def __init__(self):
        pygame.init()
        self.history = []                 # (generations, seconds) of every run watched
        self.running = True
        self.settings = dict(DEFAULT_SETTINGS)    # chosen in the settings screen
        self.goto("home")
        pygame.display.set_icon(knight_image("w", 64))

    def goto(self, name):
        screen_class = SCREENS[name]
        # Each screen has its own window size; the screen is built after the window exists
        # because it loads images that need a display.
        self.surface = pygame.display.set_mode(getattr(screen_class, "SIZE", (theme.WIDTH, theme.HEIGHT)))
        pygame.display.set_caption("Knight's Tour - Genetic Algorithm")
        self.screen = screen_class(self)

    def job_settings(self):
        # Arguments of GAJob, in order.
        s = self.settings
        return s["population"], s["mutation"], s["max_generations"], s["tournament"]

    def quit(self):
        self.running = False

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.screen.handle_event(event)
            self.screen.update()
            self.screen.draw(self.surface)
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
