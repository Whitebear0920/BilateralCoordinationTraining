import pygame
from enum import Enum, auto

import config
from common import Button
from common.assets_manager import AssetsManager
class Game1Setting:
    def __init__(self,screen):
        self.screen = screen
        self.next_scene = None
        
        self.font = AssetsManager.get_font("main")
        
        self.enabled_action_indices = [Game1Action.VV,Game1Action.HH]
        self.train_duration = 20
        self.action_duration = 30
        self.break_duration = 20
        
        self.action_name = ["雙手水平","雙手垂直","左垂直 + 右水平","左水平 + 右垂直","左逆 + 右順","左逆 + 右逆","左順 + 右逆","左順 + 右順","左垂直 + 右順","左垂直 + 右逆","左逆 + 右垂直","左順 + 右垂直","左水平 + 右逆","左順 + 右水平","左水平 + 右順","左逆 + 右水平",]
        self.action_btn = []
        start_x = 200
        start_y = 120
        gap_y = 60
        gap_x = 350
        for i in range(16):
            col = i // 8
            row = i % 8
            x = start_x + col * gap_x
            y = start_y + row * gap_y

            btn = Button(self.action_name[i],x,y,300,50,self.font,config.BLUE)
            self.action_btn.append(btn)
            pass
        #self.action_btn = Button("", config.WIDTH//2,50, 300, 50, self.font, config.BLUE)

    def handle_event(self, event):
        pass
    
    def update(self):
        pass
    
    def draw(self):
        self.screen.fill((40, 40, 40))
        self.draw_text("設置",config.WIDTH//2,21)
        for btn in self.action_btn:
            btn.draw(self.screen)
        #self.action_btn.draw(self.screen)
        pass

    def draw_text(self, text, x, y, color=(255,255,255), isCenter = True):
        surf = self.font.render(text, True, color)
        if isCenter:
            rect = surf.get_rect(center=(x,y))
            self.screen.blit(surf, rect)
        else:
            self.screen.blit(surf, (x, y))
class Game1Action(Enum):
    HH = auto()
    VV = auto()