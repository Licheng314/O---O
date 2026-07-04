"""
physics/gravity.py
重力配置与计算
"""

from data_config import GRAVITY_CONFIG


class Gravity:
    """重力管理器"""

    def __init__(self, scale=None):
        self.scale = scale if scale is not None else GRAVITY_CONFIG["gravity"]
        # y 轴向下为正（pygame 坐标系）
        self.vector = (0, 1)

    def apply(self, velocity_y, dt):
        """将重力应用到 y 速度分量"""
        return velocity_y + self.scale * dt
