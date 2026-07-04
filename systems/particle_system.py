"""
systems/particle_system.py
粒子系统 — 管理火花和碎片粒子
"""

import math
import random
import pygame
from data_config import SCREEN_HEIGHT


class Particle:
    """单个粒子"""
    __slots__ = ('x', 'y', 'vx', 'vy', 'life', 'max_life', 'color', 'size')

    def __init__(self, x, y, vx, vy, life, color, size=2):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = color
        self.size = size

    def update(self, dt):
        self.life -= dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 300 * dt  # 粒子也受重力影响

    @property
    def alive(self):
        return self.life > 0

    @property
    def alpha(self):
        return max(0, min(255, int(255 * (self.life / self.max_life))))


class ParticleSystem:
    """粒子系统管理器"""

    def __init__(self):
        self.particles = []

    def emit_sparks(self, x, y, count, color, speed=200, life=0.4):
        """发射火花粒子"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            spd = random.uniform(speed * 0.5, speed)
            vx = math.cos(angle) * spd
            vy = math.sin(angle) * spd
            self.particles.append(
                Particle(x, y, vx, vy, random.uniform(life * 0.5, life), color,
                         random.randint(1, 3))
            )

    def emit_debris(self, x, y, count, color, speed=150, life=0.6):
        """发射碎片粒子"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            spd = random.uniform(speed * 0.3, speed)
            vx = math.cos(angle) * spd
            vy = math.sin(angle) * spd - random.uniform(0, 100)
            self.particles.append(
                Particle(x, y, vx, vy, random.uniform(life * 0.5, life), color,
                         random.randint(2, 5))
            )

    def update(self, dt):
        """更新所有粒子"""
        self.particles = [p for p in self.particles if p.alive]
        for p in self.particles:
            p.update(dt)

    def draw(self, screen, camera_y):
        """绘制所有粒子"""
        for p in self.particles:
            alpha = p.alpha
            screen_y = int(p.y - camera_y)
            if -20 < screen_y < SCREEN_HEIGHT + 20:
                try:
                    surf = pygame.Surface((p.size * 2, p.size * 2), pygame.SRCALPHA)
                    pygame.draw.circle(surf, (*p.color[:3], alpha),
                                       (p.size, p.size), p.size)
                    screen.blit(surf, (int(p.x - p.size), screen_y - p.size))
                except Exception:
                    pass

    def clear(self):
        self.particles.clear()
