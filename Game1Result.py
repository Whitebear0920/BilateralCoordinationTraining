import pygame

import Config
from ui.Button import Button
from AssetsManager import AssetsManager

class Game1Result:
    def __init__(self, screen, result_data):
        self.screen = screen
        self.next_scene = None
        self.score = result_data["score"]

        self.font = AssetsManager.get_font("main")

        self.title = self.font.render("結算結果", True, (255, 255, 255))
        self.score = self.font.render(f"得分：{self.score}", True, (255, 255, 255))
        self.btn_a = Button("再玩一次", 0, 0, 200, 60, self.font)
        self.btn_b = Button("返回主選單", 0, 0, 200, 60, self.font)
        self.btn_c = Button("離開", 0, 0, 200, 60, self.font)


        self.title_rect = self.title.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT // 2 - 200))
        self.score_rect = self.score.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT // 2 - 100 ))
        self.btn_a.rect.center = (Config.WIDTH//2, Config.HEIGHT//2 +100)
        self.btn_b.rect.center = (Config.WIDTH//2, Config.HEIGHT//2 + 200)
        self.btn_c.rect.center = (Config.WIDTH//2, Config.HEIGHT//2 + 300)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_a.is_clicked(event):
                self.next_scene = {"name":"Game1"}
            elif self.btn_b.is_clicked(event):
                self.next_scene = {"name":"Menu"}
            elif self.btn_c.is_clicked(event):
                self.next_scene = {"name":"Exit"}


    def update(self):
        pass

    def draw(self):
        self.screen.fill((40, 40, 40))


        self.screen.blit(self.title, self.title_rect)
        self.screen.blit(self.score, self.score_rect)
        self.btn_a.draw(self.screen)
        self.btn_b.draw(self.screen)
        self.btn_c.draw(self.screen)
