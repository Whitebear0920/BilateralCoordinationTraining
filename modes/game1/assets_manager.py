import pygame
import os
from .video_player import VideoPlayer
import config

class AssetsManager:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ASSETS_DIR = "assets"

    images = {}
    sounds = {}
    fonts  = {}
    videos = {}

    # ========= pre =========
    @classmethod
    def preload(cls):
        print("[assets] Preloading assets...")

        # ---- Images ----
        cls._load_image("hand", "Image/Game1/hand.png")

        # ---- Sounds ----
        cls._load_sound("coin", "sound/coin.wav", volume=0.8)

        # ---- Fonts ----
        cls._load_font("main", "font/msjh.ttc", 36)

        # ---- video ----
        cls._load_video("CCWCCW", "video/CCWCCW.mov", size=(960,540), loop=True)
        cls._load_video("CCWCW", "video/CCWCW.mov", size=(960,540), loop=True)
        cls._load_video("CWCCW", "video/CWCCW.mov", size=(960,540), loop=True)
        cls._load_video("CWCW", "video/CWCW.mov", size=(960,540), loop=True)
        cls._load_video("VH", "video/VH.mp4", size=(960,540), loop=True)
        cls._load_video("HV", "video/VH.mp4", size=(960,540), loop=True, flip_x=False)
        cls._load_video("VCW", "video/VCW.mp4", size=(960,540), loop=True)
        cls._load_video("VCCW", "video/VCCW.mp4", size=(960,540), loop=True)
        cls._load_video("HCCW", "video/HCCW.mp4", size=(960,540), loop=True)
        cls._load_video("CCWV", "video/VCW.mp4", size=(960,540), loop=True, flip_x=False)
        cls._load_video("CWV", "video/VCCW.mp4", size=(960,540), loop=True, flip_x=False)
        cls._load_video("CWH", "video/HCCW.mp4", size=(960,540), loop=True, flip_x=False)
        cls._load_video("HH", "video/HH.mp4", size=(960,540), loop=True)
        cls._load_video("VV", "video/VV.mp4", size=(960,540), loop=True)
        cls._load_video("HCW", "video/HCW.mp4", size=(960,540), loop=True)
        cls._load_video("CCWH", "video/CCWH.mp4", size=(960,540), loop=True, flip_x=False)
        print("[assets] Preload finished.")

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