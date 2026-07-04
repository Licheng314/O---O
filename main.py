"""
main.py
O---O 游戏入口

一键物理攀登游戏 — 按空格键切换棍子锚点，向上攀登躲避岩浆！

重构后 main.py 只负责启动游戏。
游戏逻辑 → core/game.py
棍子系统 → entities/stick.py
关卡系统 → level/level.py
关卡加载 → level/level_loader.py
粒子系统 → systems/particle_system.py
音效系统 → systems/sound_manager.py
图片管理 → systems/image_manager.py
相机系统 → systems/camera.py
输入管理 → core/input_manager.py
状态枚举 → core/game_state.py
事件总线 → core/event_bus.py
UI 渲染 → render.py
配置数据 → data_config.py
地图数据 → maps/level1/
"""

from core.game import Game

if __name__ == "__main__":
    game = Game()
    game.run()
