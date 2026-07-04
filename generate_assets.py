"""
generate_assets.py
生成 O---O 游戏所需的所有美术素材（PNG）和音效素材（WAV）。
运行一次即可：python generate_assets.py
"""

import pygame
import math
import wave
import struct
import os

# ============================================================
# 初始化 pygame（仅用于 Surface 绘制，不创建窗口）
# ============================================================
pygame.init()

ARTS_DIR = "arts"

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


# ============================================================
# 辅助绘图函数
# ============================================================
def draw_circle_surface(size, color, outline_color=None, outline_width=0):
    """绘制一个带边框的圆形 Surface"""
    surf = pygame.Surface(size, pygame.SRCALPHA)
    cx, cy = size[0] // 2, size[1] // 2
    r = min(cx, cy) - outline_width
    if outline_color and outline_width > 0:
        pygame.draw.circle(surf, outline_color, (cx, cy), r + outline_width)
    pygame.draw.circle(surf, color, (cx, cy), r)
    # 添加高光
    highlight_r = r // 3
    if highlight_r > 2:
        pygame.draw.circle(surf, (255, 255, 255, 100), (cx - r//3, cy - r//3), highlight_r)
    return surf


def draw_gradient_rect(width, height, color_top, color_bottom):
    """绘制垂直渐变矩形"""
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    for y in range(height):
        t = y / height
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * t)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * t)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * t)
        a = 255
        if len(color_top) > 3:
            a = int(color_top[3] + ((color_bottom[3] if len(color_bottom) > 3 else 255) - color_top[3]) * t)
        pygame.draw.line(surf, (r, g, b, a), (0, y), (width, y))
    return surf


# ============================================================
# 生成棍子素材
# ============================================================
def generate_stick_assets():
    print("生成棍子素材...")
    ensure_dir(f"{ARTS_DIR}/stick")

    # 端点：24px 半径的白色圆形
    endpoint = draw_circle_surface((52, 52), (220, 220, 240), (150, 150, 170), 2)
    pygame.image.save(endpoint, f"{ARTS_DIR}/stick/endpoint.png")

    # 棍体：细长矩形（4px粗细，纹理化）
    rod = pygame.Surface((8, 128), pygame.SRCALPHA)
    for y in range(128):
        shade = 180 + int(40 * math.sin(y / 128 * math.pi))
        pygame.draw.line(rod, (shade, shade, shade + 20, 255), (1, y), (6, y))
    pygame.draw.rect(rod, (100, 100, 120, 255), (0, 0, 8, 128), 1)
    pygame.image.save(rod, f"{ARTS_DIR}/stick/rod.png")

    print("  端点图片已保存")
    print("  棍体图片已保存")


