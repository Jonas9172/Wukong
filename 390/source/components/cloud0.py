import json
import os
from .. import constants as C
from . import cloud
import random

from .. import setup, tools


class Cloud0(cloud.Cloud):
    def __init__(self, x, y):
        self.height = 28
        self.width = 64
        self.a = 0
        self.disappear_picture_list = []
        self.load_data()
        self.load_images()
        cloud.Cloud.__init__(self, 0, x, y, 3, self.disappear_picture_list)

    def move(self, level):

        if level == 3:
            self.x -= 1
        else:
            self.y += 1

    def load_data(self):
        file_name = 'stuff_pixel.json'
        file_path = os.path.join('source/data/components', file_name)
        with open(file_path) as f:
            self.cloud_data = json.load(f)

    def load_images(self):
        sheet = setup.GRAPHICS['stuff_pixel']
        frame_rects = self.cloud_data['image_frames']

        for group, group_frame_rects in frame_rects.items():
            for frame_rect in group_frame_rects:
                image = tools.get_image(sheet, frame_rect['x'], frame_rect['y'], frame_rect['width'],
                                        frame_rect['height'], (0, 0, 0), C.CLOUD_MULTI)
                if group == 'cloud0':
                    self.disappear_picture_list.append(image)
        self.image = self.disappear_picture_list[0]
