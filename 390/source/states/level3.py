import random

from . import game_screen_1
from ..components import info
from .. import setup
from .. import constants as C
import pygame
from ..components import player, cloud, cloud0, cloud1, portal


class Level3:
    def __init__(self, mode="single"):
        self.random_n = None
        if mode == "online":
            self.mode = 2

        if mode == "single":
            self.mode = 1
            self.last_cloud_y = random.randint(670, 700)# random.randint(0, 936)

        self.x = 0
        self.y = 0
        self.create_cloud1()

        self.create_portal(4920, 375)

    def initial_position(self, player):
        player.rect.x = 50
        player.rect.y = 630
        player.state = "fall"

    def create_cloud1(self):
        cloud.cloud1_list.append(cloud1.Cloud1(0, 700))
        cloud.cloud1_list.append(cloud1.Cloud1(4872, 400))

    def create_cloud0(self, game_window):
        if self.mode == 2:
            self.x = game_window.x + int(self.random_n.split(",")[0])
            self.y = int(self.random_n.split(",")[1])

        if self.mode == 1:
            if self.last_cloud_y >= 300:
                if random.randint(0, 5) == 0:
                    self.y = random.randint(self.last_cloud_y, 700)
                else:
                    self.y = random.randint(self.last_cloud_y - 100, self.last_cloud_y - 50)
            else:
                if random.randint(0, 5) == 0:
                    self.y = random.randint(200, self.last_cloud_y)
                else:
                    self.y = random.randint(self.last_cloud_y, 700)

            self.last_cloud_y = self.y
            self.x = random.randint(game_window.x + 1050, game_window.x + 1060)
        cloud.cloud0_list.append(cloud0.Cloud0(self.x, self.y))

    def create_portal(self, x, y):
        portal.portal_list.append(portal.Portal(x, y))

    def update(self, game_window=None, random_n=None):
        self.random_n = random_n
        self.create_cloud0(game_window)
