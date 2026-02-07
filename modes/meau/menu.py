import pygame
import config
from common import Button
from modes.game1 import AssetsManager

class MenuScene:
    def __init__(self, screen):
        self.screen = screen
        self.next_scene = None
        self.button_font = AssetsManager.get_font("main")
        self.btn_a = Button("遊戲 1", 0, 0, 200, 60, self.button_font)
        self.btn_b = Button("離開", 0, 0, 200, 60, self.button_font)
        #self.btn_c = Button("離開", 0, 0, 200, 60, self.button_font)
        self.btn_a.rect.center = (config.WIDTH//2, config.HEIGHT//2 - 100)
        self.btn_b.rect.center = (config.WIDTH//2, config.HEIGHT//2 + 100)
        #self.btn_c.rect.center = (config.WIDTH//2, config.HEIGHT//2 + 300)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_a.is_clicked(event):
                self.next_scene = {"name":"Game1"}
            elif self.btn_b.is_clicked(event):
                self.next_scene = {"name":"Exit"}
            #elif self.btn_c.is_clicked(event):
            #    self.next_scene = {"name":"Exit"}

    def update(self):
        pass

    def draw(self):
        self.screen.fill((40, 40, 40))
        self.btn_a.draw(self.screen)
        self.btn_b.draw(self.screen)
        #self.btn_c.draw(self.screen)