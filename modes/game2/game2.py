import pygame.draw
import math
import config
import random
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
        self.angle_step = 180 / (level_info_dict[self.level]["line"] - 1)  # marble軌道角度控制
        # 時間控制
        self.time_manager = TimeManager(play_time=level_info_dict[self.level]["time"])
        self.anim_timer = 0  # 動畫計時器
        self.anim_speed = 5  # 滑動速度
        # 角度計算API
        self.angle_api = api
        # 縮放比例
        scale_ration = (judge_circle_radius - inner_circle_radius)  * 2
        #VFX
        self.sword_vfx = AssetsManager.get_sound("sword")
        self.error_vfx = AssetsManager.get_sound("error")
        # 光劍設定
        self.red_sword = AssetsManager.get_image("RED_SWORD")
        self.blue_sword = AssetsManager.get_image("BLUE_SWORD")
        self.red_sword = self._rescale_ration(self.red_sword, scale_ration)
        self.blue_sword = self._rescale_ration(self.blue_sword, scale_ration)
        self.left_sword = LightSword(self.red_sword, self.angle_api, "LEFT", "RED") # 右手紅
        self.right_sword = LightSword(self.blue_sword, self.angle_api, "RIGHT", "BLUE") # 左手藍
        self.sword_sprite_manager = pygame.sprite.Group()
        self.sword_sprite_manager.add(self.left_sword)
        self.sword_sprite_manager.add(self.right_sword)
        # marble設定
        self.next_generate_time = None # 生成時間控制
        self.marble_pool = {"RED":[], "BLUE":[]}
        self.marble_sprite_manager = pygame.sprite.Group()
        for _ in range(10):
            red_marble_sprite = Marble("RED", level_info_dict[self.level]["marble_speed"], self.angle_step)
            blue_marble_sprite = Marble("BLUE", level_info_dict[self.level]["marble_speed"], self.angle_step)
            self.marble_pool["RED"].append(red_marble_sprite)
            self.marble_pool["BLUE"].append(blue_marble_sprite)
            self.marble_sprite_manager.add(red_marble_sprite)
            self.marble_sprite_manager.add(blue_marble_sprite)
        # button設定
        self.start_btn = None
        self.exit_btn = None
        self.pause_btn = None
        # info box 文字內容
        self.info_text = "準備開始囉!!"

    def update(self): # first call in the main loop
        if self.game_state == "START":
            # 更新時間
            self.time_manager.update_timer()
            # 更新光劍
            self.sword_sprite_manager.update()
            # 更新marble生成
            self.time_manager.generate_marble()
            # Update marble_pool
            for color, ls in self.marble_pool.items():
                for m in ls:
                    if m.is_active() or m.is_broken:
                        m.update()
            # 碰撞檢查
            for sword in self.sword_sprite_manager:
                # 這裡的 marble_sprite_manager 包含所有彈珠
                hit_list = pygame.sprite.spritecollide(sword, self.marble_sprite_manager, False, pygame.sprite.collide_mask)
                for m in hit_list:
                    # 增加 m.is_active() 判斷，避免重複砍中正在碎裂的彈珠
                    if m.is_active() and not m.is_broken():
                        if (m.color == "RED" and sword.color == "RED") or (m.color == "BLUE" and sword.color == "BLUE"):
                            m.hit()

    def draw(self): # second call in the main loop
        self.screen.fill(config.GAME2_GRAY)
        if self.game_state == "PAUSE":
            # 畫暫停框
            self._draw_info_box()
        elif self.game_state == "START":
            # 畫場景
            self._draw_ui()
            # 畫marble
            for color, ls in self.marble_pool.items():
                for m in ls:
                    if m.is_active():
                        m.draw(self.screen)
            # 畫光劍
            self.sword_sprite_manager.draw(self.screen)

    def handle_event(self, event):
        # 按鈕事件
        if self.game_state == "PAUSE":
            # 偵測 Start 按鈕
            if self.level_1_btn.is_clicked(event) and level_info_dict[1]["previous_level_passed"]:
                self.level = 1
                self.angle_step = 180 / (level_info_dict[self.level]["line"] - 1)
                self._change_game_state("START")
            if self.level_2_btn.is_clicked(event) and level_info_dict[2]["previous_level_passed"]:
                self.level = 2
                self.angle_step = 180 / (level_info_dict[self.level]["line"] - 1)
                self._change_game_state("START")
            if self.level_3_btn.is_clicked(event) and level_info_dict[3]["previous_level_passed"]:
                self.level = 3
                self.angle_step = 180 / (level_info_dict[self.level]["line"] - 1)
                self._change_game_state("START")
            # 偵測 Exit 按鈕
            if self.exit_btn.is_clicked(event):
                self.next_scene = {"name":"Menu"}
        # Gaming event
        elif self.game_state == "START":
            # Beta
            if event.type == pygame.KEYDOWN:
                print("keydown")
                if event.key == pygame.K_g:
                    self.score_manager.add_score(100)
            # 偵測 ? 按鈕
            if self.pause_btn is not None and self.pause_btn.is_clicked(event):
                self._change_game_state("PAUSE")
            # 時間事件
            if event == GAME2_TIMER_ALERT:
                self.info_text = "你的分數: " + str(self.score_manager.get_score()) + "!!"
                self._game_level_upgrade(self.score_manager.get_score())
                self.score_manager.reset_score(0)
                self._reset_all_marble_to_default()
                self._change_game_state("PAUSE")
            # 分數事件
            if event == MARBLE_NO_BREAK: # 沒擊破 扣分 # !!!! Not active
                #self.score_manager.decrease_score(10)
                self.error_vfx.play()
                pass
            if event == MARBLE_BREAK: # 擊破 加分
                self.score_manager.add_score(10)
                self.sword_vfx.play()
            # Marble 事件
            if event == MARBLE_GENERATE:
                self._generate_marble()

    # region inner function
    # drawing relate function
    ## 關卡選擇畫面
    def _draw_info_box(self):
        # 1. 定義方框大小與位置
        box_width, box_height = 500, 300
        box_x = (config.WIDTH - box_width) // 2
        box_y = (config.HEIGHT - box_height) // 2

        # 2. 背景與邊框
        bg_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(self.screen, (50, 50, 50), bg_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), bg_rect, 3)

        # --- 3. 動態標題動畫邏輯 ---
        self.anim_timer += 1  # 每一幀增加計時

        # 設定字體（建議標題用大一點的字）
        title_font = pygame.font.SysFont("microsoftjhenghei", 100, bold=True)
        target_y = box_y - 80  # 標題最終停留的垂直位置（方框上方）
        start_y = -100  # 初始位置（螢幕外）

        # 定義四個字的屬性：文字、顏色、延遲時間、當前x位置偏移
        # 延遲時間讓字體有「一個接一個」的感覺
        elements = [
            {"text": "光", "color": config.RED, "delay": 0, "offset_x": -165},
            {"text": "劍", "color": config.BLUE, "delay": 10, "offset_x": -55},
            {"text": "遊戲", "color": (255, 255, 255), "delay": 25, "offset_x": 105}
        ]

        for item in elements:
            # 計算插值：如果計時器超過了延遲，才開始移動
            elapsed = max(0, self.anim_timer - item["delay"])
            # 使用簡單的移動邏輯，直到到達 target_y
            current_y = min(target_y, start_y + elapsed * self.anim_speed)

            surf = title_font.render(item["text"], True, item["color"])
            rect = surf.get_rect(center=(config.WIDTH // 2 + item["offset_x"], current_y))
            self.screen.blit(surf, rect)

        # 提示文字
        self._draw_text("左手紅色 右手藍色", config.WIDTH // 2, box_y + 90)

        # 4. 按鈕處理
        btn_w, btn_h = 120, 45
        self.level_1_btn = Button("LV. 1", config.WIDTH // 2 - btn_w * 1.5 - 10, box_y + 120, btn_w, btn_h, self.font,
                                config.GREEN if level_info_dict[1]["previous_level_passed"] else config.GRAY)
        self.level_2_btn = Button("LV. 2", config.WIDTH // 2 - btn_w // 2, box_y + 120, btn_w, btn_h, self.font,
                                config.GREEN if level_info_dict[2]["previous_level_passed"] else config.GRAY)
        self.level_3_btn = Button("LV. 3", config.WIDTH // 2 + btn_w // 2 + 10, box_y + 120, btn_w, btn_h, self.font,
                                config.GREEN if level_info_dict[3]["previous_level_passed"] else config.GRAY)
        self.exit_btn = Button("Exit", config.WIDTH // 2 - btn_w // 2, box_y + 190, btn_w, btn_h, self.font, config.RED)

        self.level_1_btn.draw(self.screen)
        self.level_2_btn.draw(self.screen)
        self.level_3_btn.draw(self.screen)
        self.exit_btn.draw(self.screen)
    ## 繪製圓形線條與暫停按鈕以及倒數計時器
    def _draw_ui(self):
        # 1. 準備常用參數
        center = pygame.Vector2(circle_center_x, circle_center_y)
        t = pygame.time.get_ticks() / 1000.0
        # 計算旋轉角度 (180度平分)
        # 注意：Pygame 的 Vector 旋轉角度正值是順時針，0度是指向右方 (1, 0)
        num_lines = level_info_dict[self.level]["line"]
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
        current_score = self.score_manager.get_score()
        pass_score = level_info_dict[self.level]["pass_score"]

        # 判斷當前分數的顏色
        score_color = "GREEN" if current_score >= pass_score else "RED"

        # 拆成三個片段
        parts = [
            ("分數：", "WHITE"),
            (str(current_score), score_color),
            (f" / {pass_score}", "WHITE")
        ]

        self._draw_status_box(parts, (config.WIDTH * 0.05, config.HEIGHT * 0.05), "topleft")

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
    ## 繪製提示文字
    def _draw_text(self, text, x, y, color=(255,255,255), isCenter = True):
        surf = self.font.render(text, True, color)
        if isCenter:
            rect = surf.get_rect(center=(x,y))
            self.screen.blit(surf, rect)
        else:
            self.screen.blit(surf, (x, y))
    ## 繪製分數
    def _draw_status_box(self, text, pos, anchor, color="WHITE"):
        """
        text: 可以是字串 "100" 或 列表 [("A", "RED"), ("B", "WHITE")]
        color: 當 text 是字串時使用的顏色，預設為白色
        """
        # --- 第一步：統一格式 ---
        # 如果傳進來的是一般字串，我們把它變成 [(字串, 顏色)] 的格式
        if isinstance(text, str):
            text_parts = [(text, color)]
        else:
            # 如果傳進來的是 list，就直接使用
            text_parts = text

        # --- 第二步：計算總大小與準備畫布 ---
        surfaces = []
        total_width = 0
        max_height = 0

        for txt, clr in text_parts:
            surf = self.font.render(txt, True, clr)
            surfaces.append(surf)
            total_width += surf.get_width()
            max_height = max(max_height, surf.get_height())

        # 建立一個透明組合畫布
        combined_surf = pygame.Surface((total_width, max_height), pygame.SRCALPHA)
        x_offset = 0
        for surf in surfaces:
            combined_surf.blit(surf, (x_offset, 0))
            x_offset += surf.get_width()

        # --- 第三步：畫框與背景 ---
        text_rect = combined_surf.get_rect(**{anchor: pos})
        bg_rect = text_rect.inflate(20, 10)

        # 畫背景
        bg_surf = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, (0, 0, 0, 150), [0, 0, bg_rect.width, bg_rect.height])
        self.screen.blit(bg_surf, bg_rect.topleft)

        # 畫邊框（這裡固定用白色，或者如果你希望邊框跟著顏色走，可以用 color 或 text_parts[0][1]）
        pygame.draw.rect(self.screen, "WHITE", bg_rect, width=2)

        # 把文字畫上去
        self.screen.blit(combined_surf, text_rect)
    # control relate
    def _rescale_ration(self, image, target_height):
        old_width, old_height = image.get_width(), image.get_height()
        ratio = target_height / old_height
        target_width = int(old_width * ratio)
        return pygame.transform.smoothscale(image, (target_width, target_height))

    def _change_game_state(self, state):
        if state == "START":
            self.game_state = "START"
            self.time_manager.start_timer()
            print("Game2 state is changed!! state: START")
        elif state == "PAUSE":
            self.game_state = "PAUSE"
            self.time_manager.stop_timer()
            print("Game2 state is changed!! state: PAUSE")

    def _game_level_upgrade(self, score):
        if score > level_info_dict[self.level]["pass_score"]:
            if self.level < 3:
                level_info_dict[self.level+1]["previous_level_passed"] = True
    def _generate_marble(self):
        # Every 1 sec go to marble_pool find an inactive sprite.
            # 生成一顆marble 隨機位置 隨機顏色
        random_number = random.randint(1, 2)
        if random_number == 1:
            marble_color = "RED" # left area. right hand
        else:
            marble_color = "BLUE" # right area. left hand
        temp_active = []
        temp_broken = []
        for m in self.marble_pool[marble_color]:
            temp_active.append(m.is_active())
            temp_broken.append(m.is_broken())
            if not m.is_active() and not m.is_broken():
                m.update_offset(new_angle_step=self.angle_step,
                                new_track_id=random.randint(*(1, (level_info_dict[self.level]["line"] - 2) // 2 + 1) if marble_color == "RED" else ((level_info_dict[self.level]["line"] - 2) // 2 + 1, level_info_dict[self.level]["line"] - 2)),
                                new_speed=level_info_dict[self.level]["marble_speed"])
                m.active_sprite()
                break

    def _reset_all_marble_to_default(self):
        # Update marble_pool
        for color, ls in self.marble_pool.items():
            for m in ls:
                m.reset_to_start_state()
                m.unactive_sprite()
    # endregion