# ============================================================
# 生成墙壁素材
# ============================================================
def generate_wall_assets():
    print("生成墙壁素材...")
    ensure_dir(f"{ARTS_DIR}/walls")

    T = 32  # tile size

    # --- 普通墙壁：灰褐色方块，带砖缝纹理 ---
    normal = pygame.Surface((T, T), pygame.SRCALPHA)
    normal.fill((100, 85, 70))
    # 砖缝
    pygame.draw.line(normal, (70, 55, 40), (0, T // 2), (T, T // 2), 1)
    pygame.draw.line(normal, (70, 55, 40), (T // 2, 0), (T // 2, T // 2 - 1), 1)
    pygame.draw.line(normal, (70, 55, 40), (0, 0), (T, 0), 2)
    pygame.draw.line(normal, (70, 55, 40), (0, T - 1), (T, T - 1), 2)
    pygame.draw.line(normal, (70, 55, 40), (0, 0), (0, T), 2)
    pygame.draw.line(normal, (70, 55, 40), (T - 1, 0), (T - 1, T), 2)
    # 高光边缘
    pygame.draw.line(normal, (130, 115, 100), (1, 1), (T - 2, 1), 1)
    pygame.draw.line(normal, (130, 115, 100), (1, 1), (1, T - 2), 1)
    pygame.image.save(normal, f"{ARTS_DIR}/walls/normal_wall.png")

    # --- 终点墙壁：金色发光方块 ---
    goal = pygame.Surface((T, T), pygame.SRCALPHA)
    goal.fill((180, 150, 40))
    # 发光效果
    for i in range(4):
        alpha = 60 - i * 15
        pygame.draw.rect(goal, (255, 220, 60, alpha), (i, i, T - 2 * i, T - 2 * i), 1)
    pygame.draw.line(goal, (255, 240, 100), (4, 4), (T - 5, 4), 2)
    pygame.draw.line(goal, (255, 240, 100), (4, 4), (4, T - 5), 2)
    pygame.draw.line(goal, (100, 80, 20), (0, 0), (T, 0), 2)
    pygame.draw.line(goal, (100, 80, 20), (0, T - 1), (T, T - 1), 2)
    pygame.draw.line(goal, (100, 80, 20), (0, 0), (0, T), 2)
    pygame.draw.line(goal, (100, 80, 20), (T - 1, 0), (T - 1, T), 2)
    # 星星标记
    star_color = (255, 255, 200)
    cx, cy = T // 2, T // 2
    pygame.draw.line(goal, star_color, (cx, cy - 8), (cx, cy + 8), 2)
    pygame.draw.line(goal, star_color, (cx - 8, cy), (cx + 8, cy), 2)
    pygame.draw.line(goal, star_color, (cx - 6, cy - 6), (cx + 6, cy + 6), 1)
    pygame.draw.line(goal, star_color, (cx + 6, cy - 6), (cx - 6, cy + 6), 1)
    pygame.image.save(goal, f"{ARTS_DIR}/walls/goal_wall.png")

    # --- 脆弱墙壁：灰色带裂纹 ---
    fragile = pygame.Surface((T, T), pygame.SRCALPHA)
    fragile.fill((130, 120, 110))
    # 裂纹
    crack_color = (40, 35, 30)
    pygame.draw.line(fragile, crack_color, (4, 10), (10, 6), 1)
    pygame.draw.line(fragile, crack_color, (10, 6), (18, 14), 1)
    pygame.draw.line(fragile, crack_color, (18, 14), (22, 22), 1)
    pygame.draw.line(fragile, crack_color, (22, 22), (15, 24), 1)
    pygame.draw.line(fragile, crack_color, (15, 24), (8, 20), 1)
    pygame.draw.line(fragile, crack_color, (8, 20), (3, 18), 1)
    # 边框
    pygame.draw.rect(fragile, (80, 70, 60), (0, 0, T, T), 1)
    pygame.image.save(fragile, f"{ARTS_DIR}/walls/fragile_wall.png")

    print("  普通墙壁已保存")
    print("  终点墙壁已保存")
    print("  脆弱墙壁已保存")


# ============================================================
# 生成道具素材
# ============================================================
def generate_item_assets():
    print("生成道具素材...")
    ensure_dir(f"{ARTS_DIR}/items")

    T = 32

    # --- 危险障碍物：红色尖刺 ---
    hazard = pygame.Surface((T, T), pygame.SRCALPHA)
    # 红色圆形背景
    pygame.draw.circle(hazard, (200, 40, 30), (T // 2, T // 2), T // 2 - 2)
    pygame.draw.circle(hazard, (240, 60, 40), (T // 2, T // 2), T // 2 - 2, 2)
    # 尖刺符号
    spike_color = (255, 200, 50)
    cx, cy = T // 2, T // 2
    for angle in [0, math.pi / 2, math.pi, 3 * math.pi / 2]:
        ex = cx + int(10 * math.cos(angle))
        ey = cy + int(10 * math.sin(angle))
        pygame.draw.line(hazard, spike_color, (cx, cy), (ex, ey), 3)
    pygame.image.save(hazard, f"{ARTS_DIR}/items/hazard.png")

    # --- 增长道具：绿色圆形 + 加号 ---
    length_up = pygame.Surface((T, T), pygame.SRCALPHA)
    pygame.draw.circle(length_up, (40, 170, 60), (T // 2, T // 2), T // 2 - 2)
    pygame.draw.circle(length_up, (80, 210, 100), (T // 2, T // 2), T // 2 - 2, 2)
    # 加号
    pygame.draw.rect(length_up, (255, 255, 255), (T // 2 - 2, T // 2 - 9, 4, 18))
    pygame.draw.rect(length_up, (255, 255, 255), (T // 2 - 9, T // 2 - 2, 18, 4))
    pygame.image.save(length_up, f"{ARTS_DIR}/items/length_up.png")

    # --- 缩短道具：橙色圆形 + 减号 ---
    length_down = pygame.Surface((T, T), pygame.SRCALPHA)
    pygame.draw.circle(length_down, (200, 120, 30), (T // 2, T // 2), T // 2 - 2)
    pygame.draw.circle(length_down, (240, 150, 50), (T // 2, T // 2), T // 2 - 2, 2)
    pygame.draw.rect(length_down, (255, 255, 255), (T // 2 - 9, T // 2 - 2, 18, 4))
    pygame.image.save(length_down, f"{ARTS_DIR}/items/length_down.png")

    # --- 加速道具：蓝色圆形 + 双箭头 ---
    speed_up = pygame.Surface((T, T), pygame.SRCALPHA)
    pygame.draw.circle(speed_up, (40, 100, 200), (T // 2, T // 2), T // 2 - 2)
    pygame.draw.circle(speed_up, (80, 150, 240), (T // 2, T // 2), T // 2 - 2, 2)
    # >> 符号
    arrow_color = (255, 255, 255)
    for i, bx in enumerate([T // 2 - 5, T // 2 + 1]):
        pygame.draw.polygon(speed_up, arrow_color, [
            (bx - 4, T // 2 - 7),
            (bx + 3, T // 2),
            (bx - 4, T // 2 + 7),
        ])
    pygame.image.save(speed_up, f"{ARTS_DIR}/items/speed_up.png")

    # --- 减速道具：紫色圆形 + 双左箭头 ---
    speed_down = pygame.Surface((T, T), pygame.SRCALPHA)
    pygame.draw.circle(speed_down, (150, 50, 180), (T // 2, T // 2), T // 2 - 2)
    pygame.draw.circle(speed_down, (190, 90, 220), (T // 2, T // 2), T // 2 - 2, 2)
    # << 符号
    for i, bx in enumerate([T // 2 - 1, T // 2 + 5]):
        pygame.draw.polygon(speed_down, arrow_color, [
            (bx + 4, T // 2 - 7),
            (bx - 3, T // 2),
            (bx + 4, T // 2 + 7),
        ])
    pygame.image.save(speed_down, f"{ARTS_DIR}/items/speed_down.png")

    print("  道具素材已保存")


# ============================================================
# 生成岩浆素材
# ============================================================
def generate_lava_assets():
    print("生成岩浆素材...")
    ensure_dir(f"{ARTS_DIR}/lava")

    W, H = 64, 48
    lava = pygame.Surface((W, H), pygame.SRCALPHA)

    # 岩浆渐变：深红 → 橙红 → 黄
    for y in range(H):
        t = y / H
        if t < 0.3:
            r = int(180 + 75 * (t / 0.3))
            g = int(20 + 60 * (t / 0.3))
            b = int(5 + 20 * (t / 0.3))
        elif t < 0.7:
            r = 255
            g = int(80 + 120 * ((t - 0.3) / 0.4))
            b = int(25 + 60 * ((t - 0.3) / 0.4))
        else:
            r = 255
            g = int(200 + 55 * ((t - 0.7) / 0.3))
            b = int(85 + 80 * ((t - 0.7) / 0.3))

        # 波浪效果
        wave_offset = int(4 * math.sin(y / 6 + 0) + 3 * math.sin(y / 3 + 1))
        for x in range(W):
            shade = 1.0 + 0.1 * math.sin(x / 5 + y / 4)
            rr = min(255, int(r * shade))
            gg = min(255, int(g * shade))
            bb = min(255, int(b * shade))
            lava.set_at((x, y), (rr, gg, bb, 255))

    # 顶部泡沫效果
    for x in range(W):
        foam_y = int(3 * math.sin(x / 8) + 2 * math.sin(x / 3))
        for fy in range(max(0, foam_y - 2), min(H, foam_y + 3)):
            lava.set_at((x, fy), (255, 200, 100, 200))

    pygame.image.save(lava, f"{ARTS_DIR}/lava/lava.png")
    print("  岩浆素材已保存")


# ============================================================
# 生成背景素材
# ============================================================
def generate_background_assets():
    print("生成背景素材...")
    ensure_dir(f"{ARTS_DIR}/backgrounds")

    W, H = 800, 600

    # --- 菜单背景：深空背景 ---
    menu_bg = pygame.Surface((W, H))
    menu_bg.fill((10, 8, 20))
    # 星星
    import random
    random.seed(42)
    for _ in range(120):
        x = random.randint(0, W - 1)
        y = random.randint(0, H - 1)
        brightness = random.randint(80, 220)
        size = random.randint(1, 3)
        if size == 1:
            menu_bg.set_at((x, y), (brightness, brightness, brightness))
        else:
            pygame.draw.circle(menu_bg, (brightness, brightness, brightness), (x, y), size - 1)
    # 底部微光
    for y in range(H - 80, H):
        alpha = (y - (H - 80)) / 80
        c = int(30 * alpha)
        pygame.draw.line(menu_bg, (c, c // 2, c // 4), (0, y), (W, y))
    pygame.image.save(menu_bg, f"{ARTS_DIR}/backgrounds/menu_bg.png")

    # --- 关卡背景：深蓝灰洞穴背景 ---
    level_bg = pygame.Surface((W, H))
    level_bg.fill((15, 12, 25))
    random.seed(123)
    # 暗星 / 尘埃
    for _ in range(80):
        x = random.randint(0, W - 1)
        y = random.randint(0, H - 1)
        b = random.randint(40, 100)
        level_bg.set_at((x, y), (b, b, b + 20))
    # 底部暖光（岩浆反射）
    for y in range(H - 60, H):
        t = (y - (H - 60)) / 60
        r = int(40 * t)
        g = int(10 * t)
        pygame.draw.line(level_bg, (r, g, 0), (0, y), (W, y))
    pygame.image.save(level_bg, f"{ARTS_DIR}/backgrounds/level_01_bg.png")

    print("  背景素材已保存")


# ============================================================
# 音效生成（使用 wave 模块生成简单正弦波音效）
# ============================================================
def generate_sine_wav(filename, frequency, duration, sample_rate=44100, volume=0.5,
                       freq_end=None, volume_decay=True):
    """生成正弦波 WAV 文件，支持频率滑动"""
    n_samples = int(sample_rate * duration)
    with wave.open(filename, 'w') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        for i in range(n_samples):
            t = i / sample_rate
            progress = i / n_samples

            # 频率滑动
            if freq_end is not None:
                freq = frequency + (freq_end - frequency) * progress
            else:
                freq = frequency

            # 音量衰减
            if volume_decay:
                vol = volume * (1.0 - progress)
            else:
                vol = volume

            # 应用 ADSR 包络（简化：attack + decay）
            if progress < 0.02:
                vol *= progress / 0.02  # attack
            elif progress > 0.7:
                vol *= (1.0 - progress) / 0.3  # release

            value = int(vol * 32767 * math.sin(2 * math.pi * freq * t))
            value = max(-32767, min(32767, value))
            wav.writeframes(struct.pack('<h', value))


def generate_sound_assets():
    print("生成音效素材...")
    ensure_dir(f"{ARTS_DIR}/sounds")

    SR = 22050  # 采样率，节省空间

    # 抓住普通墙壁：短促高音
    generate_sine_wav(f"{ARTS_DIR}/sounds/anchor_success.wav", 660, 0.12, SR, 0.4)
    print("  anchor_success.wav")

    # 抓空：低沉音
    generate_sine_wav(f"{ARTS_DIR}/sounds/anchor_miss.wav", 180, 0.25, SR, 0.35)
    print("  anchor_miss.wav")

    # 抓住脆弱墙壁：带颤音
    generate_sine_wav(f"{ARTS_DIR}/sounds/anchor_fragile.wav", 500, 0.15, SR, 0.35, 400)
    print("  anchor_fragile.wav")

    # 墙壁碎裂：噪音感（用快速下降音模拟）
    generate_sine_wav(f"{ARTS_DIR}/sounds/wall_break.wav", 800, 0.3, SR, 0.4, 100)
    print("  wall_break.wav")

    # 胜利：上行音阶
    generate_sine_wav(f"{ARTS_DIR}/sounds/goal.wav", 440, 0.15, SR, 0.5, 880, False)
    generate_sine_wav(f"{ARTS_DIR}/sounds/goal2.wav", 880, 0.3, SR, 0.5, 1320, False)
    # 拼接成完整胜利音效
    goal_wav = wave.open(f"{ARTS_DIR}/sounds/goal.wav", 'rb')
    goal2_wav = wave.open(f"{ARTS_DIR}/sounds/goal2.wav", 'rb')
    combined = wave.open(f"{ARTS_DIR}/sounds/goal_combined.wav", 'w')
    combined.setnchannels(1)
    combined.setsampwidth(2)
    combined.setframerate(SR)
    combined.writeframes(goal_wav.readframes(goal_wav.getnframes()))
    combined.writeframes(goal2_wav.readframes(goal2_wav.getnframes()))
    goal_wav.close()
    goal2_wav.close()
    combined.close()
    os.replace(f"{ARTS_DIR}/sounds/goal_combined.wav", f"{ARTS_DIR}/sounds/goal.wav")
    os.remove(f"{ARTS_DIR}/sounds/goal2.wav")
    print("  goal.wav")

    # 碰到危险物：尖锐警告音
    generate_sine_wav(f"{ARTS_DIR}/sounds/hazard.wav", 900, 0.2, SR, 0.3, 200)
    print("  hazard.wav")

    # 长度增加：上升叮咚
    generate_sine_wav(f"{ARTS_DIR}/sounds/length_up.wav", 523, 0.12, SR, 0.35, 784)
    print("  length_up.wav")

    # 长度缩短：下降叮咚
    generate_sine_wav(f"{ARTS_DIR}/sounds/length_down.wav", 784, 0.12, SR, 0.35, 523)
    print("  length_down.wav")

    # 速度增加：快速哔哔
    generate_sine_wav(f"{ARTS_DIR}/sounds/speed_up.wav", 600, 0.08, SR, 0.3, 900)
    print("  speed_up.wav")

    # 速度减少：慢速哔哔
    generate_sine_wav(f"{ARTS_DIR}/sounds/speed_down.wav", 600, 0.15, SR, 0.3, 300)
    print("  speed_down.wav")

    # 岩浆死亡：低音下沉
    generate_sine_wav(f"{ARTS_DIR}/sounds/lava_death.wav", 300, 0.6, SR, 0.5, 40)
    print("  lava_death.wav")

    # 游戏开始：激昂短音
    generate_sine_wav(f"{ARTS_DIR}/sounds/game_start.wav", 330, 0.1, SR, 0.4, 660, False)
    print("  game_start.wav")

    # 重开：简短音
    generate_sine_wav(f"{ARTS_DIR}/sounds/restart.wav", 440, 0.08, SR, 0.3)
    print("  restart.wav")


# ============================================================
# 主函数
# ============================================================
def main():
    print("=" * 50)
    print("O---O 游戏素材生成器")
    print("=" * 50)
    print()

    generate_stick_assets()
    print()
    generate_wall_assets()
    print()
    generate_item_assets()
    print()
    generate_lava_assets()
    print()
    generate_background_assets()
    print()
    generate_sound_assets()

    print()
    print("=" * 50)
    print("所有素材生成完毕！")
    print("=" * 50)
    pygame.quit()


if __name__ == "__main__":
    main()
