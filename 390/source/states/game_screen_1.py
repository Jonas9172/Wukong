
from ..components import info
from .. import setup
from .. import constants as C
import pygame
from ..components import player, cloud, portal, coin
from . import level1, level2, level3


class GameScreen:
    def __init__(self):

        self.pass_level = 1
        self.setup_background()
        self.setup_player()
        self.coin_number = 0
        self.level = level1.Level1()
        self.level.initial_position(self.player)
        self.finished = False
        self.current_time = 0
        self.timer = 0
        self.info = info.Info('game_screen_1')
        self.next = 'results'

        self.on_cloud = False
        self.on_ground = True
        self.on_cloud0 = False
        self.on_cloud1 = False
        self.in_portal = False
        self.top = -450
        self.start_x = 0
        self.next_cloud = False
        self.first_cloud = True

    def update_level_state(self):
        if self.pass_level == 2 and self.in_portal:
            self.level = level2.Level2()
            self.level.initial_position(self.player)
            self.in_portal = False

        if self.pass_level == 3 and self.in_portal:
            self.level = level3.Level3()
            self.level.initial_position(self.player)
            self.setup_background()
            self.in_portal = False

        if self.pass_level == 4 and self.in_portal:
            self.pass_level = 1
            self.level = level1.Level1()
            self.level.initial_position(self.player)
            self.setup_background()
            self.on_ground = True
            self.in_portal = False
            self.start_x = 0
            self.finished = True

    # 设置游戏界面背景
    def setup_background(self):
        if not self.pass_level == 3:
            self.background = setup.GRAPHICS['backgroud']
        else:
            self.background = setup.GRAPHICS['backgroud_']
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width * C.BG_MULTI),
                                                                   int(rect.height * C.BG_MULTI)))
        self.background_rect = self.background.get_rect()
        self.game_ground = pygame.Surface((self.background_rect.width, self.background_rect.height))
        self.game_window = setup.SCREEN.get_rect()

    def update_background(self):

        self.top += 1
        if self.top >= 800:
            self.top = -450

    # 创建player
    def setup_player(self):
        self.player = player.Player('wukong_pixel')

    # 更新player的位置
    def update_player_position(self):
        self.player.rect.x += self.player.x_vel
        if self.pass_level == 3:
            if self.on_cloud0 and not self.on_cloud1:
                self.player.rect.x -= 1

        if not self.pass_level == 3:
            if self.player.rect.x < 0:
                self.player.rect.x = 0
            if self.player.rect.right > C.SCREEN_W:
                self.player.rect.right = C.SCREEN_W
            if self.player.rect.y > 755:
                self.player.rect.y = 755
        else:
            if self.player.rect.x < self.start_x:
                self.player.rect.x = self.start_x
            if self.player.rect.right > 5000:
                self.player.rect.right = 5000
            if self.player.rect.y > 755:
                self.player.rect.y = 755

        self.player.rect.y += self.player.y_vel
        if self.pass_level == 3 and self.on_cloud0:
            self.player.rect.y -= 1

    def update_game_window(self):
        third = self.game_window.x + self.game_window.width / 3
        if self.player.x_vel > 0 and self.player.rect.centerx > third and self.game_window.right < 5000:
            self.game_window.x += self.player.x_vel
            self.start_x = self.game_window.x

    def on_clouds(self, the_cloud):
        self.on_cloud = False
        if self.player.rect.x < the_cloud.x + the_cloud.width and self.player.rect.x + 28 > the_cloud.x:
            if the_cloud.y < self.player.rect.y + 45 and the_cloud.y - 1 > self.player_y + 15:
                self.on_cloud = True
                if the_cloud.cloud_type == 1:
                    self.on_cloud1 = True

    def in_the_portal(self, portal_0):
        self.in_portal = False
        if self.player.rect.x < portal_0.x + portal_0.width and self.player.rect.x + 28 > portal_0.x:
            if portal_0.y < self.player.rect.y + 45 and portal_0.y - 1 > self.player_y + 15:
                self.in_portal = True

    def coin_gotten(self, coin_0):
        coin_0.hitted = False
        if self.player.rect.x < coin_0.rect.x + coin_0.width + 3 and self.player.rect.x + coin_0.height + 3 > coin_0.rect.x:
            if coin_0.rect.y < self.player.rect.y + 45 and coin_0.rect.y + coin_0.height > self.player_y:
                coin_0.hitted = True

    def update(self, surface, keys, timer, coin_number, result):
        if self.in_portal:
            self.pass_level += 1

            cloud.clear_cloud()
            coin.clear_coin()
            portal.clear_portal()

        self.update_level_state()
        # update info and player and background
        self.info.update(timer, self.coin_number)

        self.player.update(keys, self.on_ground, self.on_cloud0, self.on_cloud1)
        self.player_x = self.player.rect.x
        self.player_y = self.player.rect.y
        self.update_player_position()

        self.on_cloud0 = False
        self.on_cloud1 = False

        self.update_background()
        if self.pass_level == 3:
            self.update_game_window()

        # draw info and player and background
        self.draw()

        if not self.pass_level == 3 and not self.pass_level == 4:
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.timer >= 1200:
                self.level.update()
                self.timer = self.current_time
        elif self.pass_level == 3:
            if self.next_cloud or self.first_cloud:
                self.first_cloud = False
                self.level.update(self.game_window)
                self.next_cloud = False

        if cloud.cloud1_list:
            for cloud_1 in cloud.cloud1_list:
                self.update_cloud1_display(cloud_1)
                self.on_clouds(cloud_1)
                if self.on_cloud:
                    self.on_cloud0 = True
                    self.on_ground = False

        if portal.portal_list:
            for portal_0 in portal.portal_list:
                self.update_portal_display(portal_0)
                self.in_the_portal(portal_0)

        if cloud.cloud0_list:
            for cloud_0 in cloud.cloud0_list:
                self.update_cloud0_display_move(cloud_0)
                self.on_clouds(cloud_0)
                if cloud_0.x <= 800 + self.game_window.x:
                    cloud_0.a += 1
                    if cloud_0.a == 1:
                        self.next_cloud = True

                if self.on_cloud:
                    self.on_cloud0 = True
                    self.on_ground = False

        if coin.coin_list:
            for coin_0 in coin.coin_list:
                coin_0.update()
                self.update_coin_display_move(coin_0)
                self.coin_gotten(coin_0)
                if coin_0.hitted and not coin_0.a:
                    self.coin_number += 1
                    coin_0.a = True

        self.score_coin()
        self.draw_surface(surface)

    def update_cloud0_display_move(self, cloud0s):
        cloud0s.move(self.pass_level)
        cloud0s.display(self.game_ground)

    def update_cloud1_display(self, cloud1s):
        cloud1s.display(self.game_ground)

    def update_portal_display(self, portal_0):
        portal_0.display(self.game_ground)

    def update_coin_display_move(self, coins):
        coins.move(self.pass_level)
        coins.display(self.game_ground)

    def score_coin(self):
        font = pygame.font.Font(C.FONT0, 20)
        self.score = font.render("X" + str(self.coin_number), 1, (0, 0, 0))

    def draw(self):

        if not self.pass_level == 3:
            self.game_ground.blit(self.background, (0, self.top))
            self.game_ground.blit(self.background, (0, self.top - 1250))
        else:
            self.game_ground.blit(self.background, self.game_window, self.game_window)
        self.game_ground.blit(self.player.image, self.player.rect)

    def draw_surface(self, surface):
        if not self.pass_level == 3:
            surface.blit(self.game_ground, (0, 0))
        else:
            surface.blit(self.game_ground, (0, 0), self.game_window)
        surface.blit(self.score, (935, 24))
        self.info.draw(surface)

