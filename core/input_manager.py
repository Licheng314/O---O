"""
core/input_manager.py
输入管理器 — 将 Pygame 事件转换为游戏内部事件
"""

import pygame


class InputManager:
    """将 Pygame 原始事件转换为游戏内部事件名"""

    KEY_MAP = {
        pygame.K_SPACE: "space",
        pygame.K_ESCAPE: "quit",
        pygame.K_F3: "toggle_debug",
        pygame.K_r: "restart",
        pygame.K_p: "test_level",
    }

    def __init__(self):
        self.r_press_time = None  # 追踪 R 键按住时长

    def poll(self):
        """轮询事件，返回游戏内部事件名列表"""
        events = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events.append("quit")

            elif event.type == pygame.KEYDOWN:
                mapped = self.KEY_MAP.get(event.key)
                if mapped:
                    events.append(mapped)
                if event.key == pygame.K_r:
                    import time
                    self.r_press_time = time.time()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    self.r_press_time = None
                    events.append("restart_short")

        return events

    def r_held_seconds(self):
        """返回 R 键已按住秒数"""
        import time
        if self.r_press_time is None:
            return 0.0
        return time.time() - self.r_press_time
