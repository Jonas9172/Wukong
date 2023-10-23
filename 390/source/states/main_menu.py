import pygame

import main
from network import Network
from . import game_screen_2
from .. import setup
from .. import tools
from .. import constants as C
from .. components import info


class MainMenu:
    def __init__(self):
        self.frames = []
        self.frame_rects = [(0, 0, 45, 45), (45, 0, 45, 45), (90, 0, 45, 45), (135, 0, 45, 45)]
        self.frame_index = 0
        self.timer = 0
        self.loadingIcon_frame(self.frame_rects)
        self.image = self.frames[self.frame_index]
        self.setup_background()
        self.setup_cursor()
        self.info = info.Info('main_menu')
        self.finished = False
        self.next = 'load_screen'
        self.ready = 0
        self.data = None
        self.start_match = 0
        self.a = 1
        self.net = None

    def setup_background(self):
        self.logo = setup.GRAPHICS['logo']
        self.logo_rect = self.logo.get_rect()
        self.logo = pygame.transform.scale(self.logo, (int(self.logo_rect.width*C.BG_MULTI),
                                                       int(self.logo_rect.height*C.BG_MULTI)))

        self.background = setup.GRAPHICS['bg']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * C.BG_MULTI),
                                                                   int(self.background_rect.height * C.BG_MULTI)))
        self.viewport = setup.SCREEN.get_rect()

        self.match = setup.GRAPHICS['match']
        self.match_rect = self.match.get_rect()
        self.match = pygame.transform.scale(self.match, (int(self.match_rect.width * C.MATCH_PAGE_MULTI),
                                                   int(self.match_rect.height * C.MATCH_PAGE_MULTI)))

    def setup_cursor(self):
        self.cursor = pygame.sprite.Sprite()
        self.cursor.image = tools.get_image(setup.GRAPHICS['stuff_pixel'], 0, 0, 64, 28, (0, 0, 0), C.BG_MULTI*0.75)
        rect = self.cursor.image.get_rect()
        rect.x, rect.y = (300, 500)
        self.cursor.rect = rect
        self.cursor.state = '1P'

    def update_cursor(self, keys):
        if keys[pygame.K_UP]:
            self.cursor.state = '1P'
            self.cursor.rect.y = 500
        elif keys[pygame.K_DOWN]:
            self.cursor.state = '2P'
            self.cursor.rect.y = 550
        elif keys[pygame.K_RETURN]:
            if self.cursor.state == '1P':
                self.next = 'load_screen_1'
                self.finished = True
            elif self.cursor.state == '2P':
                self.start_match = 1

    def update_match(self, surface, keys):
        if self.start_match == 1:
            if keys[pygame.K_q]:
                self.start_match = 0
                self.a = 1
                return

            surface.blit(self.match, (260, 440))
            self.current_time = pygame.time.get_ticks()
            if self.timer == 0:
                self.timer = self.current_time
            elif self.current_time - self.timer > 150:
                self.frame_index += 1
                self.frame_index %= 4
                self.timer = self.current_time
            self.image = self.frames[self.frame_index]
            surface.blit(self.image, (635, 535))

            self.data = self.send_data()

            if self.data == "wait":
                self.ready = 0

            if self.data == "ready":
                self.ready = 1
                self.start_match = 0

            if self.ready == 1:
                self.next = 'load_screen_2'
                self.finished = True

    def loadingIcon_frame(self, frame_rects):
        sheet = setup.GRAPHICS['loading']
        for frame_rect in frame_rects:
            self.frames.append(tools.get_image(sheet, *frame_rect, (255, 255, 255), C.ICON_MULTI))

    def update(self, surface, keys, timer=None, coin_number=None, result=None, net=None):
        self.net = net
        surface.blit(self.background, self.viewport)
        surface.blit(self.logo, (200, 60))

        x = self.start_match
        self.update_cursor(keys)
        surface.blit(self.cursor.image, self.cursor.rect)

        self.info.update()
        self.info.draw(surface)
        if x:
            self.update_match(surface, keys)

    def send_data(self):
        data = 'u b'
        reply = self.net.send(data)
        return reply