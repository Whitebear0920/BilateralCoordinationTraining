import pygame
import time
from . import settings

class TimeManager:
    def __init__(self, play_time=10):
        self.start_time = 0
        self.start_flag = False

        self.initial_time = play_time


    def set_timer(self, time): # Game duration varies depending on game level.
        # unit(second)
        self.initial_time = time

    def start_timer(self):
        self.start_time = time.time()
        self.start_flag = True

    def stop_timer(self):
        self.start_flag = False

    def reset_timer(self):
        self.start_time = 0

    def get_remaining_time(self):
        if self.start_flag:
            time_left = self.initial_time - (time.time() - self.start_time)
            if time_left <= 0:
                self.stop_timer()
                pygame.event.post(settings.GAME2_TIMER_ALERT)
            return time_left
        else:
            return self.initial_time


