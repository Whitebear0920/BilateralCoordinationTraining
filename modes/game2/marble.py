import pygame
from common import AssetsManager
from .settings import *

class marble(pygame.sprite.Sprite):
    def __init__(self, color, speed, angle_step, track_id):
        super().__init__()

        if color == "RED":
            self.image = AssetsManager.get_image("red_marble.png")
            self.image_broke = AssetsManager.get_image("red_marble_broke.png")
        elif color == "BLUE":
            self.image = AssetsManager.get_image("blue_marble.png")
            self.image_broke = AssetsManager.get_image("blue_marble_broke.png")
        self.rect = self.image.get_rect()

        self.track_pos = level_dict
        self.speed = speed

    def update(self):
        pass