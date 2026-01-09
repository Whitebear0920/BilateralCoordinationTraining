import pygame
import Config
from ui.Button import Button
from AssetsManager import AssetsManager

class MenuScene:
    def __init__(self, screen):
        self.screen = screen
        self.next_scene = None
        self.button_font = AssetsManager.get_font("main")
        self.btn_a = Button("遊戲 1", 0, 0, 200, 60, self.button_font)
        self.btn_b = Button("遊戲 2", 0, 0, 200, 60, self.button_font)
        self.btn_c = Button("離開", 0, 0, 200, 60, self.button_font)
        self.btn_a.rect.center = (Config.WIDTH//2, Config.HEIGHT//2 - 100)
        self.btn_b.rect.center = (Config.WIDTH//2, Config.HEIGHT//2 + 100)
        self.btn_c.rect.center = (Config.WIDTH//2, Config.HEIGHT//2 + 300)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_a.is_clicked(event):
                self.next_scene = "Game1"
            elif self.btn_b.is_clicked(event):
                self.next_scene = "Game2"
            elif self.btn_c.is_clicked(event):
                self.next_scene = "Exit"

    def update(self):
        pass

    def draw(self):
        self.screen.fill((40, 40, 40))
        self.btn_a.draw(self.screen)
        self.btn_b.draw(self.screen)
        self.btn_c.draw(self.screen)