import pygame
from .. import setup, tools
from .. import constants as C
import json
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.face_right = True
        self.frame_index = 0
        self.load_data()
        self.setup_states()
        self.setup_velocities()
        self.setup_timers()
        self.load_images()

    def load_data(self):
        file_name = self.name + '.json'
        file_path = os.path.join('source/data/player', file_name)
        with open(file_path) as f:
            self.player_data = json.load(f)

    def setup_states(self):
        self.state = 'walk'
        self.face_right = True
        self.dead = False

    def setup_velocities(self):
        speed = self.player_data['speed']
        self.x_vel = 0
        self.y_vel = 0

        self.max_walk_vel = speed['max_walk_speed']
        self.max_run_vel = speed['max_run_speed']
        self.max_y_vel = speed['max_y_velocity']
        self.jump_vel = speed['jump_velocity']
        self.walk_accel = speed['walk_accel']
        self.run_accel = speed['run_accel']
        self.turn_accel = speed['turn_accel']
        self.gravity = C.GRAVITY
        self.anti_gravity = C.ANTI_GRAVITY

        self.max_x_vel = self.max_walk_vel
        self.x_accel = self.walk_accel

    def setup_timers(self):
        self.walking_timer = 0
        self.transition_timer = 0

    def load_images(self):
        sheet = setup.GRAPHICS[self.name]
        frame_rects = self.player_data['image_frames']

        self.right_normal_frames = []
        self.left_normal_frames = []

        self.normal_frames = [self.right_normal_frames, self.left_normal_frames]

        self.all_frames = [
            self.right_normal_frames,
            self.left_normal_frames,
        ]

        self.right_frames = self.right_normal_frames
        self.left_frames = self.left_normal_frames

        for group, group_frame_rects in frame_rects.items():
            for frame_rect in group_frame_rects:
                right_image = tools.get_image(sheet, frame_rect['x'], frame_rect['y'], frame_rect['width'],
                                              frame_rect['height'], (255, 255, 255), C.PLAYER_MULTI)
                left_image = pygame.transform.flip(right_image, True, False)
                if group == 'right_normal':
                    self.right_normal_frames.append(right_image)
                    self.left_normal_frames.append(left_image)

        self.frame_index = 0
        self.frames = self.right_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()

    def update(self, keys, on_ground, on_cloud, on_cloud1):
        self.current_time = pygame.time.get_ticks()
        self.handle_states(keys, on_ground, on_cloud, on_cloud1)

    def handle_states(self, keys, on_ground, on_cloud, on_cloud1):
        if self.state == 'stand':
            self.stand(keys, on_ground, on_cloud, on_cloud1)
        elif self.state == 'walk':
            self.walk(keys, on_ground, on_cloud, on_cloud1)
        elif self.state == 'jump':
            self.jump(keys)
        elif self.state == 'fall':
            self.fall(keys, on_ground, on_cloud, on_cloud1)

        if self.face_right:
            self.image = self.right_frames[self.frame_index]
        else:
            self.image = self.left_frames[self.frame_index]

    def stand(self, keys, on_ground, on_cloud, on_cloud1):
        self.frame_index = 0
        self.x_vel = 0
        if on_ground:
            self.y_vel = 0

        if not on_ground:
            if not on_cloud1:
                self.y_vel = 1

        if keys[pygame.K_RIGHT]:
            self.face_right = True
            self.state = 'walk'
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            self.state = 'walk'
        elif keys[pygame.K_SPACE]:
            self.state = 'jump'
            self.y_vel = self.jump_vel

    def walk(self, keys, on_ground, on_cloud, on_cloud1):
        self.max_x_vel = self.max_walk_vel
        self.x_accel = self.walk_accel

        if self.current_time - self.walking_timer > 100:
            if self.frame_index < 3:
                self.frame_index += 1
            else:
                self.frame_index = 1
            self.walking_timer = self.current_time

        if not on_ground:
            if on_cloud:
                self.y_vel = 1
                if on_cloud1:
                    self.y_vel = 0
            else:
                self.state = 'fall'

        if keys[pygame.K_SPACE]:
            self.state = 'jump'
            self.y_vel = self.jump_vel

        if keys[pygame.K_RIGHT]:
            self.face_right = True
            if self.x_vel < 0:
                self.frame_index = 4
                self.x_accel = self.turn_accel
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            if self.x_vel > 0:
                self.frame_index = 4
                self.x_accel = self.turn_accel
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)
        else:
            if self.face_right:
                self.x_vel -= self.x_accel*1.5
                if self.x_vel < 0:
                    self.x_vel = 0
                    self.state = 'stand'
            else:
                self.x_vel += self.x_accel*1.5
                if self.x_vel > 0:
                    self.x_vel = 0
                    self.state = 'stand'

    def jump(self, keys):
        self.frame_index = 3
        self.y_vel += self.anti_gravity

        if keys[pygame.K_RIGHT]:
            self.face_right = True
            if self.x_vel < 0:
                self.frame_index = 4
                self.x_accel = self.turn_accel
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            if self.x_vel > 0:
                self.frame_index = 4
                self.x_accel = self.turn_accel
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)
        else:
            if self.face_right:
                self.x_vel -= self.x_accel*1.5
                if self.x_vel < 0:
                    self.x_vel = 0

            else:
                self.x_vel += self.x_accel*1.5
                if self.x_vel > 0:
                    self.x_vel = 0

        if self.y_vel >= 0:
            self.state = 'fall'

    def fall(self, keys, on_ground, on_cloud, on_cloud1):
        self.y_vel = self.calc_vel(self.y_vel, self.gravity, self.max_y_vel)

        if on_cloud:
            self.state = 'walk'

        if keys[pygame.K_RIGHT]:
            self.face_right = True
            if self.x_vel < 0:
                self.frame_index = 4
                self.x_accel = self.turn_accel
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, True)
        elif keys[pygame.K_LEFT]:
            self.face_right = False
            if self.x_vel > 0:
                self.frame_index = 4
                self.x_accel = self.turn_accel
            self.x_vel = self.calc_vel(self.x_vel, self.x_accel, self.max_x_vel, False)
        else:
            if self.face_right:
                self.x_vel -= self.x_accel*1.5
                if self.x_vel < 0:
                    self.x_vel = 0
            else:
                self.x_vel += self.x_accel*1.5
                if self.x_vel > 0:
                    self.x_vel = 0

        if self.rect.y > C.GROUND_HEIGHT:
            self.rect.y = C.GROUND_HEIGHT
            self.y_vel = 0
            self.state = 'walk'

    def calc_vel(self, vel, accel, max_vel, is_positive=True):
        if is_positive:
            return min(vel + accel, max_vel)
        else:
            return max(vel - accel, -max_vel)

    def as_rival(self, frame_index, face_right):
        if face_right:
            self.image = self.right_frames[frame_index]
        else:
            self.image = self.left_frames[frame_index]


