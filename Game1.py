import pygame
import Config
from ui.Button import Button

class Game1Scene:
    def __init__(self, screen, font, gesture):
        self.screen = screen
        self.next_scene = None
        self.font = font
        self.gesture = gesture
        self.last_snapshot = {
            "left_circle": gesture["left_circle"],
            "right_circle": gesture["right_circle"],
            "left_horizontal_loop": gesture["left_horizontal_loop"],
            "right_horizontal_loop": gesture["right_horizontal_loop"],
            "left_vertical_loop": gesture["left_vertical_loop"],
            "right_vertical_loop": gesture["right_vertical_loop"],
        }
    def handle_event(self, event):
        pass

    def update(self):
        self.last_snapshot = {
            "left_circle": self.gesture["left_circle"],
            "right_circle": self.gesture["right_circle"],
            "left_horizontal_loop": self.gesture["left_horizontal_loop"],
            "right_horizontal_loop": self.gesture["right_horizontal_loop"],
            "left_vertical_loop": self.gesture["left_vertical_loop"],
            "right_vertical_loop": self.gesture["right_vertical_loop"],
        }
        print(self.last_snapshot)
        pass

    def draw(self):
        self.screen.fill((40, 40, 40))