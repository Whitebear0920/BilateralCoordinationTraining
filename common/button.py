import pygame
import colorsys
from config import BLUE, WHITE

class Button:
    def __init__(self, text, x, y, width, height, font, color = "BLUE"):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font

        self.color = color
        self.hover_color = self._adjust_brightness(self.color, 1.2)

    @staticmethod
    def _adjust_brightness(rgb, factor):
        # 1. 將 RGB 轉換為 0-1 之間的比例
        r, g, b = [x / 255.0 for x in rgb]

        # 2. 轉為 HLS (Hue, Lightness, Saturation)
        h, l, s = colorsys.rgb_to_hls(r, g, b)

        # 3. 調整亮度 (L)，確保不超過 1.0
        new_l = min(1.0, l * factor)

        # 4. 轉回 RGB 並還原為 0-255
        new_r, new_g, new_b = colorsys.hls_to_rgb(h, new_l, s)
        return (int(new_r * 255), int(new_g * 255), int(new_b * 255))

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN and
            event.button == 1 and
            self.rect.collidepoint(event.pos)
        )
