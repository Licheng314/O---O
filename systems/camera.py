"""
systems/camera.py
平滑跟随相机系统 — 带死区（dead zone），避免微小抖动和边界跳变
"""

import random
from data_config import SCREEN_HEIGHT


class Camera:
    """
    平滑跟随相机。

    死区机制：
      玩家在死区范围内移动时，相机保持不动。
      只有玩家偏离理想位置超过 dead_zone 像素时，相机才会更新目标位置。
      这避免了：
        - 棍子锚定旋转时相机跟着圆周运动产生的微小抖动
        - 地图边界处 target 反复跳变

    参数
    ----
    y : float
        初始相机 Y 位置（世界坐标）
    map_height : float
        地图总高度（像素）
    dead_zone : float
        死区大小（像素），默认 80。玩家在此范围内移动不会触发相机跟随。
    """

    def __init__(self, y, map_height, dead_zone=80):
        self.y = y
        self.target_y = y
        self.map_height = map_height
        self.smooth_speed = 5.0
        self.dead_zone = dead_zone

    def set_target(self, follow_y):
        """
        设置跟踪目标（玩家世界 Y 坐标）。

        相机尽量将玩家放在屏幕上方约 35% 处。
        仅在理想位置偏离当前 target 超过 dead_zone 时才更新 target，
        避免微小移动导致的频繁调整。
        """
        # 理想相机位置：让玩家在屏幕上方约 1/3 处
        ideal = follow_y - SCREEN_HEIGHT * 0.35
        # 夹紧到地图范围，防止边界跳变
        max_y = max(0, self.map_height - SCREEN_HEIGHT)
        ideal = max(0.0, min(ideal, max_y))

        # 死区：理想位置偏离当前 target 超过阈值才更新
        if abs(ideal - self.target_y) > self.dead_zone:
            self.target_y = ideal

    def update(self, dt):
        """平滑移动相机（指数衰减逼近 target）"""
        diff = self.target_y - self.y
        self.y += diff * min(1.0, self.smooth_speed * dt)

    def apply_shake(self, amount=5):
        """屏幕震动"""
        self.y += random.uniform(-amount, amount)

    def world_to_screen(self, world_x, world_y):
        """世界坐标转屏幕坐标"""
        return (int(world_x), int(world_y - self.y))
