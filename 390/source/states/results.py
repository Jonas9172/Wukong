import pygame
from .. import setup
from .. import tools
from .. import constants as C
from .. components import info


class Results:
    def __init__(self):
        self.setup_background()
        self.info = info.Info('results')
        self.finished = False
        self.next = 'main_menu'

    def setup_background(self):
        self.results = setup.GRAPHICS['results']
        self.results_rect = self.results.get_rect()
        self.results = pygame.transform.scale(self.results, (int(self.results_rect.width*C.BG_MULTI),
                                                       int(self.results_rect.height*C.BG_MULTI)))

        self.background = setup.GRAPHICS['bg']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * C.BG_MULTI),
                                                                   int(self.background_rect.height * C.BG_MULTI)))
        self.viewport = setup.SCREEN.get_rect()

    def update(self, surface, keys, timer=None, coin_number=None, result=None, net=None):
        if keys[pygame.K_q]:
            self.finished = True

        surface.blit(self.background, self.viewport)
        surface.blit(self.results, (200, 60))

        self.info.update(timer, coin_number, result)
        self.info.draw(surface, 400, 280)

