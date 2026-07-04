"""
entities/hazard.py
Hazard 危险物实体
"""

import pygame
from data_config import TILE_SIZE


class Hazard:
    """危险物实体 — 碰到后棍子强制脱锚"""

    def __init__(self, config):
        self.id = config.get("id", "hazard_?")
        pos = config.get("position", [0, 0])
        self.x = pos[0] if isinstance(pos, (list, tuple)) else pos.x
        self.y = pos[1] if isinstance(pos, (list, tuple)) else pos.y
        self.width = config.get("width", config.get("size", TILE_SIZE))
        self.height = config.get("height", config.get("size", TILE_SIZE))

        self.active = True
        self.appearance = config.get("appearance")
        self.prefab = config.get("prefab", "spike")

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.width), int(self.height))

    def contains_point(self, x, y):
        return self.rect.collidepoint(x, y)

    def trigger(self, stick):
        """触发危险物：强制脱锚"""
        if not self.active:
            return False
        stick.force_detach()
        return True

    def __repr__(self):
        return f"Hazard(id={self.id}, prefab={self.prefab}, pos=({self.x},{self.y}), active={self.active})"
