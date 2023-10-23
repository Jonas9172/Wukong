import pygame
from .. import constants as C
from . import coin
from .. import tools

pygame.font.init()


class Info:
    def __init__(self, state):
        self.state = state
        self.create_state_labels()
        self.flash_coin = coin.FlashingCoin(900, 20, 1.5)
        self.timer = 0
        self.coin_number = 0
        self.result = None

    def create_state_labels(self):
        self.state_labels = []
        if self.state == 'main_menu':
            self.state_labels.append((self.create_label('1 PLAYER GAME'), (400, 500)))
            self.state_labels.append((self.create_label('2 PLAYER GAME'), (400, 555)))
            self.state_labels.append((self.create_label('(FIND MATCH)', 15), (610, 560)))
        elif self.state == 'load_screen_1':
            self.state_labels.append((self.create_label('1 PLAYER GAME', 30), (375, 500)))
        elif self.state == 'load_screen_2':
            self.state_labels.append((self.create_label('2 PLAYER GAME', 30), (375, 555)))
        elif self.state == 'results':
            self.state_labels.append((self.create_label('Press Q to continue'), (380, 650)))

    def create_label(self, label, size=25, width_scale=1.25, height_scale=1):
        font = pygame.font.Font(C.FONT0, size)
        label_image = font.render(label, 1, (0, 0, 0))

        return label_image

    def update(self, timer=None, coin_number=None, result=None):
        self.flash_coin.update()
        if self.state == 'results':
            if self.timer == 0:
                self.timer = timer
        else:
            self.timer = timer

        if coin_number:
            self.coin_number = coin_number

        if result:
            if result == 'w':
                self.result = 'You win !'
            elif result == 'l':
                self.result = 'You lose.'

    def draw(self, surface, star_x=None, star_y=None):

        if star_x:
            self.flash_coin.rect.x = star_x
            self.flash_coin.rect.y = star_y

        if self.state == 'game_screen_1' or self.state == 'game_screen_2':
            surface.blit(self.create_label('Time: ' + str(self.timer) + 's'), (700, 20))
        elif self.state == 'results':
            time_score = int(1000 / self.timer)
            total_score = time_score + self.coin_number

            surface.blit(self.create_label(self.result, 60), (380, 500))

            surface.blit(self.create_label('Your time: ' + str(self.timer) + 's              ' + str(time_score)),
                         (320, 220))
            surface.blit(self.create_label('X' + str(self.coin_number) + '                        ' + str(self.coin_number)),
                         (self.flash_coin.rect.x + 30, self.flash_coin.rect.y))
            surface.blit(self.create_label('Score'), (600, 180))
            surface.blit(self.create_label('Score:  ' + str(total_score), 40), (390, 360))

        for label in self.state_labels:
            surface.blit(label[0], label[1])

        surface.blit(self.flash_coin.image, self.flash_coin.rect)
