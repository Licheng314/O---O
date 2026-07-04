# UI显示设计.md

## 1. UI 设计目标

### 1.1 总体风格

本游戏的 UI 风格目标是：

```text
音游感 + 唯美感 + 极简锚点主题
```

关键词：

- 几何字体
- 细字体
- 浅色文字
- 柔和发光
- 霓虹脉冲
- 节奏闪光
- 黑白 / 蓝紫 / 青蓝对比
- 音游式反馈
- 钢琴键般优雅

---

## 2. 设计原则

### 2.1 音游感

音游感主要由以下部分共同决定：

| 组成 | 说明 |
|---|---|
| 字体 | 几何感、未来感、细长、干净 |
| 动效 | 脉冲、节奏闪光、呼吸光 |
| 色彩 | 青蓝、紫粉、白色、深色背景 |
| 反馈 | 抓住时瞬间闪光，抓空时失亮 |
| 排版 | 字距稍大，居中，留白充足 |

---

### 2.2 唯美感

唯美感主要由以下部分共同决定：

| 组成 | 说明 |
|---|---|
| 配色 | 浅色文字、低饱和蓝紫光 |
| 字重 | Light / Regular，避免过粗 |
| 光效 | 柔和发光，不刺眼 |
| 背景 | 深蓝黑、渐变、轻微粒子 |
| 节奏 | 动画慢而轻，不频繁抖动 |

---

### 2.3 核心美术规则

1. **不要使用系统默认字体。**
2. **标题必须有发光效果。**
3. **重要反馈必须有瞬间亮度变化。**
4. **游戏内 UI 不能遮挡棍子和墙壁。**
5. **中文 UI 优先保证清晰。**
6. **所有字体、颜色、特效参数集中配置。**
7. **美术设计师只修改 UI 配置和 `render.py`，不修改游戏逻辑。**

---

## 3. 字体设计

### 3.1 字体文件目录

所有字体统一放置在：

```text
arts/fonts/
```

推荐结构：

```text
arts/
    fonts/
        Exo2-Light.ttf
        Exo2-Regular.ttf
        Orbitron-Medium.ttf
        Rajdhani-SemiBold.ttf
        NotoSansSC-Light.ttf
        NotoSansSC-Regular.ttf
        PlayfairDisplay-Regular.ttf
```

---

### 3.2 推荐字体组合

#### 主标题字体

推荐：

```text
Exo 2 Light
```

用途：

- 游戏标题
- 主菜单标题
- 胜利标题
- 关卡大标题

风格：

- 细
- 未来感
- 柔和
- 唯美
- 不过度机械

备用：

```text
Orbitron Medium
```

更偏音游 / 科幻。

---

#### UI 数字字体

推荐：

```text
Rajdhani SemiBold
```

用途：

- 高度
- 时间
- 关卡编号
- 岩浆高度
- 速度提示

风格：

- 细长
- 数字美观
- 音游 UI 感强

---

#### 中文说明字体

推荐：

```text
Noto Sans SC Light
```

用途：

- 操作说明
- 教学文字
- 道具说明
- 暂停菜单

风格：

- 清晰
- 干净
- 现代
- 不抢画面

---

#### 优雅装饰字体

推荐：

```text
Playfair Display Regular
```

用途：

- 关卡副标题
- 胜利结算文案
- 章节名

风格：

- 钢琴键般优雅
- 古典音乐标题感
- 适合英文短句

---

## 4. 色彩设计

### 4.1 主色板

| 名称 | 颜色 | 用途 |
|---|---|---|
| Pure White | `#F8FFFF` | 主文字 |
| Ice Cyan | `#78F6FF` | 主发光 |
| Neon Cyan | `#00D9FF` | 强反馈 |
| Soft Purple | `#B58CFF` | 二级光晕 |
| Deep Navy | `#050914` | 背景 |
| Lava Orange | `#FF6A2A` | 岩浆警告 |
| Danger Red | `#FF3355` | 危险提示 |
| Goal Gold | `#FFE8A3` | 终点 / 胜利 |
| Piano Black | `#050505` | 钢琴风背景 |
| Piano White | `#F2F2EA` | 钢琴风文字 |

