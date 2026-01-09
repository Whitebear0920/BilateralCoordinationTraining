import time
import math
import pygame
class HandAni:
    def __init__(self, image, mode, start_pos, period,
                 amplitude=280, radius=320):
        """
        image: pygame.Surface
        mode: 'VERTICAL', 'HORIZONTAL', 'CW', 'CCW'
        start_pos: (x, y)
        period: 完成一次循環所需秒數
        """
        self.image = image
        self.rect = image.get_rect(center=start_pos)
        self.origin = pygame.Vector2(self.rect.center)
        self.mode = mode
        self.base_x, self.base_y = self.origin
        self.period = period

        self.amplitude = amplitude
        self.radius = radius

        self.start_time = time.time()
        self.x = self.base_x
        self.y = self.base_y

    def reset(self):
        self.start_time = time.time()

    def update(self):
        t = time.time() - self.start_time

        # 正規化到 0 ~ 2π（一個完整週期）
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
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
