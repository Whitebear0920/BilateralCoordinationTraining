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
        
        self.enabled_action = [Game1Action.VV,Game1Action.HH]
        self.enabled_action_indices = []
        self.train_duration = 20
        self.action_duration = 30
        self.break_duration = 20
        self.time_options = [5,10,15,20,25,30]
        self.action_name = ["雙手水平","雙手垂直","左垂直 + 右水平","左水平 + 右垂直","左逆 + 右順","左逆 + 右逆","左順 + 右逆","左順 + 右順","左垂直 + 右順","左垂直 + 右逆","左逆 + 右垂直","左順 + 右垂直","左水平 + 右逆","左順 + 右水平","左水平 + 右順","左逆 + 右水平",]
        
        self.action_btn = []
        action_btn_start_x = 200
        action_btn_start_y = 120
        action_btn_gap_y = 60
        action_btn_gap_x = 350
        for i in range(16):
            col = i // 8
            row = i % 8
            x = action_btn_start_x + col * action_btn_gap_x
            y = action_btn_start_y + row * action_btn_gap_y

            btn = Button(self.action_name[i],x,y,300,50,self.font,config.BLUE)
            self.action_btn.append(btn)
        self.all_action_select_btn = Button("全選",900,180,150,100,self.font,config.BLUE)   
        self.all_action_clear_btn = Button("清除",900,300,150,100,self.font,config.BLUE)
        
        self.break_time_btn = []
        self.train_time_btn = []
        self.action_time_btn = []
        
        time_btn_start_x = 500
        time_btn_gap = 70
        time_btn_y_break = 620
        time_btn_y_train = 690
        time_btn_y_action = 760

        for i,t in enumerate(self.time_options):

            x = time_btn_start_x + i * time_btn_gap

            self.break_time_btn.append(
                Button(str(t),x,time_btn_y_break,60,40,self.font,config.BLUE)
            )

            self.train_time_btn.append(
                Button(str(t),x,time_btn_y_train,60,40,self.font,config.BLUE)
            )

            self.action_time_btn.append(
                Button(str(t),x,time_btn_y_action,60,40,self.font,config.BLUE)
            )

        self.start_btn = Button("開始",config.WIDTH-300,config.HEIGHT-150,200,60,self.font,config.BLUE)
        self.menu_btn = Button("返回菜單",100,config.HEIGHT-150,200,60,self.font,config.BLUE)   
   

    def handle_event(self, event):
        for i, btn in enumerate(self.action_btn):
            if btn.is_clicked(event):
                action = Game1Action(i)
                if action in self.enabled_action:
                    self.enabled_action.remove(action)
                else:
                    self.enabled_action.append(action)

        # break time
        for i,btn in enumerate(self.break_time_btn):
            if btn.is_clicked(event):
                self.break_duration = self.time_options[i]

        # train time
        for i,btn in enumerate(self.train_time_btn):
            if btn.is_clicked(event):
                self.train_duration = self.time_options[i]

        # action time
        for i,btn in enumerate(self.action_time_btn):
            if btn.is_clicked(event):
                self.action_duration = self.time_options[i]

        if self.all_action_select_btn.is_clicked(event):
            self.enabled_action = list(Game1Action)
        if self.all_action_clear_btn.is_clicked(event):
            self.enabled_action.clear()

        if self.menu_btn.is_clicked(event):
            self.next_scene = {"name":"Menu"}
        if self.start_btn.is_clicked(event):
                if len(self.enabled_action) > 0:
                    self.get_action_value()
                    self.next_scene = {"name":"Game1",
                                    "enabled_action_indices":self.enabled_action_indices,
                                    "train_duration":self.train_duration,
                                    "action_duration":self.action_duration,
                                    "break_duration":self.break_duration}
        pass
    
    def update(self):
        pass
    
    def draw(self):
        self.screen.fill((40, 40, 40))
        self.draw_text("設置",config.WIDTH//2,41)
        self.draw_text("已選動作組",900,120,isCenter=False)
        self.draw_text(f"休息時間:{self.break_duration}秒",200,620,isCenter=False)
        self.draw_text(f"訓練時間:{self.train_duration}秒",200,690,isCenter=False)
        self.draw_text(f"動作時間:{self.action_duration}秒",200,760,isCenter=False)
        self.draw_enable_action_info()
        self.draw_action_button()
        self.draw_time_buttons()
        self.draw_alarm()
        self.start_btn.draw(self.screen)
        self.menu_btn.draw(self.screen)
        
    def draw_action_button(self):
        for i, btn in enumerate(self.action_btn):
            if Game1Action(i) in self.enabled_action:
                btn.color = (0,200,0)
            else:
                btn.color = config.BLUE
            btn.draw(self.screen)
        self.all_action_select_btn.draw(self.screen)
        self.all_action_clear_btn.draw(self.screen)

    def draw_enable_action_info(self):
        for i in range(len(self.enabled_action)):
            col = i // 8
            row = i % 8
            self.draw_text(f"{i+1}. {self.action_name[self.enabled_action[i].value]}",1100+col*350,178+row*52,isCenter=False)
    
    def draw_time_buttons(self):
        for i,btn in enumerate(self.break_time_btn):

            if self.break_duration == self.time_options[i]:
                btn.color = (0,200,0)
            else:
                btn.color = config.BLUE

            btn.draw(self.screen)

        for i,btn in enumerate(self.train_time_btn):

            if self.train_duration == self.time_options[i]:
                btn.color = (0,200,0)
            else:
                btn.color = config.BLUE

            btn.draw(self.screen)

        for i,btn in enumerate(self.action_time_btn):

            if self.action_duration == self.time_options[i]:
                btn.color = (0,200,0)
            else:
                btn.color = config.BLUE

            btn.draw(self.screen)  

    def draw_alarm(self):
        if len(self.enabled_action) == 0:
            self.draw_text("動作組不能為空!!",config.WIDTH-300,config.HEIGHT-200, isCenter=False)

    def get_action_value(self):
        for i in self.enabled_action:
            self.enabled_action_indices.append(i.value)
    def draw_text(self, text, x, y, color=(255,255,255), isCenter = True):
        surf = self.font.render(text, True, color)
        if isCenter:
            rect = surf.get_rect(center=(x,y))
            self.screen.blit(surf, rect)
        else:
            self.screen.blit(surf, (x, y))
class Game1Action(Enum):
    HH = 0
    VV = auto()
    VH = auto()
    HV = auto()
    CCWCW = auto()
    CCWCCW = auto()
    CWCCW = auto()
    CWCW = auto()
    VCW = auto()
    VCCW = auto()
    CCWV = auto()
    CWV = auto()
    HCCW = auto()
    CWH = auto()
    HCW = auto()
    CCWH = auto()