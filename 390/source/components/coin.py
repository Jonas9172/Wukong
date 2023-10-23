import json
import os

import pygame
from .. import tools, setup
from .. import constants as C

coin_list = []


class FlashingCoin(pygame.sprite.Sprite):
    def __init__(self, x, y, n):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []
        self.frame_index = 0
        frame_rects = [(65, 0, 14, 14), (80, 0, 14, 14), (95, 0, 14, 14), (80, 0, 14, 14)]
        self.load_frame(frame_rects, n)
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = 14
        self.height = 14
        self.timer = 0
        self.hitted = False
        self.picture_count = 0
        self.image_index = 0
        self.disappear_picture_num = 2
        self.disappear_picture_list = []
        self.load_data()
        self.load_images()
        self.h = False
        self.a = False  # getScore

    def move(self, level):
        if level == 3:
            self.rect.x -= 1
        else:
            self.rect.y += 1

    def display(self, screen):
        if self.hitted:
            self.h = True

        if self.h and self.image_index < self.disappear_picture_num:
            screen.blit(self.disappear_picture_list[self.image_index], (self.rect.x, self.rect.y))
            self.picture_count += 1
            if self.picture_count == 15:
                self.picture_count = 0
                self.image_index += 1
        elif self.image_index < self.disappear_picture_num:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.h and self.image_index >= self.disappear_picture_num:
            del_coin(self)

    def load_data(self):
        file_name = 'stuff_pixel.json'
        file_path = os.path.join('source/data/components', file_name)
        with open(file_path) as f:
            self.coin_data = json.load(f)

    def load_images(self):
        sheet = setup.GRAPHICS['stuff_pixel']
        frame_rects = self.coin_data['image_frames']

        for group, group_frame_rects in frame_rects.items():
            for frame_rect in group_frame_rects:
                image = tools.get_image(sheet, frame_rect['x'], frame_rect['y'], frame_rect['width'],
                                        frame_rect['height'], (0, 0, 0), C.COIN_MULTI)
                if group == 'coin_disappear':
                    self.disappear_picture_list.append(image)

    def load_frame(self, frame_rects, n):
        sheet = setup.GRAPHICS['stuff_pixel']
        for frame_rect in frame_rects:
            self.frames.append(tools.get_image(sheet, *frame_rect, (0, 0, 0), C.BG_MULTI * n))

    def update(self):
        self.current_time = pygame.time.get_ticks()
        frame_durations = [375, 125, 125, 125]

        if self.timer == 0:
            self.timer = self.current_time
        elif self.current_time - self.timer > frame_durations[self.frame_index]:
            self.frame_index += 1
            self.frame_index %= 4
            self.timer = self.current_time

        self.image = self.frames[self.frame_index]


def del_coin(coin):
    global coin_list
    if coin in coin_list:
        coin_list.remove(coin)


def clear_coin():
    coin_list.clear()
