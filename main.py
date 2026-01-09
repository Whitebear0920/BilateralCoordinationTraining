import pygame
import Config

from Menu import MenuScene
from Game1 import Game1Scene
from Game1Result import Game1Result

from GestureManager import GestureManager
from AssetsManager import AssetsManager

def main():
    gesture_mgr = GestureManager()

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
    clock = pygame.time.Clock()

    AssetsManager.preload()

    #font = pygame.font.Font("font/msjh.ttc", 36)
    menu = MenuScene(screen)
    current = menu

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            current.handle_event(event)

        #Scene switch
        if isinstance(current.next_scene, dict):
            if current.next_scene["name"] == "Game1":
                gesture_mgr.start()
                current = Game1Scene(screen, gesture_mgr.api)
                print("Game1")
            elif current.next_scene["name"] == "Result":
                gesture_mgr.stop()
                current = Game1Result(screen, current.next_scene["data"])
                print("Result")
            elif current.next_scene["name"] == "Game2":
                gesture_mgr.stop()
                print("Game2")
            elif current.next_scene["name"] == "Menu":
                gesture_mgr.stop()
                current = menu
                print("Menu")
            elif current.next_scene["name"] == "Exit":
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