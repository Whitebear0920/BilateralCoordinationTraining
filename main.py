import pygame
import Config

from Menu import MenuScene
from Game1 import Game1Scene

from GestureManager import GestureManager
def main():
    gesture_mgr = GestureManager()

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
    clock = pygame.time.Clock()

    font = pygame.font.Font("font/msjh.ttc", 36)
    print(font)
    menu = MenuScene(screen,font)
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
                gesture_mgr.start()
                current = Game1Scene(screen, font, gesture_mgr.api)
                print("Game1")
            elif current.next_scene == "Game2":
                gesture_mgr.stop()
                print("Game2")
            elif current.next_scene == "Menu":
                gesture_mgr.stop()
                current = menu
                print("Menu")
            elif current.next_scene == "Exit":
                gesture_mgr.stop()
                print("Exit")
                break
            
            current.next_scene = None

        current.update()
        current.draw()
        pygame.display.flip()
        clock.tick(60)
    gesture_mgr.stop()
    pygame.quit()

if __name__ == "__main__":
    main()