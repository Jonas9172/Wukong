from .. import setup
from .. components import info
from .. import constants as C
import pygame


class LoadScreen:
    def __init__(self):

        self.set_background()
        self.finished = False
        self.next = 'game_screen_2'
        self.timer = 0
        self.info = info.Info('load_screen_2')

    def set_background(self):
        self.background = setup.GRAPHICS['bg']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * C.BG_MULTI),
                                                                   int(self.background_rect.height * C.BG_MULTI)))
        self.viewport = setup.SCREEN.get_rect()

    def update(self, surface, keys, timer, coin_number, result, net):
        self.info.update()
        self.draw(surface)
        if self.timer == 0:
            self.timer = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.timer > 2000:
            self.finished = True
            self.timer = 0

    def draw(self, surface):
        surface.blit(self.background, self.viewport)
        self.info.draw(surface)