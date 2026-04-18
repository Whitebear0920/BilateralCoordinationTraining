import pygame
import math
from .settings import *


class LightSword(pygame.sprite.Sprite):
    def __init__(self, image, angle_fun, area, color):
        super().__init__()
        # 1. 基礎設定
        self.original_image = image  # 保留原始圖片用於旋轉
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.angle_info_api = angle_fun

        self.area = area
        self.color = color

        self.lerp_factor = 0.5

        # 2. 軌道參數
        self.pivot = pygame.Vector2(circle_center_x, circle_center_y)
        self.radius = inner_circle_radius

        # 3. 自動移動參數
        if area == "LEFT":
            self.angle = self.angle_info_api()["right_finger_angle"]
        elif area == "RIGHT":
            self.angle = self.angle_info_api()["left_finger_angle"]


    def update(self):
        # A. 取得目標角度 (來自 Mediapipe)
        data = self.angle_info_api()
        target_angle = data["left_finger_angle"] + 180  if self.area == "RIGHT" else data["right_finger_angle"] + 180
        print(target_angle)
        # B. 計算最短路徑的角度差 (處理 0/360 度跨越問題)
        # 這是為了確保從 359 度移動到 1 度時，是前進 2 度而不是後退 358 度
        diff = (target_angle - self.angle + 180) % 360 - 180

        # C. 應用平滑公式：當前角度 += 差距 * 平滑係數
        self.angle += diff * self.lerp_factor

        # 確保角度保持在 0-360 之間
        if self.angle <= 180:
            self.angle = 180
        elif self.angle >= 360:
            self.angle = 360

        offset = pygame.Vector2(-self.radius, 0).rotate(self.angle - 180)
        new_pos = self.pivot + offset
        rotation_angle = -(self.angle - 180 - 90)
        self.image = pygame.transform.rotozoom(self.original_image, rotation_angle, 1)
        self.rect = self.image.get_rect(center=new_pos)
        self.mask = pygame.mask.from_surface(self.image)