---

### 4.2 UI 色彩规则

#### 普通状态

```text
文字主体：Pure White
外发光：Ice Cyan
二级光晕：Soft Purple
```

#### 成功抓住

```text
文字主体：Pure White
强发光：Neon Cyan
短暂亮度爆发
```

#### 抓空

```text
文字主体：灰蓝
外发光减弱
短暂失亮
```

#### 危险

```text
文字主体：Danger Red
外发光：Lava Orange
短暂闪烁
```

#### 胜利

```text
文字主体：Goal Gold
外发光：Pure White
背景柔光扩散
```

---

## 5. UI 页面设计

### 5.1 主菜单

显示内容：

```text
O---O
PRESS SPACE
```

风格：

- 标题居中
- 字距稍大
- 青蓝霓虹发光
- 标题缓慢呼吸
- 每隔数秒轻微闪烁
- 背景深蓝黑
- 可以加入细线圆环或锚点光圈

推荐：

| 元素 | 字体 | 效果 |
|---|---|---|
| O---O | Exo 2 Light / Orbitron | NeonPulse |
| PRESS SPACE | Rajdhani | SoftBlink |

---

### 5.2 游戏内 UI

显示内容：

```text
HEIGHT 128M
LAVA RISING
STAGE 01
```

风格：

- 半透明
- 靠边放置
- 不遮挡主体
- 数字使用 Rajdhani
- 警告状态使用橙红色闪烁

推荐布局：

| 元素 | 位置 |
|---|---|
| 高度 | 左上角 |
| 关卡编号 | 右上角 |
| 岩浆警告 | 下方或岩浆附近 |
| 临时反馈 | 屏幕中心偏上 |

---

### 5.3 抓住反馈

当玩家成功抓住墙壁时，显示短暂反馈：

```text
ANCHOR!
```

效果：

- 出现时间短
- 快速放大
- 青蓝闪光
- 透明度快速淡出
- 可配合音效和小屏幕震动

---

### 5.4 抓空反馈

当玩家抓空时，显示：

```text
MISS
```

效果：

- 灰蓝色
- 发光减弱
- 轻微下坠动画
- 快速淡出

---

### 5.5 危险反馈

当碰到危险障碍物时，显示：

```text
BREAK!
```

效果：

- 红橙闪烁
- 快速抖动
- 发光短促
- 音效尖锐

---

### 5.6 胜利界面

显示内容：

```text
STAGE CLEAR
Anchor Secured
PRESS SPACE
```

风格：

- 金白色
- 柔和扩散光
- 优雅排版
- 副标题可使用 Playfair Display
- 背景可加入慢速光粒子

---

### 5.7 失败界面

显示内容：

```text
SINK
PRESS SPACE TO RETRY
```

风格：

- 暗红色
- 光效逐渐熄灭
- 背景被岩浆色覆盖
- 不使用过强闪烁

---

## 6. 特效设计

### 6.1 NeonPulse 霓虹脉冲

用途：

- 主标题
- 重要提示
- 抓住反馈

效果：

- 文字持续外发光
- 发光强度随时间变化
- 色彩在青蓝和紫色之间轻微变化

参数：

| 参数 | 说明 |
|---|---|
| base_alpha | 基础透明度 |
| pulse_speed | 脉冲速度 |
| pulse_strength | 脉冲强度 |
| glow_radius | 发光半径 |
| glow_color | 发光颜色 |
| secondary_glow_color | 二级光晕颜色 |

---

### 6.2 SoftBlink 柔和闪烁

用途：

- PRESS SPACE
- 教学提示
- 可交互提示

效果：

- 透明度缓慢变化
- 不刺眼
- 像呼吸灯

参数：

| 参数 | 说明 |
|---|---|
| min_alpha | 最小透明度 |
| max_alpha | 最大透明度 |
| blink_speed | 闪烁速度 |

---

### 6.3 RhythmFlash 节奏闪光

用途：

