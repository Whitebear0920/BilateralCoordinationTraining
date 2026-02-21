import pygame
import config
import multiprocessing as mp

from modes.meau import MenuScene
from modes.game1 import Game1Scene
from modes.game1 import Game1Result
from common import AssetsManager

from modes.game2 import Game2Scene

from common import GestureManager

def main():
    gesture_mgr = GestureManager()

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    clock = pygame.time.Clock()
    # load common asset
    AssetsManager.load_common_assets()
    #font = pygame.font.font("font/msjh.ttc", 36)
    menu = MenuScene(screen)

    # default scene setting
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
                AssetsManager.load_game1_assets()
                gesture_mgr.start("Game1")
                current = Game1Scene(screen, gesture_mgr.api)
                print("Game1")
            elif current.next_scene["name"] == "Result":
                gesture_mgr.stop()
                current = Game1Result(screen, current.next_scene["data"])
                print("Result")
            elif current.next_scene["name"] == "Game2":
                if gesture_mgr.state == "start":
                    gesture_mgr.stop()
                gesture_mgr.start("Game2")
                AssetsManager.load_game2_assets()
                current = Game2Scene(screen)
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
    mp.freeze_support()
    mp.set_start_method("spawn", force=True)
    main()