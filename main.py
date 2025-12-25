import pygame
import Config
from Menu import MenuScene

pygame.init()
screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
clock = pygame.time.Clock()

button_font = pygame.font.Font("font/msjh.ttc", 36)
print(button_font)
menu = MenuScene(screen,button_font)

current = menu

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        current.handle_event(event)

    #Scene switch
    if hasattr(current, "next_scene") and current.next_scene:
        if current.next_scene == "Game1":
            print("Game1")
        elif current.next_scene == "Game2":
            print("Game2")
        elif current.next_scene == "Exit":
            print("Exit")
            break
        current.next_scene = None

    current.update()
    current.draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()