- 成功抓住
- 完美时机
- 关卡开始

效果：

- 瞬间变亮
- 外发光快速增强
- 迅速淡出
- 可与音效同步

参数：

| 参数 | 说明 |
|---|---|
| duration | 持续时间 |
| flash_color | 闪光颜色 |
| max_scale | 最大放大倍率 |
| fade_speed | 淡出速度 |

---

### 6.4 PianoShine 钢琴高光

用途：

- 胜利界面
- 关卡标题
- 优雅副标题

效果：

- 文字上有一条柔光扫过
- 黑白对比强
- 不闪烁
- 更像琴键反光

参数：

| 参数 | 说明 |
|---|---|
| shine_speed | 高光扫过速度 |
| shine_width | 高光宽度 |
| shine_alpha | 高光透明度 |
| base_color | 基础文字颜色 |

---

### 6.5 DangerFlicker 危险闪烁

用途：

- 岩浆接近
- 危险物触发
- 失败前警告

效果：

- 红橙快速闪烁
- 短促且不持续太久
- 可以轻微抖动

参数：

| 参数 | 说明 |
|---|---|
| flicker_speed | 闪烁速度 |
| jitter_amount | 抖动幅度 |
| warning_color | 警告颜色 |
| glow_color | 警告光颜色 |

---

## 7. render.py 封装设计

### 7.1 设计目标

`render.py` 是专门给 UI 和视觉特效使用的渲染模块。

它负责：

- 字体加载
- UI 文本绘制
- 霓虹发光文字
- 柔和闪烁文字
- 节奏闪光文字
- 钢琴高光文字
- 危险闪烁文字
- 统一颜色管理
- 统一 UI 动画参数

目标是：

```text
美术设计师只需要修改 render.py 中的视觉参数，
不需要改游戏逻辑代码。
```

---

### 7.2 render.py 不负责的内容

`render.py` 不应该负责：

- 棍子物理
- 墙壁移动逻辑
- 输入处理
- 地图解析
- 道具效果逻辑
- 胜负判定
- 岩浆上升逻辑

这些应由其它系统负责。

---

### 7.3 render.py 推荐职责

| 职责 | 说明 |
|---|---|
| load_fonts | 加载字体 |
| draw_text | 绘制普通文本 |
| draw_neon_text | 绘制霓虹文本 |
| draw_soft_blink_text | 绘制柔和闪烁文本 |
| draw_rhythm_flash_text | 绘制节奏闪光文本 |
| draw_piano_shine_text | 绘制钢琴高光文本 |
| draw_danger_text | 绘制危险闪烁文本 |
| draw_main_menu_ui | 绘制主菜单 |
| draw_game_ui | 绘制游戏内 UI |
| draw_result_ui | 绘制胜利 / 失败 UI |

---

## 8. render.py 文件设计示例

