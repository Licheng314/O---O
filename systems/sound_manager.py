"""
systems/sound_manager.py
音效加载与播放管理器
"""

import os
import random
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

    def play_random(self, name, folder):
        """
        从文件夹中随机选一个 wav 播放。首次调用时加载文件夹中所有 wav。
        name: 缓存键（如 'anchor_attach'）
        folder: 文件夹路径（如 'arts/sounds/attach'）
        """
        if not self.enabled:
            return
        cache_key = f"_random_{name}"
        if cache_key not in self.sounds:
            # 首次：扫描文件夹加载所有 wav
            if os.path.isdir(folder):
                pool = []
                for f in sorted(os.listdir(folder)):
                    if f.lower().endswith('.wav'):
                        fp = os.path.join(folder, f)
                        try:
                            pool.append(pygame.mixer.Sound(fp))
                        except Exception:
                            pass
                self.sounds[cache_key] = pool if pool else None
            else:
                self.sounds[cache_key] = None
        pool = self.sounds.get(cache_key)
        if pool:
            random.choice(pool).play()

    def load_all(self, sound_config):
        """从配置字典批量加载"""
        for name, path in sound_config.items():
            self.load(name, path)
