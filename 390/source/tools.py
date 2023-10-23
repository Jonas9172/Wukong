import os

import pygame
import time
from network import Network


class Game:
    # define a game
    def __init__(self, state_dict, start_state):
        self.timer_start = 0  # start timing from game_screen(state)
        self.timer_end = 0  # start timing from starting game
        self.timer = 0  # timer = timer_end - timer_start
        self.coin_number = 0
        self.result = None  # win or lose (result of online mode)
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.keys = pygame.key.get_pressed()
        self.state_dict = state_dict
        self.state = self.state_dict[start_state]

        self.net = None  # network
        self.left = 1  # 1 for

    # switch different states and update
    def update(self):
        if self.state.finished:
            next_state = self.state.next

            if next_state == 'results':
                self.coin_number = self.state.coin_number
                self.state.coin_number = 0

            self.state.finished = False
            self.state = self.state_dict[next_state]

            if next_state == 'main_menu':
                self.result = None
                self.coin_number = 0
                self.state.next = 'load_screen'
            if next_state == 'game_screen_2':
                self.state.a = 0
                self.timer_start = round(time.perf_counter(), 2)
            if next_state == 'game_screen_1':
                self.timer_start = round(time.perf_counter(), 2)

        self.timer_end = round(time.perf_counter(), 2)
        self.timer = round(self.timer_end - self.timer_start, 2)

        if self.state.next == 'load_screen':
            if self.state.start_match:
                self.left = 1
                if self.state.a:
                    self.net = Network()
                    self.state.a = 0
            if self.state.start_match == 0 and self.left and self.net:
                self.left = 0
                self.leave_q()

        if self.state.next == 'main_menu' and self.left and self.net:
            self.left = 0
            self.result = self.reach()
            self.leave()

        if self.left and self.net:
            self.state.update(surface=self.screen, keys=self.keys, timer=self.timer,
                              coin_number=self.coin_number, result=self.result, net=self.net)
        else:
            self.state.update(self.screen, self.keys, self.timer, self.coin_number, result=self.result)

    # return 'w' or 'l' after sending "reach" to server
    def reach(self):
        reach_request = "reach"
        return self.net.reach(reach_request)

    # send "leave" to server then disconnect
    def leave(self):
        leave_request = "leave"
        self.net.leave(leave_request)

    # send "l q" to server then disconnect when finding match
    def leave_q(self):
        leave_request = "l q"
        self.net.leave(leave_request)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.state.next == 'load_screen':
                        if self.state.start_match == 0 and self.left and self.net:
                            self.left = 0
                            self.leave_q()
                    if self.left and self.net:
                        self.leave()
                    pygame.display.quit()
                elif event.type == pygame.KEYDOWN:
                    self.keys = pygame.key.get_pressed()
                elif event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()

            self.update()
            pygame.display.update()
            self.clock.tick(60)  # 60 frames per second


def load_graphics(path, accept=('.png')):
    graphics = {}
    # Returns a list of the names of the files or folders contained in the specified folder
    for pic in os.listdir(path):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(path, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
            graphics[name] = img
    return graphics


def get_image(sheet, x, y, width, height, colorkey, scale):
    image = pygame.Surface((width, height))
    image.blit(sheet, (0, 0), (x, y, width, height))
    image.set_colorkey(colorkey)
    image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    return image
