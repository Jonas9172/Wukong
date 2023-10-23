import random

from ..components import info
from .. import setup
from .. import constants as C
import pygame
from ..components import player, cloud, cloud0, cloud1, portal, coin


class Level1:
    def __init__(self, mode="single"):
        self.current_time = 0
        self.timer = 0
        self.lucky_number = 3
        self.random_n = None
        if mode == "online":
            self.mode = 2

        if mode == "single":
            self.mode = 1
            self.last_cloud_x = random.randint(0, 936)# random.randint(0, 936)

        self.x = 0
        self.y = 0
        self.create_cloud1()
        self.create_portal(20, 75)

    def initial_position(self, player):
        player.rect.x = 200
        player.rect.y = 750

    def create_cloud1(self):
        cloud.cloud1_list.append(cloud1.Cloud1(0, 100))

    def create_cloud0(self):
        if self.mode == 2:
            self.x = int(self.random_n.split(",")[0])
            self.y = int(self.random_n.split(",")[1])

        if self.mode == 1:
            if self.last_cloud_x <= 100:
                self.x = random.randint(self.last_cloud_x + 100, self.last_cloud_x + 300)
            elif self.last_cloud_x <= 300:
                if random.randint(0, 1) == 0:
                    self.x = random.randint(0, self.last_cloud_x - 100)
                else:
                    self.x = random.randint(self.last_cloud_x + 100, self.last_cloud_x + 300)
            elif self.last_cloud_x >= 636:
                self.x = random.randint(self.last_cloud_x - 300, self.last_cloud_x - 100)
            elif self.last_cloud_x >= 436:
                if random.randint(0, 1) == 0:
                    self.x = random.randint(self.last_cloud_x + 100, 736)
                else:
                    self.x = random.randint(self.last_cloud_x - 300, self.last_cloud_x - 100)
            else:
                if random.randint(0, 1) == 0:
                    self.x = random.randint(self.last_cloud_x + 100, self.last_cloud_x + 300)
                else:
                    self.x = random.randint(self.last_cloud_x - 300, self.last_cloud_x - 100)

            self.last_cloud_x = self.x
            self.y = random.randint(-50, -40)

        cloud.cloud0_list.append(cloud0.Cloud0(self.x, self.y))

    def create_portal(self, x, y):
        portal.portal_list.append(portal.Portal(x, y))

    def create_coin(self):
        coin.coin_list.append(coin.FlashingCoin(self.x + 24, self.y - 19, 1.1))

    def update(self, game_window=None, random_n=None):
        self.random_n = random_n
        self.create_cloud0()

        if self.lucky_number == len(cloud.cloud0_list):
            self.create_coin()
            self.lucky_number += 3