```python
# render.py
# ============================================================
# UI 与视觉特效渲染模块
# 
# 设计目标：
# 1. 所有字体、颜色、UI 特效参数集中管理
# 2. 美术设计师可以通过修改本文件调整 UI 风格
# 3. 游戏逻辑代码不直接处理文字特效
# ============================================================

import math
import random
import pygame


# ============================================================
# 字体路径配置
# ============================================================

FONT_PATHS = {
    # 主标题字体：唯美、未来感
    "title": "arts/fonts/Exo2-Light.ttf",

    # 备用标题字体：更强音游科技感
    "title_alt": "arts/fonts/Orbitron-Medium.ttf",

    # 数字与游戏内 UI 字体
    "ui": "arts/fonts/Rajdhani-SemiBold.ttf",

    # 中文提示字体
    "cn": "arts/fonts/NotoSansSC-Light.ttf",

    # 优雅副标题字体
    "elegant": "arts/fonts/PlayfairDisplay-Regular.ttf",
}


# ============================================================
# 颜色配置
# ============================================================

COLORS = {
    "pure_white": (248, 255, 255),
    "ice_cyan": (120, 246, 255),
    "neon_cyan": (0, 217, 255),
    "soft_purple": (181, 140, 255),
    "deep_navy": (5, 9, 20),
    "lava_orange": (255, 106, 42),
    "danger_red": (255, 51, 85),
    "goal_gold": (255, 232, 163),
    "piano_black": (5, 5, 5),
    "piano_white": (242, 242, 234),
    "miss_gray": (120, 145, 160),
}


# ============================================================
# 特效参数
# ============================================================

EFFECT_CONFIG = {
    "neon_pulse": {
        "base_alpha": 80,
        "pulse_strength": 120,
        "pulse_speed": 3.0,
        "glow_offsets": [14, 9, 5, 2],
        "primary_glow": "ice_cyan",
        "secondary_glow": "soft_purple",
        "flicker_chance": 0.015,
        "flicker_strength": 0.35,
    },

    "soft_blink": {
        "min_alpha": 90,
        "max_alpha": 230,
        "blink_speed": 2.0,
    },

    "rhythm_flash": {
        "duration": 0.45,
        "max_scale": 1.18,
        "fade_speed": 4.0,
        "flash_color": "neon_cyan",
    },

    "piano_shine": {
        "shine_speed": 120,
        "shine_width": 80,
        "shine_alpha": 90,
        "base_color": "piano_white",
        "line_color": "ice_cyan",
    },

    "danger_flicker": {
        "flicker_speed": 18.0,
        "jitter_amount": 3,
        "warning_color": "danger_red",
        "glow_color": "lava_orange",
    },
}


# ============================================================
# 字体加载
# ============================================================

class FontManager:
    def __init__(self):
        self.fonts = {}

    def load(self):
        self.fonts["title_large"] = pygame.font.Font(FONT_PATHS["title"], 96)
        self.fonts["title_medium"] = pygame.font.Font(FONT_PATHS["title"], 64)
        self.fonts["ui_large"] = pygame.font.Font(FONT_PATHS["ui"], 42)
        self.fonts["ui_medium"] = pygame.font.Font(FONT_PATHS["ui"], 30)
        self.fonts["ui_small"] = pygame.font.Font(FONT_PATHS["ui"], 22)
        self.fonts["cn_medium"] = pygame.font.Font(FONT_PATHS["cn"], 28)
        self.fonts["cn_small"] = pygame.font.Font(FONT_PATHS["cn"], 22)
        self.fonts["elegant"] = pygame.font.Font(FONT_PATHS["elegant"], 34)

    def get(self, name):
        return self.fonts[name]


# ============================================================
# 基础工具函数
# ============================================================

def color(name):
    return COLORS[name]


def render_text_surface(text, font, text_color):
    return font.render(text, True, text_color)


def blit_center(screen, surface, center_pos):
    rect = surface.get_rect(center=center_pos)
    screen.blit(surface, rect)
    return rect


# ============================================================
# 普通文字
# ============================================================

def draw_text(screen, text, font, pos, text_color="pure_white", center=False, alpha=255):
    surface = render_text_surface(text, font, color(text_color))
    surface.set_alpha(alpha)

    if center:
        return blit_center(screen, surface, pos)
    else:
        screen.blit(surface, pos)
        return surface.get_rect(topleft=pos)


# ============================================================
# 霓虹脉冲文字
# ============================================================

def draw_neon_text(screen, text, font, center_pos, time_seconds, text_color="pure_white"):
    cfg = EFFECT_CONFIG["neon_pulse"]

    pulse = (math.sin(time_seconds * cfg["pulse_speed"]) + 1.0) / 2.0
    glow_alpha = cfg["base_alpha"] + int(pulse * cfg["pulse_strength"])

    if random.random() < cfg["flicker_chance"]:
        glow_alpha = int(glow_alpha * cfg["flicker_strength"])

    primary = color(cfg["primary_glow"])
    secondary = color(cfg["secondary_glow"])

    # 二级紫色大光晕
    for offset in cfg["glow_offsets"]:
        glow = font.render(text, True, secondary)
        glow.set_alpha(max(10, glow_alpha // (offset + 1)))

        for dx, dy in [
            (-offset, 0), (offset, 0), (0, -offset), (0, offset),
            (-offset, -offset), (offset, -offset), (-offset, offset), (offset, offset)
        ]:
            rect = glow.get_rect(center=(center_pos[0] + dx, center_pos[1] + dy))
            screen.blit(glow, rect)

    # 青蓝主光晕
    for offset in cfg["glow_offsets"][1:]:
        glow = font.render(text, True, primary)
        glow.set_alpha(max(20, glow_alpha // max(1, offset // 2)))

        for dx, dy in [(-offset, 0), (offset, 0), (0, -offset), (0, offset)]:
            rect = glow.get_rect(center=(center_pos[0] + dx, center_pos[1] + dy))
            screen.blit(glow, rect)

    # 主文字
    main = font.render(text, True, color(text_color))
    rect = main.get_rect(center=center_pos)
    screen.blit(main, rect)

    return rect


# ============================================================
# 柔和闪烁文字
# ============================================================

def draw_soft_blink_text(screen, text, font, center_pos, time_seconds, text_color="pure_white"):
    cfg = EFFECT_CONFIG["soft_blink"]

    t = (math.sin(time_seconds * cfg["blink_speed"]) + 1.0) / 2.0
    alpha = int(cfg["min_alpha"] + t * (cfg["max_alpha"] - cfg["min_alpha"]))

    surface = font.render(text, True, color(text_color))
    surface.set_alpha(alpha)

    rect = surface.get_rect(center=center_pos)
    screen.blit(surface, rect)
    return rect


# ============================================================
# 节奏闪光文字
# ============================================================

def draw_rhythm_flash_text(screen, text, font, center_pos, elapsed_time, text_color="pure_white"):
    cfg = EFFECT_CONFIG["rhythm_flash"]

    if elapsed_time > cfg["duration"]:
        return None

    progress = elapsed_time / cfg["duration"]
    alpha = int(255 * (1.0 - progress))
    scale = 1.0 + (cfg["max_scale"] - 1.0) * (1.0 - progress)

    base = font.render(text, True, color(text_color))
    glow = font.render(text, True, color(cfg["flash_color"]))

    width = int(base.get_width() * scale)
    height = int(base.get_height() * scale)

    base = pygame.transform.smoothscale(base, (width, height))
    glow = pygame.transform.smoothscale(glow, (width + 20, height + 20))

    glow.set_alpha(alpha // 2)
    base.set_alpha(alpha)

    glow_rect = glow.get_rect(center=center_pos)
    base_rect = base.get_rect(center=center_pos)

    screen.blit(glow, glow_rect)
    screen.blit(base, base_rect)

    return base_rect


# ============================================================
# 钢琴高光文字
# ============================================================

def draw_piano_shine_text(screen, text, font, center_pos, time_seconds):
    cfg = EFFECT_CONFIG["piano_shine"]

    base = font.render(text, True, color(cfg["base_color"]))
    rect = base.get_rect(center=center_pos)

    # 阴影
    shadow = font.render(text, True, (20, 20, 24))
    shadow_rect = shadow.get_rect(center=(center_pos[0] + 2, center_pos[1] + 2))
    screen.blit(shadow, shadow_rect)

    # 主文字
    screen.blit(base, rect)

    # 下方细线，模拟钢琴键边缘
    line_y = rect.bottom + 8
    pygame.draw.line(
        screen,
        color(cfg["line_color"]),
        (rect.left, line_y),
        (rect.right, line_y),
        1
    )

    # 高光扫线
    shine_x = rect.left + int((time_seconds * cfg["shine_speed"]) % (rect.width + cfg["shine_width"])) - cfg["shine_width"]

    shine_surface = pygame.Surface((cfg["shine_width"], rect.height), pygame.SRCALPHA)
    pygame.draw.polygon(
        shine_surface,
        (255, 255, 255, cfg["shine_alpha"]),
        [
            (cfg["shine_width"] // 2, 0),
            (cfg["shine_width"], 0),
            (cfg["shine_width"] // 2, rect.height),
            (0, rect.height),
        ]
    )

    clipped = screen.get_clip()
    screen.set_clip(rect)
    screen.blit(shine_surface, (shine_x, rect.top))
    screen.set_clip(clipped)

    return rect


# ============================================================
# 危险闪烁文字
# ============================================================

def draw_danger_text(screen, text, font, center_pos, time_seconds):
    cfg = EFFECT_CONFIG["danger_flicker"]

    flicker = abs(math.sin(time_seconds * cfg["flicker_speed"]))
    alpha = int(120 + flicker * 135)

    jitter = cfg["jitter_amount"]
    offset_x = random.randint(-jitter, jitter)
    offset_y = random.randint(-jitter, jitter)

    glow = font.render(text, True, color(cfg["glow_color"]))
    glow.set_alpha(alpha // 2)

    main = font.render(text, True, color(cfg["warning_color"]))
    main.set_alpha(alpha)

    for dx, dy in [(-4, 0), (4, 0), (0, -4), (0, 4)]:
        rect = glow.get_rect(center=(center_pos[0] + dx + offset_x, center_pos[1] + dy + offset_y))
        screen.blit(glow, rect)

    rect = main.get_rect(center=(center_pos[0] + offset_x, center_pos[1] + offset_y))
    screen.blit(main, rect)

    return rect


# ============================================================
# UI 页面绘制
# ============================================================

def draw_main_menu_ui(screen, fonts, time_seconds):
    screen.fill(color("deep_navy"))

    draw_neon_text(
        screen,
        "O---O",
        fonts.get("title_large"),
        (screen.get_width() // 2, screen.get_height() // 2 - 80),
        time_seconds
    )

    draw_soft_blink_text(
        screen,
        "PRESS SPACE",
        fonts.get("ui_medium"),
        (screen.get_width() // 2, screen.get_height() // 2 + 60),
        time_seconds,
        text_color="ice_cyan"
    )


def draw_game_ui(screen, fonts, height_value, stage_id, lava_warning=False, time_seconds=0):
    # 高度
    draw_text(
        screen,
        f"HEIGHT {height_value}M",
        fonts.get("ui_medium"),
        (24, 20),
        text_color="pure_white"
    )

    # 关卡编号
    stage_text = f"STAGE {stage_id}"
    stage_surface = fonts.get("ui_medium").render(stage_text, True, color("pure_white"))
    screen.blit(stage_surface, (screen.get_width() - stage_surface.get_width() - 24, 20))

    # 岩浆警告
    if lava_warning:
        draw_danger_text(
            screen,
            "LAVA RISING",
            fonts.get("ui_large"),
            (screen.get_width() // 2, screen.get_height() - 90),
            time_seconds
        )


def draw_result_ui(screen, fonts, is_win, time_seconds):
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    if is_win:
        overlay.fill((5, 9, 20, 180))
        screen.blit(overlay, (0, 0))

        draw_neon_text(
            screen,
            "STAGE CLEAR",
            fonts.get("title_medium"),
            (screen.get_width() // 2, screen.get_height() // 2 - 80),
            time_seconds,
            text_color="goal_gold"
        )

        draw_piano_shine_text(
            screen,
            "Anchor Secured",
            fonts.get("elegant"),
            (screen.get_width() // 2, screen.get_height() // 2 + 10),
            time_seconds
        )

        draw_soft_blink_text(
            screen,
            "PRESS SPACE",
            fonts.get("ui_medium"),
            (screen.get_width() // 2, screen.get_height() // 2 + 100),
            time_seconds,
            text_color="ice_cyan"
        )

    else:
        overlay.fill((40, 5, 5, 190))
        screen.blit(overlay, (0, 0))

        draw_danger_text(
            screen,
            "SINK",
            fonts.get("title_medium"),
            (screen.get_width() // 2, screen.get_height() // 2 - 50),
            time_seconds
        )

        draw_soft_blink_text(
            screen,
            "PRESS SPACE TO RETRY",
            fonts.get("ui_medium"),
            (screen.get_width() // 2, screen.get_height() // 2 + 70),
            time_seconds,
            text_color="piano_white"
        )
```

