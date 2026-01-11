import pygame
import time

import Config
from HandAni import HandAni
from AssetsManager import AssetsManager

class Game1Scene:
    def __init__(self, screen, gesture):
        self.screen = screen
        self.next_scene = None
        self.gesture = gesture
        self.next_scene = None
        
        self.state = "BREAK"
        self.current_action_index = 0
        self.state_start_time  = time.time()

        self.video_duration = 5.0      #影片時間
        self.train_duration = 10.0      #練習時間
        self.action_duration = 5.0     #動作時間
        self.break_duration = 5.0      #休息時間
        self.window_sec = 1.0           #檢測時長
        
        self.window_start_time = None
        self.window_snapshot = None
        self.score = 0

        self.frame_rect = pygame.Rect(0, 0, 320, 240) #鏡頭
        self.enabled_action_indices = [2,4,6]    #啟用動作組
        self.action_sets = [
            {#0
                "Video": "HH",
                "RHand": "HORIZONTAL",
                "LHand": "HORIZONTAL",
                "name": "雙手水平",
                "check": lambda g, s: (
                    g["left_horizontal_loop"] > s["left_horizontal_loop"] and
                    g["right_horizontal_loop"] > s["right_horizontal_loop"]
                )
            },
            {#1
                "Video": "VV",
                "RHand": "VERTICAL",
                "LHand": "VERTICAL",
                "name": "雙手垂直",
                "check": lambda g, s: (
                    g["left_vertical_loop"] > s["left_vertical_loop"] and
                    g["right_vertical_loop"] > s["right_vertical_loop"]
                )
            },
            {#2
                "Video": "VH",
                "RHand": "HORIZONTAL",
                "LHand": "VERTICAL",
                "name": "左垂直 + 右水平",
                "check": lambda g, s: (
                    g["left_vertical_loop"] > s["left_vertical_loop"] and
                    g["right_horizontal_loop"] > s["right_horizontal_loop"]
                )
            },
            {#3
                "Video": "HV",
                "RHand": "VERTICAL",
                "LHand": "HORIZONTAL",
                "name": "左水平 + 右垂直",
                "check": lambda g, s: (
                    g["left_horizontal_loop"] > s["left_horizontal_loop"] and
                    g["right_vertical_loop"] > s["right_vertical_loop"]
                )
            },
            {#4
                "Video": "CCWCW",
                "RHand": "CW",
                "LHand": "CCW",
                "name": "左逆 + 右順",
                "check": lambda g, s: (
                    g["left_ccw_circle"] > s["left_ccw_circle"] and
                    g["right_cw_circle"] > s["right_cw_circle"]
                )
            },
            {#5
                "Video": "CCWCCW",
                "RHand": "CCW",
                "LHand": "CCW",
                "name": "左逆 + 右逆",
                "check": lambda g, s: (
                    g["left_ccw_circle"] > s["left_ccw_circle"] and
                    g["right_ccw_circle"] > s["right_ccw_circle"]
                )
            },
            {#6
                "Video": "CWCCW",
                "RHand": "CCW",
                "LHand": "CW",
                "name": "左順 + 右逆",
                "check": lambda g, s: (
                    g["left_cw_circle"] > s["left_cw_circle"] and
                    g["right_ccw_circle"] > s["right_ccw_circle"]
                )
            },
            {#7
                "Video": "CWCW",
                "RHand": "CW",
                "LHand": "CW",
                "name": "左順 + 右順",
                "check": lambda g, s: (
                    g["left_cw_circle"] > s["left_cw_circle"] and
                    g["right_cw_circle"] > s["right_cw_circle"]
                )
            }
        ]
        
        self.font = AssetsManager.get_font("main")
        self.hand_img = AssetsManager.get_image("hand",(100,100))
        self.score_sfx = AssetsManager.get_sound("coin")
        self.video = AssetsManager.get_video(self.action_sets[self.enabled_action_indices[0]]["Video"])

        self.Lhand_ani = HandAni(image=self.hand_img,mode=self.action_sets[self.enabled_action_indices[0]]["LHand"],start_pos=(Config.WIDTH//2-500, Config.HEIGHT//2),period=2.0)
        self.Rhand_ani = HandAni(image=self.hand_img,mode=self.action_sets[self.enabled_action_indices[0]]["RHand"],start_pos=(Config.WIDTH//2+500, Config.HEIGHT//2),period=2.0)

    def handle_event(self, event):
        pass

    def update(self):
        self.update_data()
        self.main()
        self.Lhand_ani.update()
        self.Rhand_ani.update()
        self.video.update()
        pass

    def draw(self):
        self.screen.fill((40, 40, 40))
        self.draw_ui()
        self.draw_camera()
        if  self.state == "VIDEO":
            self.video.draw(self.screen,(Config.WIDTH//2-480,Config.HEIGHT-700))
        elif self.state == "TRAIN" or self.state == "ACTION":
            self.Lhand_ani.draw(self.screen)
            self.Rhand_ani.draw(self.screen)
            pygame.draw.rect(self.screen,Config.GREEN,(Config.WIDTH//2-500, Config.HEIGHT//2,5,5))
            pygame.draw.rect(self.screen,Config.GREEN,(Config.WIDTH//2+500, Config.HEIGHT//2,5,5))

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

        # ===== BREAK =====
        if self.state == "BREAK":
            self.BREAK(now)
            return
        
        # ===== VIDEO =====
        if self.state == "VIDEO":
            self.VIDEO(now)
            return
        
        # ===== TRAIN =====
        if self.state == "TRAIN":
            self.TRAIN(now)
            return
        
        # ===== ACTION =====
        if self.state == "ACTION":
            # 時間結束進入 BREAK
            self.ACTION(now)
            return
        
        if self.state == "STOP":
            self.next_scene = {
                "name": "Result",
                "data": {
                    "score": self.score,
                }
            }

            return
        pass
    
    def BREAK(self,now):
        if now - self.state_start_time >= self.break_duration:
                
                self.state = "VIDEO"
                self.state_start_time = now
                self.window_start_time = None
                self.window_snapshot = None
                print("➡️ 進入動作組：", self.action_sets[self.enabled_action_indices[self.current_action_index]]["name"])
    
    def VIDEO(self, now):
        if now - self.state_start_time >= self.video_duration:
            self.state = "TRAIN"   # 或 ACTION
            self.state_start_time = now
            print("➡️ 教學影片結束")
    
    def TRAIN(self, now):
        if now - self.state_start_time >= self.train_duration:
            self.state = "ACTION"   # 或 ACTION
            self.state_start_time = now
            print("➡️ 練習結束")
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
                #self.score += 1
                self.score_sfx.play()
                print(f"✅ {action['name']} 成功")
            self.window_start_time = None
            self.window_snapshot = None

    def ACTION(self,now):
        if now - self.state_start_time >= self.action_duration:
            self.current_action_index = (self.current_action_index + 1) % len(self.enabled_action_indices)
            if self.current_action_index == 0:
                self.state = "STOP"
                return
            self.Lhand_ani.mode = self.action_sets[self.enabled_action_indices[self.current_action_index]]["LHand"]
            self.Rhand_ani.mode = self.action_sets[self.enabled_action_indices[self.current_action_index]]["RHand"]
            self.video = AssetsManager.get_video(self.action_sets[self.enabled_action_indices[self.current_action_index]]["Video"])
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
                self.score_sfx.play()
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
            elif self.state == "BREAK":
                remain = max(0, int(self.break_duration - (now - self.state_start_time)))
                self.draw_text(f"狀態：休息", 360, 80, (200, 200, 0))
                self.draw_text(f"休息倒數：{remain}s", 360, 120)
            elif self.state == "VIDEO":
                remain = max(0, int(self.video_duration - (now - self.state_start_time)))
                self.draw_text(f"狀態：影片播放", 360, 80, (200, 200, 0))
                self.draw_text(f"影片播放倒數：{remain}s", 360, 120)
            elif self.state == "TRAIN":
                remain = max(0, int(self.train_duration - (now - self.state_start_time)))
                self.draw_text(f"狀態：練習", 360, 80, (200, 200, 0))
                self.draw_text(f"練習倒數：{remain}s", 360, 120)


            # ===== 分數 =====
            self.draw_text(f"分數：{self.score}", 360, 160, (255, 200, 50))
        #else:
        #    self.draw_text(f"最後得分：{self.score}",Config.WIDTH//2,Config.HEIGHT//2)
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