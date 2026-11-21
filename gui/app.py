# Window and main loop: switches between the home screen and the game screen.

import pygame

from gui import theme
from gui.assets_loader import knight_image
from gui.game_screen import GameScreen
from gui.home_screen import HomeScreen


class App:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((theme.WIDTH, theme.HEIGHT))
        pygame.display.set_caption("Knight's Tour - Genetic Algorithm")
        pygame.display.set_icon(knight_image("w", 64))
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen = HomeScreen(self)

    def goto(self, name):
        self.screen = HomeScreen(self) if name == "home" else GameScreen(self)

    def quit(self):
        self.running = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.screen.handle_event(event)
            self.screen.update()
            self.screen.draw(self.surface)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
