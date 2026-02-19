import pygame


class ScoreManager:
    def __init__(self):
        self.score = 0

    def increase_score(self, score):
        self.score += 1

    def decrease_score(self, score):
        self.score -= 1

    def reset_score(self, score):
        self.score = 0

    def get_score(self):
        return(self.score)
