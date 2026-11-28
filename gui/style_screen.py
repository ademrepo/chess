# First screen: choose the style of the interface, "Chess Classic" or "Cavalier Jack".
# Both have the same features (play, genetic algorithm, CSP backtracking, labs, settings).

import pygame

from gui import cat, theme, wood
from gui.assets_loader import knight_image

CARD_W, CARD_H = 440, 470
GAP = 50


class StyleScreen:
    def __init__(self, app):
        self.app = app
        theme.use("classic")             # neutral colours for this screen
        total = 2 * CARD_W + GAP
        left = (theme.WIDTH - total) // 2
        top = 170
        self.cards = {"classic": pygame.Rect(left, top, CARD_W, CARD_H),
                      "jack": pygame.Rect(left + CARD_W + GAP, top, CARD_W, CARD_H)}

    def choose(self, style):
        theme.use(style)
        self.app.goto("home")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.choose("classic")
            elif event.key == pygame.K_2:
                self.choose("jack")
            elif event.key == pygame.K_ESCAPE:
                self.app.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for style, rect in self.cards.items():
                if rect.collidepoint(event.pos):
                    self.choose(style)

    def update(self):
        pass

    def draw(self, surface):
        surface.fill((40, 37, 34))
        mouse = pygame.mouse.get_pos()
        theme.draw_text(surface, "Knight's Tour", 52, (255, 255, 255), (theme.WIDTH // 2, 40), bold=True,
                        anchor="midtop")
        theme.draw_text(surface, "Choose your style", 22, (170, 168, 165), (theme.WIDTH // 2, 112),
                        anchor="midtop")
        self._draw_classic(surface, self.cards["classic"], self.cards["classic"].collidepoint(mouse))
        self._draw_jack(surface, self.cards["jack"], self.cards["jack"].collidepoint(mouse))

    # ------------------------------------------------------------------ the two cards
    def _draw_classic(self, surface, rect, hovered):
        pygame.draw.rect(surface, (58, 56, 53) if hovered else (49, 46, 43), rect, border_radius=14)
        if hovered:
            pygame.draw.rect(surface, (129, 182, 76), rect, 4, border_radius=14)
        board = pygame.Rect(rect.x + 70, rect.y + 36, 300, 300)
        for y in range(4):
            for x in range(4):
                color = (118, 150, 86) if (x + y) % 2 else (238, 238, 210)
                pygame.draw.rect(surface, color, (board.x + x * 75, board.y + y * 75, 75, 75))
        image = knight_image("w", 90)
        surface.blit(image, image.get_rect(center=(board.x + 75 + 37, board.y + 75 + 37)))
        theme.draw_text(surface, "Chess Classic", 34, (255, 255, 255), (rect.centerx, rect.y + 358),
                        bold=True, anchor="midtop")
        theme.draw_text(surface, "Green board, white knight", 17, (170, 168, 165),
                        (rect.centerx, rect.y + 406), anchor="midtop")
        theme.draw_text(surface, "Press 1", 14, (129, 182, 76), (rect.centerx, rect.y + 436), anchor="midtop")

    def _draw_jack(self, surface, rect, hovered):
        surface.blit(wood.panel(rect.w, rect.h), rect)
        if hovered:
            pygame.draw.rect(surface, (255, 205, 80), rect, 4, border_radius=8)
        board = pygame.Rect(rect.x + 70, rect.y + 36, 300, 300)
        for y in range(4):
            for x in range(4):
                surface.blit(wood.square(75, (x + y) % 2 == 1, False, (x + y * 4) % 4),
                             (board.x + x * 75, board.y + y * 75))
        cat.draw(surface, (board.x + 75 + 37, board.y + 75 + 37), 75)
        theme.draw_text(surface, "Cavalier Jack", 34, (245, 230, 190), (rect.centerx, rect.y + 358),
                        bold=True, anchor="midtop")
        theme.draw_text(surface, "Wooden board, a cat for the piece", 17, (196, 164, 124),
                        (rect.centerx, rect.y + 406), anchor="midtop")
        theme.draw_text(surface, "Press 2", 14, (255, 205, 80), (rect.centerx, rect.y + 436), anchor="midtop")
