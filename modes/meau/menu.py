import pygame
import config
from common import Button
from common import AssetsManager

class MenuScene:
    def __init__(self, screen):
        self.screen = screen
        self.next_scene = None
        self.button_font = AssetsManager.get_font("main")
        self.btn_game1 = Button("遊戲 1", 0, 0, 200, 60, self.button_font, config.BLUE)
        self.btn_game2 = Button("遊戲 2", 0, 0, 200, 60, self.button_font, config.BLUE)
        self.btn_exit = Button("離開", 0, 0, 200, 60, self.button_font, config.BLUE)

        self.btn_game1.rect.center = (config.WIDTH//2, config.HEIGHT//2 - 100)
        self.btn_game2.rect.center = (config.WIDTH//2, config.HEIGHT//2 + 100)
        self.btn_exit.rect.center = (config.WIDTH//2, config.HEIGHT//2 + 300)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_game1.is_clicked(event):
                self.next_scene = {"name":"Game1Setting"}
            elif self.btn_game2.is_clicked(event):
                self.next_scene = {"name":"Game2"}
            elif self.btn_exit.is_clicked(event):
               self.next_scene = {"name":"Exit"}

    def update(self):
        pass

    def draw(self):
        self.screen.fill((40, 40, 40))
        self.btn_game1.draw(self.screen)
        self.btn_game2.draw(self.screen)
        self.btn_exit.draw(self.screen)
        self.draw_text("音效使用:UUi Shen/Shura LU",20,config.HEIGHT-62,isCenter=False)
        #self.btn_c.draw(self.screen)

    def draw_text(self, text, x, y, color=(255,255,255), isCenter = True):
        surf = self.button_font.render(text, True, color)
        if isCenter:
            rect = surf.get_rect(center=(x,y))
            self.screen.blit(surf, rect)
        else:
            self.screen.blit(surf, (x, y))