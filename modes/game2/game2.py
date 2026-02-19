import pygame.draw
import math
import config
from common import AssetsManager
from common import Button
from .score_manager import ScoreManager
from .time_manager import TimeManager
from .settings import *

class Game2Scene:
    def __init__(self, screen):
        self.screen = screen
        self.level = 1
        self.score_manager = ScoreManager()

        self.time_manager = TimeManager()
        self.time_manager.start_timer()

        self.font = AssetsManager.get_font("main")
        self.draw_ui()



    def main(self):
        pass

    def draw(self):
        self.screen.fill(config.GAME2_GRAY)
        self.draw_ui()

    def draw_ui(self):
        def rotation_fun(x, y, angle):
            radian = angle * math.pi / 180
            new_x = x * math.cos(radian) + y * math.sin(radian)
            new_y = -1* x * math.sin(radian) + y * math.cos(radian)
            return (new_x, new_y)

        # Basic Layout
        # Score Rect
        text_surf = self.font.render(f"分數：{self.score_manager.get_score()}", True, "WHITE")
        text_rect = text_surf.get_rect(topleft = (config.WIDTH * 0.05, config.HEIGHT * 0.05))
        border_rect = text_rect.inflate(20, 10)
        pygame.draw.rect(self.screen, "WHITE", border_rect, width=3)
        self.screen.blit(text_surf, text_rect)
        # Time Rect
        text_surf = self.font.render(f"剩餘時間：{int(self.time_manager.get_remaining_time())//60:02d}:{int(self.time_manager.get_remaining_time()%60):02d}", True, "WHITE")
        text_rect = text_surf.get_rect(topright=(config.WIDTH * 0.95, config.HEIGHT * 0.05))
        border_rect = text_rect.inflate(20, 10)
        pygame.draw.rect(self.screen, "WHITE", border_rect, width=3)
        self.screen.blit(text_surf, text_rect)
        # Pause Button
        pause_button = Button("？", config.WIDTH * 0.96, config.HEIGHT * 0.05, config.WIDTH * 0.03, config.HEIGHT * 0.05 -5, self.font, config.GAME2_PAUSE_BTN)
        pause_button.draw(self.screen)
        # 內外圓
        pygame.draw.circle(self.screen, "WHITE", (circle_center_x, circle_center_y), inner_circle_radius, 2)
        pygame.draw.circle(self.screen, "WHITE", (circle_center_x, circle_center_y), outer_circle_radius, 5)
        # 判定指示圓
        pygame.draw.circle(self.screen, "CYAN", (circle_center_x, circle_center_y), judge_circle_radius, 3)
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
        

    def update(self):
        pass

    def handle_event(self, event):
        pass