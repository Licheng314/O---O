"""
core/event_bus.py
简单发布/订阅事件总线 — 解耦游戏事件（音效、粒子、UI 气泡等）
"""


class EventBus:
    """轻量级事件总线"""

    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_name, callback):
        """订阅事件"""
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(callback)

    def unsubscribe(self, event_name, callback):
        """取消订阅"""
        if event_name in self._listeners:
            self._listeners[event_name] = [
                cb for cb in self._listeners[event_name] if cb != callback
            ]

    def emit(self, event_name, data=None):
        """发布事件"""
        for callback in self._listeners.get(event_name, []):
            callback(data)

    def clear(self):
        """清除所有监听器"""
        self._listeners.clear()


# 全局单例
event_bus = EventBus()