---

## 9. 游戏主程序中如何调用 render.py

### 9.1 初始化

```python
import pygame
from render import FontManager

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

fonts = FontManager()
fonts.load()
```

---

### 9.2 主菜单调用

```python
from render import draw_main_menu_ui

time_seconds = pygame.time.get_ticks() / 1000.0
draw_main_menu_ui(screen, fonts, time_seconds)
```

---

### 9.3 游戏内 UI 调用

```python
from render import draw_game_ui

draw_game_ui(
    screen=screen,
    fonts=fonts,
    height_value=128,
    stage_id="01",
    lava_warning=True,
    time_seconds=time_seconds
)
```

---

### 9.4 结果界面调用

```python
from render import draw_result_ui

draw_result_ui(
    screen=screen,
    fonts=fonts,
    is_win=True,
    time_seconds=time_seconds
)
```

---

## 10. 美术设计师修改指南

### 10.1 修改字体

在 `render.py` 中修改：

```python
FONT_PATHS = {
    "title": "arts/fonts/Exo2-Light.ttf",
}
```

即可更换标题字体。

---

### 10.2 修改颜色

在 `render.py` 中修改：

```python
COLORS = {
    "ice_cyan": (120, 246, 255),
}
```

即可改变 UI 主发光颜色。

---

### 10.3 修改霓虹闪烁速度

