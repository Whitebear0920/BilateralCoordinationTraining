import time
import math
import pygame


class HandAni:
    def __init__(self, image, mode, start_pos, period,
                 amplitude=70, radius=80):
        """
        image: pygame.Surface
        mode: 'VERTICAL', 'HORIZONTAL', 'CW', 'CCW'
        start_pos: (x, y)
        period: 完成一次循環所需秒數
        """

        self.image = image
        self.rect = image.get_rect(center=start_pos)

        self.origin = pygame.Vector2(self.rect.center)
        self.base_x, self.base_y = self.origin

        self.mode = mode
        self.period = period

        self.amplitude = amplitude
        self.radius = radius

        self.start_time = time.time()

        self.x = self.base_x
        self.y = self.base_y

        # ===== 方向計算 =====
        self.prev_x = self.x
        self.prev_y = self.y
        self.angle = 0

    def reset(self):
        self.start_time = time.time()
        self.prev_x = self.x
        self.prev_y = self.y

    def update(self):
        t = time.time() - self.start_time

        # 正規化到 0 ~ 2π
        omega = 2 * math.pi / self.period
        phase = omega * t

        if self.mode == "VERTICAL":
            self.x = self.base_x
            self.y = self.base_y + self.amplitude * math.sin(phase)

        elif self.mode == "HORIZONTAL":
            self.x = self.base_x + self.amplitude * math.sin(phase)
            self.y = self.base_y

        elif self.mode == "CCW":
            self.x = self.base_x - self.radius * math.cos(phase)
            self.y = self.base_y + self.radius * math.sin(phase)

        elif self.mode == "CW":
            self.x = self.base_x + self.radius * math.cos(phase)
            self.y = self.base_y + self.radius * math.sin(phase)

        # ===== 計算移動方向 =====
        dx = self.x - self.prev_x
        dy = self.y - self.prev_y

        if dx != 0 or dy != 0:
            self.angle = math.degrees(math.atan2(dy, dx))

        self.prev_x = self.x
        self.prev_y = self.y

        self.rect.center = (self.x, self.y)

    def draw(self, screen):

        # +90 是因為圖片通常是「朝上」
        rotated = pygame.transform.rotate(self.image, -self.angle + 90)

        rect = rotated.get_rect(center=self.rect.center)

        screen.blit(rotated, rect)