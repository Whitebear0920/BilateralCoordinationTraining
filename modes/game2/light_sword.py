import pygame
import math
from .settings import *


class LightSword(pygame.sprite.Sprite):
    def __init__(self, image, start_revers = False):
        super().__init__()
        # 1. 基礎設定
        self.original_image = image  # 保留原始圖片用於旋轉
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()

        # 2. 軌道參數
        self.pivot = pygame.Vector2(circle_center_x, circle_center_y)
        self.radius = inner_circle_radius

        # 3. 自動移動參數
        self.move_speed = 2.0  # 每次更新移動的角度
        if start_revers:
            self.angle = 360.0  # 起始角度 (180度在左邊)
            self.direction = -1  # 1 為順時針，-1 為逆時針
        else:
            self.angle = 180.0  # 起始角度 (180度在左邊)
            self.direction = 1  # 1 為順時針，-1 為逆時針

    def update(self):
        # A. 更新角度 (在 180 到 360 度之間來回)
        self.angle += self.move_speed * self.direction

        if self.angle >= 360:
            self.angle = 360
            self.direction = -1  # 撞到右邊，反轉
        elif self.angle <= 180:
            self.angle = 180
            self.direction = 1  # 撞到左邊，反轉

        # B. 計算位置 (向量魔法)
        # 建立一個長度為半徑的水平向量，然後旋轉它
        # Pygame 的 rotate 角度：正值為順時針
        offset = pygame.Vector2(-self.radius, 0).rotate(self.angle - 180)
        new_pos = self.pivot + offset

        # C. 讓光劍「指向」圓心外側 (旋轉圖片)
        # 我們計算光劍應該旋轉的角度，使其垂直於圓弧
        # 這裡的旋轉角度剛好會跟我們的移動角度連動
        rotation_angle = -(self.angle - 180 - 90)  # 修正偏移量使其垂直
        self.image = pygame.transform.rotozoom(self.original_image, rotation_angle, 1)

        # D. 同步位置 (更新 rect)
        # 記住：旋轉後的圖片 rect 會變大，所以一定要重新取得 rect 並對齊中心
        self.rect = self.image.get_rect(center=new_pos)