在 `render.py` 中修改：

```python
EFFECT_CONFIG = {
    "neon_pulse": {
        "pulse_speed": 3.0,
    }
}
```

数值越大，闪烁越快。

---

### 10.4 修改发光范围

在 `render.py` 中修改：

```python
"glow_offsets": [14, 9, 5, 2]
```

数值越大，光晕越宽。

---

### 10.5 修改 PRESS SPACE 呼吸效果

在 `render.py` 中修改：

```python
"soft_blink": {
    "min_alpha": 90,
    "max_alpha": 230,
    "blink_speed": 2.0,
}
```

---

### 10.6 修改危险提示抖动

在 `render.py` 中修改：

```python
"danger_flicker": {
    "jitter_amount": 3,
}
```

---

## 11. 与数据驱动设计的关系

虽然 `render.py` 负责 UI 视觉表现，但仍然建议将长期稳定的数据放到 `data_config.py` 中。

推荐分工：

| 文件 | 负责内容 |
|---|---|
| `data_config.py` | 游戏数值、地图符号、素材路径、音效路径 |
| `render.py` | UI 字体、颜色、绘制函数、文字特效 |
| `main.py` | 游戏流程调用 |
| `stick.py` | 棍子物理 |
| `level_loader.py` | 地图解析 |
| `sound_system.py` | 音效播放 |

