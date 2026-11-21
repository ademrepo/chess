# Window and main loop: switches between the home, game and replay screens.

import pygame

from gui import theme
from gui.assets_loader import knight_image
from gui.game_screen import GameScreen
from gui.home_screen import HomeScreen
from gui.replay_screen import ReplayScreen

SCREENS = {"home": HomeScreen, "game": GameScreen, "replay": ReplayScreen}


class App:
    def __init__(self):
        pygame.init()
        self.history = []                 # (generations, seconds) of every run watched
        self.running = True
        self.goto("home")
        pygame.display.set_icon(knight_image("w", 64))

    def goto(self, name):
        screen_class = SCREENS[name]
        # Each screen has its own window size; the screen is built after the window exists
        # because it loads images that need a display.
        self.surface = pygame.display.set_mode(getattr(screen_class, "SIZE", (theme.WIDTH, theme.HEIGHT)))
        pygame.display.set_caption("Knight's Tour - Genetic Algorithm")
        self.screen = screen_class(self)

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
