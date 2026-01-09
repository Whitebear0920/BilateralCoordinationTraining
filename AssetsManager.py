import pygame
import os

class AssetsManager:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ASSETS_DIR = os.path.join(BASE_DIR, "Assets")

    images = {}
    sounds = {}
    fonts  = {}

    # ========= pre =========
    @classmethod
    def preload(cls):
        print("[Assets] Preloading assets...")

        # ---- Images ----
        cls._load_image("hand", "Image/Game1/hand.png")

        # ---- Sounds ----
        cls._load_sound("coin", "Sound/coin.wav", volume=0.8)

        # ---- Fonts ----
        cls._load_font("main", "Font/msjh.ttc", 36)

        print("[Assets] Preload finished.")

    # ========= Image =========
    @classmethod
    def _load_image(cls, key, path, scale=None, alpha=True):
        full = os.path.join(cls.ASSETS_DIR, path)
        if not os.path.exists(full):
            raise FileNotFoundError(f"Image not found: {full}")

        img = pygame.image.load(full)
        img = img.convert_alpha() if alpha else img.convert()

        if scale:
            img = pygame.transform.smoothscale(img, scale)

        cls.images[key] = img

    @classmethod
    def get_image(cls, key, scale):
        img = cls.images[key]
        if scale:
            img = pygame.transform.smoothscale(img, scale)
        return img

    # ========= Sound =========
    @classmethod
    def _load_sound(cls, key, path, volume=1.0):
        full = os.path.join(cls.ASSETS_DIR, path)
        if not os.path.exists(full):
            raise FileNotFoundError(f"Sound not found: {full}")

        snd = pygame.mixer.Sound(full)
        snd.set_volume(volume)
        cls.sounds[key] = snd

    @classmethod
    def get_sound(cls, key):
        return cls.sounds[key]

    # ========= Font =========
    @classmethod
    def _load_font(cls, key, path, size):
        full = os.path.join(cls.ASSETS_DIR, path)
        if not os.path.exists(full):
            raise FileNotFoundError(f"Font not found: {full}")

        cls.fonts[key] = pygame.font.Font(full, size)

    @classmethod
    def get_font(cls, key):
        return cls.fonts[key]
