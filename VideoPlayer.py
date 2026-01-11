import cv2
import pygame
import numpy as np

class VideoPlayer:
    def __init__(self, path, size, loop=False):
        self.cap = cv2.VideoCapture(path)
        if not self.cap.isOpened():
            raise FileNotFoundError(f"Video not found: {path}")

        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
        self.size = size
        self.loop = loop
        self.clock = pygame.time.Clock()
        self.surface = None
        self.finished = False

    def update(self):
        if self.finished:
            return

        ret, frame = self.cap.read()
        if not ret:
            if self.loop:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                return
            else:
                self.finished = True
                return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        surface = pygame.surfarray.make_surface(frame)
        self.surface = pygame.transform.scale(surface, self.size)

        self.clock.tick(self.fps)

    def draw(self, screen, pos=(0, 0)):
        if self.surface:
            screen.blit(self.surface, pos)

    def release(self):
        self.cap.release()
