"""
core/game_state.py
游戏状态枚举
"""

from enum import Enum


class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    WIN = "win"
    DEAD = "dead"
