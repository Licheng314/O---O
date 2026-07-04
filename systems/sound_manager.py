"""
systems/sound_manager.py
音效加载与播放管理器
"""

import os
import pygame


class SoundManager:
    """加载和管理音效"""

    def __init__(self):
        self.sounds = {}
        self.enabled = True
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        except Exception:
            self.enabled = False
            print("警告：无法初始化音效系统")

    def load(self, name, path):
        """加载单个音效"""
        if self.enabled and os.path.exists(path):
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
            except Exception:
                self.sounds[name] = None
        else:
            self.sounds[name] = None

    def play(self, name):
        """播放音效"""
        if self.enabled and name in self.sounds and self.sounds[name]:
            try:
                self.sounds[name].play()
            except Exception:
                pass

    def load_all(self, sound_config):
        """从配置字典批量加载"""
        for name, path in sound_config.items():
            self.load(name, path)
