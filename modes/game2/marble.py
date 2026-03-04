import pygame
import math
from common.assets_manager import AssetsManager
from .settings import *


class Marble(pygame.sprite.Sprite):
    def __init__(self, color, speed, angle_step, track_id, active = False):
        super().__init__()

        scale = (judge_circle_radius - inner_circle_radius) * 0.8

        # 1. 載入資源
        if color == "RED":
            self.image = AssetsManager.get_image("RED_MARBLE")
            self.image = pygame.transform.smoothscale(self.image, (scale, scale))
            self.image_broke = AssetsManager.get_image("RED_MARBLE_BROKE")
            self.image_broke = pygame.transform.smoothscale(self.image_broke, (scale, scale))
        elif color == "BLUE":
            self.image = AssetsManager.get_image("BLUE_MARBLE")
            self.image = pygame.transform.smoothscale(self.image, (scale, scale))
            self.image_broke = AssetsManager.get_image("BLUE_MARBLE_BROKE")
            self.image_broke = pygame.transform.smoothscale(self.image_broke, (scale, scale))

        self.rect = self.image.get_rect() # this is necessary

        self.angle_step = angle_step
        # 根據 track_id 計算旋轉向量 (排除最左 0 與最右 num_lines-1)
        self.direction = pygame.Vector2(-1, 0).rotate(track_id * self.angle_step)

        # 初始位置：在外圓邊界上
        self.center_pos = pygame.Vector2(circle_center_x, circle_center_y)
        self.current_pos = self.center_pos + self.direction * outer_circle_radius

        self.speed = speed
        self.track_id = track_id
        self.is_broken = False

        self.active = active

    def update(self):
        if not self.is_broken:
            # 往中心點移動：當前位置沿著方向向量的反方向前進
            self.current_pos -= self.direction * self.speed

            # 更新 Sprite 的 rect 位置 (置中)
            self.rect.center = (int(self.current_pos.x), int(self.current_pos.y))

            # 判斷是否到達中心 (或低於內圓半徑)，到達後可以自動消失
            dist_to_center = self.current_pos.distance_to(self.center_pos)
            if dist_to_center < inner_circle_radius:
                self.current_pos = self.center_pos + self.direction * outer_circle_radius

    def update_offset(self, new_angle_step=None, new_speed=None, new_track_id=None):
        if new_angle_step is not None:
            self.angle_step = new_angle_step

        if new_speed is not None:
            self.speed = new_speed

        if new_track_id is not None:
            self.track_id = new_track_id

    def active_sprite(self):
        self.active = True

    def unactive_sprite(self):
        self.active = False