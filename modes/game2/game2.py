import pygame.draw
import math
import config
from common.assets_manager import AssetsManager
from common.button import Button
from .score_manager import ScoreManager
from .time_manager import TimeManager
from .settings import *
from .light_sword import LightSword
from .marble import Marble

class Game2Scene:
    def __init__(self, screen, api):
        self.screen = screen
        self.score_manager = ScoreManager()
        self.font = AssetsManager.get_font("main")
        self.next_scene = None
        # game control
        self.game_state = "PAUSE" # "PAUSE", "START"
        # 遊戲參數設定
        self.level = 1  # 遊戲等級
        self.angle_step = 180 / (level_dict[self.level] - 1) if level_dict[self.level] > 1 else 0  # marble軌道角度控制
        # 時間控制
        self.time_manager = TimeManager(play_time=level_info_dict[self.level]["time"])
        # 角度計算API
        self.angle_api = api
        # 縮放比例
        scale_ration = (judge_circle_radius - inner_circle_radius)  * 2
        # 光劍設定
        self.red_sword = AssetsManager.get_image("RED_SWORD")
        self.blue_sword = AssetsManager.get_image("BLUE_SWORD")
        self.red_sword = self._rescale_ration(self.red_sword, scale_ration)
        self.blue_sword = self._rescale_ration(self.blue_sword, scale_ration)
        self.left_sword = LightSword(self.red_sword, self.angle_api, "LEFT")
        self.right_sword = LightSword(self.blue_sword, self.angle_api, "RIGHT")
        self.sprite_manager = pygame.sprite.Group()
        self.sprite_manager.add(self.left_sword)
        self.sprite_manager.add(self.right_sword)
        # marble設定
        for i in range(10):
            red_marble_sprite = Marble("RED", 5, self.angle_step, 1)
            blue_marble_sprite = Marble("BLUE", 5, self.angle_step, 3)
            self.sprite_manager.add(red_marble_sprite)
            self.sprite_manager.add(blue_marble_sprite)
        # button設定
        self.start_btn = None
        self.exit_btn = None
        self.pause_btn = None

    def update(self): # first call in the main loop
        if self.game_state == "START":
            self.time_manager.update_timer()
            self.sprite_manager.update()

    def draw(self): # second call in the main loop
        self.screen.fill(config.GAME2_GRAY)
        if self.game_state == "PAUSE":
            self._draw_info_box()
        elif self.game_state == "START":
            self._draw_ui()
            self.sprite_manager.draw(self.screen)

    def handle_event(self, event):
        # 按鈕事件
        if self.game_state == "PAUSE":
            # 偵測 Start 按鈕
            if self.start_btn.is_clicked(event):
                self._change_game_state("START")
            # 偵測 Exit 按鈕
            if self.exit_btn.is_clicked(event):
                self.next_scene = {"name":"Menu"}
            # 偵測 ? 按鈕
        elif self.game_state == "START":
            if self.pause_btn is not None and self.pause_btn.is_clicked(event):
                self._change_game_state("PAUSE")
        # Game time over event
        if self.game_state == "START":
            if event == GAME2_TIMER_ALERT:
                self._change_game_state("PAUSE")


    def _change_game_state(self, state):
        if state == "START":
            self.game_state = "START"
            self.time_manager.start_timer()
            print("Game2 state is changed!! state: START")
        elif state == "PAUSE":
            self.game_state = "PAUSE"
            self.time_manager.stop_timer()
            print("Game2 state is changed!! state: PAUSE")

    # draw info box
    def _draw_info_box(self):
        # 1. 定義方框大小與位置
        box_width, box_height = 400, 300
        box_x = (config.WIDTH - box_width) // 2
        box_y = (config.HEIGHT - box_height) // 2

        # 2. 畫出外框底色 (可以用稍微深一點的灰色或半透明黑色)
        # 繪製一個矩形作為背景
        bg_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(self.screen, (50, 50, 50), bg_rect)  # 深灰色背景
        pygame.draw.rect(self.screen, (255, 255, 255), bg_rect, 3)  # 白色邊框，寬度 3

        # 3. 繪製文字 (標題)
        title_surf = self.font.render("GAME PAUSED", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(config.WIDTH // 2, box_y + 50))
        self.screen.blit(title_surf, title_rect)

        # 4. 放置你的自定義按鈕
        # 使用你提供的 Button 格式
        btn_w, btn_h = 120, 45

        # Start (或 Resume) 按鈕
        self.start_btn = Button("Start",
                            config.WIDTH // 2 - btn_w // 2,
                            box_y + 120,
                            btn_w, btn_h,
                            self.font, config.GREEN)

        # Exit 按鈕
        self.exit_btn = Button("Exit",
                          config.WIDTH // 2 - btn_w // 2,
                          box_y + 190,
                          btn_w, btn_h,
                          self.font, config.RED)

        # 執行按鈕的繪製方法 (假設你的 Button 類別有 draw 方法)
        self.start_btn.draw(self.screen)
        self.exit_btn.draw(self.screen)

    # region inner function
    def _draw_ui(self):
        # 1. 準備常用參數
        center = pygame.Vector2(circle_center_x, circle_center_y)
        t = pygame.time.get_ticks() / 1000.0
        # 計算旋轉角度 (180度平分)
        # 注意：Pygame 的 Vector 旋轉角度正值是順時針，0度是指向右方 (1, 0)
        num_lines = level_dict[self.level]
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
        self._draw_status_box("".join(["分數：",
                                      str(self.score_manager.get_score()),
                                      "/",
                                      str(level_info_dict[self.level]["pass_score"])]),
                              (config.WIDTH * 0.05, config.HEIGHT * 0.05),
                              "topleft")

        time_val = self.time_manager.get_remaining_time()
        time_str = f"剩餘時間：{int(time_val) // 60:02d}:{int(time_val % 60):02d}"

        # 如果時間小於 5 秒，文字變紅色且閃爍
        time_color = "WHITE"
        if time_val <= 5 and int(t * 10) % 2 == 0:
            time_color = (255, 50, 50)

        self._draw_status_box(time_str, (config.WIDTH * 0.95, config.HEIGHT * 0.05), "topright", color=time_color)
        # 5. 暫停按鈕
        self.pause_btn = Button("？", config.WIDTH * 0.96, config.HEIGHT * 0.05, config.WIDTH * 0.03,
                              config.HEIGHT * 0.05 - 5, self.font, config.GAME2_PAUSE_BTN)
        self.pause_btn.draw(self.screen)

    def _draw_status_box(self, text, pos, anchor, color="WHITE"):
        text_surf = self.font.render(text, True, color)
        text_rect = text_surf.get_rect(**{anchor: pos})

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

    def _game_level_upgrade(self):
        self.level += 1
        self.angle_step = 180 / (level_dict[self.level] - 1) if level_dict[self.level] > 1 else 0
    # endregion
