import pygame
import time

import Config
from ui.Button import Button

class Game1Scene:
    def __init__(self, screen, font, gesture):
        self.screen = screen
        self.next_scene = None
        self.font = font
        self.gesture = gesture
        self.next_scene = None

        self.hand_img = pygame.image.load(f"Assets/Image/Game1/hand.png").convert_alpha()

        self.state = "BREAK"
        self.current_action_index = 0
        self.state_start_time  = time.time()

        self.action_duration = 15.0 #動作時間
        self.break_duration = 5.0   #休息時間
        self.window_sec = 1.0       #檢測時長
        
        self.window_start_time = None
        self.window_snapshot = None
        self.score = 0

        self.frame_rect = pygame.Rect(0, 0, 320, 240) #鏡頭
        self.enabled_action_indices = [4, 2]    #啟用動作組
        self.action_sets = [
            {
                "name": "雙手水平",
                "check": lambda g, s: (
                    g["left_horizontal_loop"] > s["left_horizontal_loop"] and
                    g["right_horizontal_loop"] > s["right_horizontal_loop"]
                )
            },
            {
                "name": "雙手垂直",
                "check": lambda g, s: (
                    g["left_vertical_loop"] > s["left_vertical_loop"] and
                    g["right_vertical_loop"] > s["right_vertical_loop"]
                )
            },
            {
                "name": "左垂直 + 右水平",
                "check": lambda g, s: (
                    g["left_vertical_loop"] > s["left_vertical_loop"] and
                    g["right_horizontal_loop"] > s["right_horizontal_loop"]
                )
            },
            {
                "name": "左水平 + 右垂直",
                "check": lambda g, s: (
                    g["left_horizontal_loop"] > s["left_horizontal_loop"] and
                    g["right_vertical_loop"] > s["right_vertical_loop"]
                )
            },
            {
                "name": "左逆 + 右順",
                "check": lambda g, s: (
                    g["left_ccw_circle"] > s["left_ccw_circle"] and
                    g["right_cw_circle"] > s["right_cw_circle"]
                )
            },
            {
                "name": "左逆 + 右逆",
                "check": lambda g, s: (
                    g["left_ccw_circle"] > s["left_ccw_circle"] and
                    g["right_ccw_circle"] > s["right_ccw_circle"]
                )
            },
            {
                "name": "左順 + 右逆",
                "check": lambda g, s: (
                    g["left_cw_circle"] > s["left_cw_circle"] and
                    g["right_ccw_circle"] > s["right_ccw_circle"]
                )
            },
            {
                "name": "左順 + 右順",
                "check": lambda g, s: (
                    g["left_cw_circle"] > s["left_cw_circle"] and
                    g["right_cw_circle"] > s["right_cw_circle"]
                )
            }
        ]
    def handle_event(self, event):
        pass

    def update(self):
        self.update_data()
        self.main()
        pass

    def draw(self):
        self.screen.fill((40, 40, 40))
        self.screen.blit(self.hand_img, (360, 200))
        self.draw_ui()
        self.draw_camera()
    
    def update_data(self):
        temp = self.gesture()
        self.last_snapshot = {
            "now_frame": temp["now_frame"],
            "left_ccw_circle": temp["left_ccw_circle"],
            "left_cw_circle": temp["left_cw_circle"],
            "right_ccw_circle": temp["right_ccw_circle"],
            "right_cw_circle": temp["right_cw_circle"],
            "left_horizontal_loop": temp["left_horizontal_loop"],
            "right_horizontal_loop": temp["right_horizontal_loop"],
            "left_vertical_loop": temp["left_vertical_loop"],
            "right_vertical_loop": temp["right_vertical_loop"],
        }
        #print(self.last_snapshot)
    
    def main(self):
        now = time.time()

        # ===== BREAK=====
        if self.state == "BREAK":
            self.BREAK(now)
            return

        # ===== ACTION=====
        if self.state == "ACTION":
            # 時間結束進入 BREAK
            self.ACTION(now)
            return
        
        if self.state == "STOP":
            self.next_scene = "Menu"
            return
        pass
    
    def BREAK(self,now):
        if now - self.state_start_time >= self.break_duration:
                
                self.state = "ACTION"
                self.state_start_time = now
                self.window_start_time = None
                self.window_snapshot = None
                print("➡️ 進入動作組：", self.action_sets[self.enabled_action_indices[self.current_action_index]]["name"])

    def ACTION(self,now):
        if now - self.state_start_time >= self.action_duration:
            self.current_action_index = (self.current_action_index + 1) % len(self.enabled_action_indices)
            if self.current_action_index == 0:
                self.state = "STOP"
                return
            self.state = "BREAK"
            self.state_start_time = now
            self.window_start_time = None
            self.window_snapshot = None
            print("⏸ 休息 5 秒")
            return
        # ===== 存狀態 =====
        if self.window_start_time is None:
            self.window_start_time = now
            self.window_snapshot = {
                "left_horizontal_loop": self.last_snapshot["left_horizontal_loop"],
                "right_horizontal_loop": self.last_snapshot["right_horizontal_loop"],
                "left_vertical_loop": self.last_snapshot["left_vertical_loop"],
                "right_vertical_loop": self.last_snapshot["right_vertical_loop"],
                "left_ccw_circle": self.last_snapshot["left_ccw_circle"],
                "left_cw_circle": self.last_snapshot["left_cw_circle"],
                "right_ccw_circle": self.last_snapshot["right_ccw_circle"],
                "right_cw_circle": self.last_snapshot["right_cw_circle"],
            }
            return
        # ===== 檢測 =====
        if now - self.window_start_time >= self.window_sec:
            action = self.action_sets[self.enabled_action_indices[self.current_action_index]]
            if action["check"](self.last_snapshot, self.window_snapshot):
                self.score += 1
                print(f"✅ {action['name']} 成功，目前分數{self.score}")
            self.window_start_time = None
            self.window_snapshot = None
    def draw_ui(self):
        now = time.time()

        # ===== 目前動作 =====
        action = self.action_sets[self.enabled_action_indices[self.current_action_index]]
        if self.state != "STOP":
            self.draw_text(f"動作：{action['name']}", 360, 40)

            # ===== 狀態 + 倒數 =====
            if self.state == "ACTION":
                remain = max(0, int(self.action_duration - (now - self.state_start_time)))
                self.draw_text(f"狀態：動作中", 360, 80, (0, 200, 0))
                self.draw_text(f"剩餘時間：{remain}s", 360, 120)
            else:
                remain = max(0, int(self.break_duration - (now - self.state_start_time)))
                self.draw_text(f"狀態：休息", 360, 80, (200, 200, 0))
                self.draw_text(f"休息倒數：{remain}s", 360, 120)

            # ===== 分數 =====
            self.draw_text(f"分數：{self.score}", 360, 160, (255, 200, 50))
        else:
            self.draw_text(f"最後得分：{self.score}",Config.WIDTH//2,Config.HEIGHT//2)
    def draw_text(self, text, x, y, color=(255,255,255)):
        surf = self.font.render(text, True, color)
        self.screen.blit(surf, (x, y))

    def draw_camera(self):
        frame = self.last_snapshot["now_frame"]
        if frame is None:
            return
        frame = frame.copy()
        frame = frame[:, :, ::-1]
        surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        surface = pygame.transform.scale(surface,(self.frame_rect.width, self.frame_rect.height))
        self.screen.blit(surface, self.frame_rect)
        return