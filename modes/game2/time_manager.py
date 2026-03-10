import pygame
import time
from .settings import *

class TimeManager:
    def __init__(self, play_time=10):
        self.start_flag = False
        self.initial_time = play_time
        # game time control
        self.start_time = None # 時間量測基準點
        self.count_time = 0 # record how long time passing.
        self.time_left = play_time # 剩餘時間 目標時間 - 經過的時間
        self.keep_next_call_time = None
        # marble control
        self.generate_marble_time = None
    # region game time control
    def get_remaining_time(self):
        return self.time_left

    def set_timer(self, time): # Game duration varies depending on game level.
        # unit(second)
        self.initial_time = time

    def reset_timer(self):
        self.start_flag = False
        self.start_time = None
        self.count_time = 0
        self.time_left = self.initial_time

    def start_timer(self):
        self.start_time = time.time()
        self.start_flag = True

    def stop_timer(self):
        self.start_flag = False
        self.keep_next_call_time = None

    def update_timer(self):
        if self.start_flag:
            this_time_call_time = time.time()
            if self.keep_next_call_time is None:
                self.count_time += this_time_call_time - self.start_time
            else:
                self.count_time += this_time_call_time - self.keep_next_call_time
            self.time_left = self.initial_time - self.count_time
            self.keep_next_call_time = this_time_call_time

            if self.time_left <= 0:
                pygame.event.post(GAME2_TIMER_ALERT)
                self.reset_timer()
                self.stop_timer()
    # endregion
    # region marble generate time control
    def generate_marble(self):
        this_time = time.time()
        if self.generate_marble_time is None or this_time - self.generate_marble_time >= 2:
            self.generate_marble_time = this_time
            pygame.event.post(MARBLE_GENERATE)
    # endregion



