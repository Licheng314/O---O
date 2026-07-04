"""
systems/image_manager.py
图片加载管理器
"""

import os
import pygame


class ImageManager:
    """加载和管理图片素材"""

    def __init__(self):
        self.images = {}

    def load(self, name, path, scale=None):
        """加载图片，不存在时创建占位"""
        if os.path.exists(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                if scale:
                    img = pygame.transform.scale(img, scale)
                self.images[name] = img
                return
            except Exception:
                pass
        self.images[name] = None

    def get(self, name):
        return self.images.get(name)

    def clear(self):
        self.images.clear()
