import pygame
import math
from common.assets_manager import AssetsManager
from .settings import *


class Marble(pygame.sprite.Sprite):
    def __init__(self, color, speed, num_lines, track_id):
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

        self.rect = self.image.get_rect()

        # 2. 計算位置與方向
        # 你的 UI 邏輯是 180 度平分，且從正左方 (-1, 0) 開始旋轉
        angle_step = 180 / (num_lines - 1) if num_lines > 1 else 0

        # 根據 track_id 計算旋轉向量 (排除最左 0 與最右 num_lines-1)
        self.direction = pygame.Vector2(-1, 0).rotate(track_id * angle_step)

        # 初始位置：在外圓邊界上
        self.center_pos = pygame.Vector2(circle_center_x, circle_center_y)
        self.current_pos = self.center_pos + self.direction * outer_circle_radius

        self.speed = speed
        self.track_id = track_id
        self.is_broken = False

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