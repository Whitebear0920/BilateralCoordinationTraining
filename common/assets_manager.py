import pygame
import os
from modes.game1.video_player import VideoPlayer
import config

class AssetsManager:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ASSETS_DIR = "assets"

    scene_asset_loaded = False
    scene_asset_load_name = None

    images = {}
    sounds = {}
    fonts  = {}
    videos = {}

    # ========= pre =========
    @classmethod
    def load_common_assets(cls):
        print("[assets] Preloading Common assets...")
        # ---- Fonts ----
        cls._load_font("main", "font/msjh.ttc", 36)
        print("[assets] Common Preload finished.")

    @classmethod
    def load_game1_assets(cls):
        def load_game1():
            print("[assets] Preloading Game1 assets...]")
            # ---- Images ----
            cls._load_image("hand", "image/Game1/hand.png")
            # ---- Sounds ----
            cls._load_sound("coin", "sound/coin.wav", volume=0.8)
            # ---- video ----
            cls._load_video("CCWCCW", "video/CCWCCW.mov", size=(960, 540), loop=True)
            cls._load_video("CCWCW", "video/CCWCW.mov", size=(960, 540), loop=True)
            cls._load_video("CWCCW", "video/CWCCW.mov", size=(960, 540), loop=True)
            cls._load_video("CWCW", "video/CWCW.mov", size=(960, 540), loop=True)
            cls._load_video("VH", "video/VH.mp4", size=(960, 540), loop=True)
            cls._load_video("HV", "video/VH.mp4", size=(960, 540), loop=True, flip_x=False)
            cls._load_video("VCW", "video/VCW.mp4", size=(960, 540), loop=True)
            cls._load_video("VCCW", "video/VCCW.mp4", size=(960, 540), loop=True)
            cls._load_video("HCCW", "video/HCCW.mp4", size=(960, 540), loop=True)
            cls._load_video("CCWV", "video/VCW.mp4", size=(960, 540), loop=True, flip_x=False)
            cls._load_video("CWV", "video/VCCW.mp4", size=(960, 540), loop=True, flip_x=False)
            cls._load_video("CWH", "video/HCCW.mp4", size=(960, 540), loop=True, flip_x=False)
            cls._load_video("HH", "video/HH.mp4", size=(960, 540), loop=True)
            cls._load_video("VV", "video/VV.mp4", size=(960, 540), loop=True)
            cls._load_video("HCW", "video/HCW.mp4", size=(960, 540), loop=True)
            cls._load_video("CCWH", "video/CCWH.mp4", size=(960, 540), loop=True, flip_x=False)

            # 紀錄載入狀態
            cls.scene_asset_loaded = True
            cls.scene_asset_load_name = "Game1"
            print("[assets] Game1 Preload finished.")

        if not cls.scene_asset_loaded:
            load_game1()
        elif cls.scene_asset_load_name == "Game1":
            print("[assets] Game1 had loaded.")
        elif cls.scene_asset_load_name != "Game1":
            # unload and load
            cls._unload_current_scene()
            load_game1()

    @classmethod
    def load_game2_assets(cls):
        def load_game2():
            print("[assets] Preloading Game2 assets...]")
            cls._load_image("RED_SWORD", "image/game2/red_light_sword.png")
            cls._load_image("BLUE_SWORD", "image/game2/blue_light_sword.png")
            cls._load_image("RED_MARBLE", "image/game2/red_marble.png")
            cls._load_image("BLUE_MARBLE", "image/game2/blue_marble.png")
            cls._load_image("RED_MARBLE_BROKE", "image/game2/red_marble_broke.png")
            cls._load_image("BLUE_MARBLE_BROKE", "image/game2/blue_marble_broke.png")

            cls.scene_asset_loaded = True
            cls.scene_asset_load_name = "Game2"
            print("[assets] Game2 Preload finished.")
        if not cls.scene_asset_loaded:
            load_game2()
        elif cls.scene_asset_load_name == "Game2":
            print("[assets] Game1 had loaded.")
        elif cls.scene_asset_load_name != "Game2":
            # unload and load
            cls._unload_current_scene()
            load_game2()

    # ========= image =========
    @classmethod
    def _load_image(cls, key, path, scale=None, alpha=True):
        full = os.path.join(cls.ASSETS_DIR, path)
        if not os.path.exists(full):
            raise FileNotFoundError(f"image not found: {full}")

        img = pygame.image.load(full)
        img = img.convert_alpha() if alpha else img.convert()

        if scale:
            img = pygame.transform.smoothscale(img, scale)

        cls.images[key] = img

    @classmethod
    def get_image(cls, key, scale=None):
        img = cls.images[key]
        if scale:
            img = pygame.transform.smoothscale(img, scale)
        return img

    # ========= sound =========
    @classmethod
    def _load_sound(cls, key, path, volume=1.0):
        full = os.path.join(cls.ASSETS_DIR, path)
        if not os.path.exists(full):
            raise FileNotFoundError(f"sound not found: {full}")

        snd = pygame.mixer.Sound(full)
        snd.set_volume(volume)
        cls.sounds[key] = snd

    @classmethod
    def get_sound(cls, key):
        return cls.sounds[key]

    # ========= font =========
    @classmethod
    def _load_font(cls, key, path, size):
        full = os.path.join(cls.ASSETS_DIR, path)
        if not os.path.exists(full):
            raise FileNotFoundError(f"font not found: {full}")

        cls.fonts[key] = pygame.font.Font(full, size)

    @classmethod
    def get_font(cls, key):
        return cls.fonts[key]

    # ========= video =========
    @classmethod
    def _load_video(cls, key, path, size, loop=False, flip_x=True):
        full = os.path.join(cls.ASSETS_DIR, path)
        if not os.path.exists(full):
            raise FileNotFoundError(f"video not found: {full}")

        cls.videos[key] = VideoPlayer(full, size, loop, flip_x)
    
    @classmethod
    def get_video(cls, key):
        return cls.videos[key]

    @classmethod
    def _unload_current_scene(cls):
        """釋放當前場景的所有資源，避免記憶體洩漏"""
        print(f"[assets] Unloading scene: {cls.scene_asset_load_name}...")

        # 1. 影片必須優先釋放（尤其是如果有開啟 Thread 或 Camera）
        for video in cls.videos.values():
            if hasattr(video, 'release'):  # 假設你的 VideoPlayer 有 release 方法
                video.release()

        # 2. 清空字典
        cls.images.clear()
        cls.sounds.clear()
        cls.videos.clear()
        # 注意：fonts 通常很小，可以保留在 common，若要清空也可以
        cls.scene_asset_loaded = False
        cls.scene_asset_load_name = None

        # 3. 強制垃圾回收 (這對釋放大型影片緩存很有幫助)
        import gc
        gc.collect()
        print("[assets] Unload finished.")