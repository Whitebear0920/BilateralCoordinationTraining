import pygame.draw
import math

import config
from .settings import *

class Game2Scene:
    def __init__(self, screen):
        self.screen = screen
        self.level = 1

    def main(self):
        pass

    def draw(self):
        self.screen.fill((52,52,52))
        self.draw_ui()

    def draw_ui(self):
        def rotation_fun(x, y, angle):
            radian = angle * math.pi / 180
            new_x = x * math.cos(radian) + y * math.sin(radian)
            new_y = -1* x * math.sin(radian) + y * math.cos(radian)
            return (new_x, new_y)

        # Basic Layout
        # 內外圓
        pygame.draw.circle(self.screen, "WHITE", (circle_center_x, circle_center_y), inner_circle_radius, 2)
        pygame.draw.circle(self.screen, "WHITE", (circle_center_x, circle_center_y), outer_circle_radius, 5)
        # 內外圓相連線
        start_pos = (outer_circle_radius, 0)
        end_pos = (inner_circle_radius, 0)
        turn_angle = 180 / (level_dict[self.level]-1)
        for i in range(level_dict[self.level]):
            draw_start_pos = (start_pos[0] + circle_center_x, start_pos[1] + circle_center_y)
            draw_end_pos = (end_pos[0] + circle_center_x, end_pos[1] + circle_center_y)
            pygame.draw.line(self.screen, "WHITE", draw_start_pos, draw_end_pos, 5)
            start_pos = rotation_fun(*start_pos, turn_angle)
            end_pos = rotation_fun(*end_pos, turn_angle)
        # 分數&關卡提示



    def update(self):
        self.screen.fill((52,52,52))
        pass

    def handle_event(self, event):
        pass