---

## 12. 开发注意事项

### 12.1 性能注意

Pygame 每帧渲染多层发光文字会有一定开销。

优化建议：

1. 主菜单和结算界面可以使用完整发光。
2. 游戏内 UI 尽量少用大面积发光。
3. 静态文字可以缓存 surface。
4. 小提示使用轻量透明度变化即可。
5. 发光层数不要过多。

---

### 12.2 可读性注意

不要为了特效牺牲可读性。

尤其是：

- 教学文字
- 失败重试提示
- 游戏内高度信息

这些内容应保持清晰。

---

### 12.3 闪烁安全

避免高频强闪烁。

建议：

- 危险闪烁持续时间短。
- 不要全屏快速闪白。
- UI 闪烁频率不要过高。
- 霓虹闪烁以呼吸式为主。

---

## 13. 最终 UI 风格总结

本游戏 UI 的核心方向是：

```text
用几何字体制造音游感，
用细字重和柔和光效制造唯美感，
用脉冲和节奏闪光强化锚点切换反馈。
```

最终目标：

- 主菜单像霓虹音乐游戏标题。
- 胜利界面像优雅的钢琴曲终章。
- 游戏内 UI 简洁、不干扰操作。
- 抓住和抓空反馈清晰、有节奏。
- 美术设计师可以通过修改 `render.py` 快速调整视觉效果。
