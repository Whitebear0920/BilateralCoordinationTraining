import pygame


class ScoreManager:
    def __init__(self):
        self.score = 0

    def add_score(self, score):
        self.score += score

    def decrease_score(self, score):
        self.score -= score

    def reset_score(self, score):
        self.score = 0

    def get_score(self):
        return self.score
