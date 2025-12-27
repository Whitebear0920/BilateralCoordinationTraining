import pygame
import numpy as np

import Config
from ui.Button import Button

class Game1Scene:
    def __init__(self, screen, font, gesture):
        self.screen = screen
        self.next_scene = None
        self.font = font
        self.gesture = gesture
        self.frame_rect = pygame.Rect(0, 0, 320, 240)
    def handle_event(self, event):
        pass

    def update(self):
        self.update_data()
        pass

    def draw(self):
        self.screen.fill((40, 40, 40))
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
        print(self.last_snapshot)
        
    def draw_camera(self):
        if self.last_snapshot["now_frame"] is not None:
            frame = self.last_snapshot["now_frame"]
            frame = frame[:, :, ::-1]
            surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            surface = pygame.transform.scale(surface,(self.frame_rect.width, self.frame_rect.height))
            self.screen.blit(surface, self.frame_rect)