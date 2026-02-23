import pygame.draw
import math
import config
from common.assets_manager import AssetsManager
from common import Button
from .score_manager import ScoreManager
from .time_manager import TimeManager
from .settings import *
from .light_sword import LightSword

class Game2Scene:
    def __init__(self, screen, api):
        self.screen = screen
        self.level = 1
        self.score_manager = ScoreManager()

        self.angle_api = api

        self.time_manager = TimeManager()
        self.time_manager.start_timer()

        self.font = AssetsManager.get_font("main")


        scale_ration = (judge_circle_radius - inner_circle_radius)  * 2
        self.red_sword = AssetsManager.get_image("RED_SWORD")
        self.blue_sword = AssetsManager.get_image("BLUE_SWORD")
        self.red_sword = self._rescale_ration(self.red_sword, scale_ration)
        self.blue_sword = self._rescale_ration(self.blue_sword, scale_ration)
        self.left_sword = LightSword(self.red_sword, self.angle_api, "LEFT")
        self.right_sword = LightSword(self.blue_sword, self.angle_api, "RIGHT")

        self.sprite_manager = pygame.sprite.Group()
        self.sprite_manager.add(self.left_sword)
        self.sprite_manager.add(self.right_sword)

    def main(self):
        self.sprite_manager.update()

    def draw(self):
        self.screen.fill(config.GAME2_GRAY)
        self.draw_ui()

        self.sprite_manager.draw(self.screen)

    def draw_ui(self):
        # 1. 準備常用參數
        center = pygame.Vector2(circle_center_x, circle_center_y)
        num_lines = level_dict[self.level]
        t = pygame.time.get_ticks() / 1000.0

        # 計算旋轉角度 (180度平分)
        # 注意：Pygame 的 Vector 旋轉角度正值是順時針，0度是指向右方 (1, 0)
        start_angle = 180
        angle_step = 180 / (num_lines - 1) if num_lines > 1 else 0

        # --- 繪製順序：先畫線，再畫圓 (解決凸出問題) ---

        # 2. 繪製內外圓相連線
        for i in range(num_lines):
            # 建立一個指向左方的基礎向量，然後旋轉
            # 這裡的角度是 i * angle_step (順時針旋轉)
            direction = pygame.Vector2(-1, 0).rotate(i * angle_step)

            # 利用向量乘法快速得到座標
            draw_start = center + direction * outer_circle_radius
            draw_end = center + direction * inner_circle_radius

            pygame.draw.line(self.screen, "WHITE", draw_start, draw_end, 5)

        # 3. 繪製圓圈 (當作「蓋子」壓在線上面)
        pygame.draw.circle(self.screen, "WHITE", center, inner_circle_radius, 2)
        pygame.draw.circle(self.screen, "WHITE", center, outer_circle_radius, 5)
        pygame.draw.circle(self.screen, "CYAN", center, judge_circle_radius, 3)

        # 4. 繪製文字 UI (建議寫成小工具函數減少重複代碼)
        self._draw_status_box(f"分數：{self.score_manager.get_score()}", (config.WIDTH * 0.05, config.HEIGHT * 0.05),
                              "topleft")

        time_val = self.time_manager.get_remaining_time()
        time_str = f"剩餘時間：{int(time_val) // 60:02d}:{int(time_val % 60):02d}"

        # 如果時間小於 5 秒，文字變紅色且閃爍
        time_color = "WHITE"
        if time_val <= 5 and int(t * 10) % 2 == 0:
            time_color = (255, 50, 50)

        self._draw_status_box(time_str, (config.WIDTH * 0.95, config.HEIGHT * 0.05), "topright", color=time_color)
        # 5. 暫停按鈕
        pause_button = Button("？", config.WIDTH * 0.96, config.HEIGHT * 0.05, config.WIDTH * 0.03,
                              config.HEIGHT * 0.05 - 5, self.font, config.GAME2_PAUSE_BTN)
        pause_button.draw(self.screen)

    def update(self):
        self.main()

    def handle_event(self, event):
        pass

    def _draw_status_box(self, text, pos, anchor, color="WHITE"):
        text_surf = self.font.render(text, True, color)
        text_rect = text_surf.get_rect(**{anchor: pos})

        # 畫一個半透明的黑底背景，增加層次感
        bg_rect = text_rect.inflate(20, 10)
        bg_surf = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, (0, 0, 0, 150), [0, 0, bg_rect.width, bg_rect.height])  # 150 是透明度
        self.screen.blit(bg_surf, bg_rect.topleft)

        # 畫邊框
        pygame.draw.rect(self.screen, color, bg_rect, width=2)
        self.screen.blit(text_surf, text_rect)

    def _rescale_ration(self, image, target_height):
        old_width, old_height = image.get_width(), image.get_height()
        ratio = target_height / old_height
        target_width = int(old_width * ratio)
        return pygame.transform.smoothscale(image, (target_width, target_height))