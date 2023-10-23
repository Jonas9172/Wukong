import json
import os

from . import base
from .. import setup, tools
from .. import constants as C

portal_list = []


class Portal(base.Base):
    def __init__(self, x, y):
        base.Base.__init__(self, x, y)
        self.height = 30
        self.width = 46
        self.picture_list = []
        self.load_data()
        self.load_images()

    def display(self, screen):
        screen.blit(self.picture_list[0], (self.x, self.y))

    def load_data(self):
        file_name = 'stuff_pixel.json'
        file_path = os.path.join('source/data/components', file_name)
        with open(file_path) as f:
            self.portal_data = json.load(f)

    def load_images(self):
        sheet = setup.GRAPHICS['stuff_pixel']
        frame_rects = self.portal_data['image_frames']

        for group, group_frame_rects in frame_rects.items():
            for frame_rect in group_frame_rects:
                image = tools.get_image(sheet, frame_rect['x'], frame_rect['y'], frame_rect['width'],
                                        frame_rect['height'], (0, 0, 0), C.CLOUD_MULTI)
                if group == 'portal':
                    self.picture_list.append(image)
        self.image = self.picture_list[0]


def clear_portal():
    portal_list.clear()