# 《O---O游戏设计大纲.md》

## 1. 游戏概述

### 1.1 游戏名称

**O---O**

### 1.2 游戏类型

- 2D 竖直攀登游戏
- 一键操作游戏
- 连续物理运动游戏
- Game Jam 主题：**Anchor**

### 1.3 核心玩法概述

玩家控制一根由两个端点和中间棍体组成的刚性棍子：

```text
O---O
```

游戏中只有一个主要操作键：**空格键**。

按下空格键时，棍子的当前锚点会切换到另一端。

- 如果新的锚点端点正好落在可锚定墙壁上，则棍子抓住墙壁。
- 如果新的锚点端点没有落在墙壁上，则棍子抓空，进入空中飞行状态。
- 空中飞行时，两个端点都不在墙壁上，棍子绕质心旋转，并受到重力影响。
- 玩家需要不断切换锚点，利用墙壁向上攀登，躲避不断上升的岩浆，最终抓住终点墙壁获得胜利。

### 1.4 游戏目标

玩家需要在岩浆追上之前，通过精准切换锚点，不断向上攀登，最终抓住终点墙壁。

### 1.5 核心特色

- 只有一个按键：空格。
- 墙壁不产生碰撞，只提供锚定判定。
- 抓空不会无效，而是进入物理飞行状态。
- 空中飞行时棍子绕质心旋转。
- 岩浆持续上升，形成时间压力。
- 地图通过符号文本设计，便于快速制作关卡。
- 使用数据驱动设计，核心数值统一配置在 `data_config.py` 中。

---

## 2. 操作设计

### 2.1 按键

| 按键 | 功能 |
|---|---|
| Space | 切换锚点 / 开始游戏 / 死亡后重开 |

### 2.2 输入规则

按下空格时：

1. 当前锚点切换到另一端。
2. 检查新的锚点端点是否位于墙壁区域内。
3. 如果在墙壁区域内，则抓住该墙壁。
4. 如果不在墙壁区域内，则进入空中飞行状态。
5. 旋转方向保持不变。

---

## 3. 核心物理规则

### 3.1 棍子状态

棍子拥有两种主要状态：

```text
Anchored    已锚定状态
Airborne    空中飞行状态
```

---

### 3.2 已锚定状态

当棍子的某一个端点抓住墙壁时，棍子处于已锚定状态。

规则：

- 当前锚点端固定在墙壁上。
- 如果墙壁是移动墙壁，锚点跟随墙壁移动。
- 另一端围绕当前锚点旋转。
- 棍子整体不受重力下坠影响。
- 棍子保持固定转速。
- 墙壁不会阻挡棍子。
- 墙壁不会与棍子产生摩擦或粘性。

---

### 3.3 空中飞行状态

当玩家抓空，或因为危险障碍物导致锚点脱落时，棍子进入空中飞行状态。

规则：

- 两个端点都不在墙壁上。
- 棍子绕自身质心旋转。
- 棍子的质心维持原有速度方向运动。
- 棍子的质心受到重力影响。
- 棍子继续保持原本旋转方向。
- 玩家仍然可以按空格尝试重新抓住墙壁。

---

### 3.4 墙壁判定规则

墙壁不参与物理碰撞。

墙壁只参与以下判定：

```text
当玩家按下空格时，新锚点端点是否位于墙壁区域中
```

如果端点位于墙壁区域中，则抓住。

如果端点不在墙壁区域中，则抓空。

---

### 3.5 危险障碍物判定规则

危险障碍物会与棍子产生触发判定。

规则：

- 只有危险障碍物是“碰到触发”。
- 当棍子任意部分碰到危险障碍物时，如果当前处于已锚定状态，则锚点脱落。
- 锚点脱落后棍子进入空中飞行状态。
- 危险障碍物不一定直接杀死玩家，而是制造失控风险。

---

### 3.6 道具判定规则

除危险障碍物外，其它道具均为“抓住触发”。

也就是说：

- 长度道具需要端点作为新锚点抓住该道具所在区域后触发。
- 速度道具需要端点作为新锚点抓住该道具所在区域后触发。
- 道具触发后改变棍子的长度或转速。

---

## 4. 棍子设计

### 4.1 棍子对象 Stick

棍子由三个部分组成：

1. 左端点
2. 右端点
3. 中间棍体

整体表现为：

```text
O---O
```

---

### 4.2 棍子属性

棍子需要包含以下属性：

| 属性名 | 说明 |
|---|---|
| left_endpoint_mass | 左端点质量 |
| left_endpoint_radius | 左端点半径 |
| right_endpoint_mass | 右端点质量 |
| right_endpoint_radius | 右端点半径 |
| rod_mass | 棍子质量 |
| rod_radius | 棍子半径 |
| angular_speed | 转速 |
| length | 棍子长度 |
| center_position | 质心位置 |
| linear_velocity | 质心线速度 |
| angle | 当前角度 |
| anchor_side | 当前锚点端，left 或 right |
| state | 当前状态，Anchored 或 Airborne |
| attached_wall | 当前抓住的墙壁对象 |

---

### 4.3 质量规则

端点和棍子的质量均匀分布。

棍子的总质量为：

$$
M = m_l + m_r + m_{rod}
$$

其中：

- $$m_l$$ 为左端点质量
- $$m_r$$ 为右端点质量
- $$m_{rod}$$ 为棍体质量

如果左右端点质量不同，则质心不一定处于几何中心。

不过在 Game Jam 版本中，为简化实现，可以默认：

```text
左端点质量 = 右端点质量
```

此时质心可近似位于棍子几何中心。

---

### 4.4 质心计算

如果使用简化版本：

$$
C = \frac{P_l + P_r}{2}
$$

如果需要考虑不同质量，则可以使用加权质心。

设：

- 左端点位置为 $$P_l$$
- 右端点位置为 $$P_r$$
- 棍体质心位于两端点中点 $$P_{rod}$$

则整体质心为：

$$
C =
\frac{
m_l P_l + m_r P_r + m_{rod} P_{rod}
}{
m_l + m_r + m_{rod}
}
$$

---

### 4.5 已锚定时运动

当某一端点抓住墙壁时：

- 锚点端位置固定。
- 自由端绕锚点端旋转。
- 角速度为配置中的 `angular_speed`。
- 如果墙壁移动，锚点位置跟随墙壁移动。

---

### 4.6 空中飞行时运动

空中飞行时：

- 棍子绕质心旋转。
- 质心受到重力影响。
- 质心线速度不断更新。
- 两个端点根据质心、角度和长度计算。

---

### 4.7 长度变化规则

#### 增长道具

当棍子触发增长道具时：

- 当前锚点不动。
- 从另一边开始增长。
- 棍子长度增加。
- 自由端沿当前方向向外延伸。

#### 缩短道具

当棍子触发缩短道具时：

- 当前锚点不动。
- 从另一边开始缩短。
- 棍子长度减少。
- 自由端沿当前方向向锚点靠近。

#### 长度限制

建议设置：

| 参数 | 说明 |
|---|---|
| min_length | 最小棍长 |
| max_length | 最大棍长 |

避免棍子过短或过长导致玩法失控。

---

### 4.8 转速变化规则

#### 加速道具

- 增加棍子的转速。
- 保持原有旋转方向不变。

#### 减速道具

- 减少棍子的转速。
- 保持原有旋转方向不变。
- 转速不能低于最小转速。

---

## 5. 墙壁设计

### 5.1 墙壁对象 Wall

墙壁是可锚定区域。

墙壁不产生碰撞，只用于锚定判定。

---

### 5.2 墙壁属性

| 属性名 | 说明 |
|---|---|
| length | 墙壁长度 |
| appearance | 墙壁外观 |
| is_one_time | 是否一次性 |
| is_goal | 是否终点 |
| move_strategy | 移动策略对象 |
| position | 墙壁当前位置 |
| direction | 墙壁方向 |
| active | 墙壁是否仍然存在 |

---

### 5.3 墙壁类型

墙壁通过属性组合来定义，而不是写死类型。

#### 普通墙壁

```text
is_one_time = False
is_goal = False
move_strategy = None
```

#### 脆弱墙壁

```text
is_one_time = True
is_goal = False
move_strategy = None
```

规则：

- 可以被抓住。
- 当锚点离开墙壁后，墙壁碎掉。
- 碎掉后不能再次抓住。

#### 移动墙壁

```text
move_strategy != None
```

规则：

- 墙壁会根据移动策略移动。
- 棍子抓住移动墙壁后，锚点跟随墙壁移动。

#### 终点墙壁

```text
is_goal = True
```

规则：

- 当玩家抓住终点墙壁时，游戏胜利。

---

### 5.4 自动瓷砖规则

墙壁使用自动瓷砖保证美观。

地图设计师只需要用符号绘制墙壁形状，程序根据相邻格子自动选择合适的墙壁贴图。

自动瓷砖需要支持：

- 单独块
- 水平连接
- 垂直连接
- 内角
- 外角
- 端点
- 十字连接
- T 形连接

---

## 6. 移动策略设计

### 6.1 策略模式

墙壁移动使用策略模式实现。

每个移动墙壁拥有一个 `move_strategy` 对象。

墙壁本身不关心如何移动，只在每帧调用：

```python
move_strategy.update(delta_time, wall)
```

移动逻辑由具体策略类封装。

---

### 6.2 移动策略基类 MoveStrategy

属性：

| 属性名 | 说明 |
|---|---|
| move_speed | 移动速度 |
| move_points | 移动点数组 |
| current_index | 当前目标点索引 |

方法：

| 方法名 | 说明 |
|---|---|
| update(delta_time, wall) | 更新墙壁位置 |
| reset() | 重置移动状态 |

---

### 6.3 循环移动策略 LoopMoveStrategy

墙壁会在移动数组中循环遍历点。

例如：

```text
P0 -> P1 -> P2 -> P0 -> P1 -> P2 ...
```

适合：

- 往复移动平台
- 循环机关
- 节奏型锚点

属性：

| 属性名 | 说明 |
|---|---|
| move_speed | 移动速度 |
| move_points | 移动点数组 |
| current_index | 当前目标点索引 |

规则：

- 墙壁从当前点向下一个点直线移动。
- 到达目标点后切换到数组中的下一个点。
- 到达数组末尾后回到第一个点。
- 无限循环。

---

### 6.4 一次性移动策略 OneShotMoveStrategy

墙壁会按移动数组中的点依次移动，到达最后一个点后停止。

例如：

```text
P0 -> P1 -> P2 -> Stop
```

适合：

- 一次性电梯
- 逃生路线
- 关卡推进机关

属性：

| 属性名 | 说明 |
|---|---|
| move_speed | 移动速度 |
| move_points | 移动点数组 |
| current_index | 当前目标点索引 |
| finished | 是否已经完成移动 |

规则：

- 墙壁从当前点向下一个点直线移动。
- 到达目标点后切换到下一个点。
- 到达最后一个点后停止。
- 停止后仍然可以作为墙壁被抓住，除非额外配置为不可用。

---

## 7. 物体与道具设计

### 7.1 物体对象 GameObject

场景中的道具和危险障碍物都继承或组合自统一的物体类。

---

### 7.2 物体属性

| 属性名 | 说明 |
|---|---|
| item_effect | 道具效果 |
| size | 尺寸 |
| trigger_condition | 触发条件 |
| position | 位置 |
| appearance | 外观 |
| active | 是否仍然有效 |

---

### 7.3 触发条件 TriggerCondition

触发条件包括：

| 条件 | 说明 |
|---|---|
| OnTouchStick | 棍子碰到时触发 |
| OnAnchor | 抓住时触发 |

规则：

- 危险障碍物使用 `OnTouchStick`。
- 长度和速度道具使用 `OnAnchor`。

---

### 7.4 道具效果 ItemEffect

道具效果包括：

| 道具 | 效果 |
|---|---|
| Hazard | 危险障碍物，使当前锚点脱落 |
| LengthUp | 增长棍子 |
| LengthDown | 缩短棍子 |
| SpeedUp | 加快转速 |
| SpeedDown | 减慢转速 |

---

### 7.5 危险障碍物

规则：

- 棍子任意部分碰到危险障碍物即触发。
- 如果棍子处于已锚定状态，则锚点脱落。
- 棍子进入空中飞行状态。
- 如果棍子已经在空中，则可以只播放危险音效，不重复改变状态。

---

### 7.6 长度道具

#### 增长道具

触发方式：

```text
抓住触发
```

效果：

- 棍子长度增加。
- 当前锚点不动。
- 自由端向外延长。

#### 缩短道具

触发方式：

```text
抓住触发
```

效果：

- 棍子长度减少。
- 当前锚点不动。
- 自由端向内缩短。

---

### 7.7 速度道具

#### 加速道具

触发方式：

```text
抓住触发
```

效果：

- 棍子的转速提高。
- 旋转方向不变。

#### 减速道具

触发方式：

```text
抓住触发
```

效果：

- 棍子的转速降低。
- 旋转方向不变。

---

## 8. 岩浆与地图框设计

### 8.1 地图框 LevelFrame

地图框表示当前关卡的有效区域。

地图框有一个持续上升的岩浆判定线。

---

### 8.2 岩浆规则

地图框以固定速度设定一个不断上升的 y 坐标。

```text
低于该 y 坐标的区域视为岩浆
```

规则：

- 岩浆 y 坐标随时间上升。
- 棍子任意部分低于岩浆 y 坐标，则游戏失败。
- 岩浆速度由配置文件设定。
- 不同关卡可以配置不同岩浆速度。

---

### 8.3 岩浆属性

| 属性名 | 说明 |
|---|---|
| lava_y | 当前岩浆高度 |
| lava_rise_speed | 岩浆上升速度 |
| start_y | 初始岩浆高度 |
| kill_margin | 判定容错距离 |
| appearance | 岩浆外观 |

---

## 9. 重力系统

### 9.1 GravitySystem

重力系统负责给空中状态的棍子施加重力。

---

### 9.2 重力属性

| 属性名 | 说明 |
|---|---|
| gravity_vector | 重力向量 |
| gravity_scale | 重力倍率 |

---

### 9.3 规则

- 只有空中飞行状态受到重力影响。
- 已锚定状态不受重力下坠影响。
- 重力参数由 `data_config.py` 配置。

---

## 10. 音效系统

### 10.1 SoundSystem

音效系统负责播放游戏反馈声音。

---

### 10.2 音效类型

需要为以下事件配置音效：

| 事件 | 音效 |
|---|---|
| 抓住普通墙壁 | anchor_success |
| 抓空 | anchor_miss |
| 抓住脆弱墙壁 | anchor_fragile |
| 脆弱墙壁碎裂 | wall_break |
| 抓住终点墙壁 | goal |
| 碰到危险障碍物 | hazard |
| 增长道具触发 | length_up |
| 缩短道具触发 | length_down |
| 加速道具触发 | speed_up |
| 减速道具触发 | speed_down |
| 岩浆死亡 | lava_death |
| 游戏开始 | game_start |
| 游戏重开 | restart |

---

### 10.3 数据驱动音效

音效路径不写死在代码中，而是在 `data_config.py` 中配置。

示例：

```python
SOUND_CONFIG = {
    "anchor_success": "arts/sounds/anchor_success.wav",
    "anchor_miss": "arts/sounds/anchor_miss.wav",
    "wall_break": "arts/sounds/wall_break.wav",
}
```

---

## 11. 数据驱动设计

### 11.1 总体原则

游戏中的所有核心数值、素材路径、道具效果、墙壁参数、音效路径都应尽可能配置在 `data_config.py` 中，而不是写死在逻辑代码中。

目标：

- 方便调参
- 方便地图设计师使用
- 方便扩展关卡
- 减少程序和内容的耦合

---

### 11.2 配置文件

统一配置文件：

```text
data_config.py
```

该文件需要包含：

- 棍子默认参数
- 墙壁默认参数
- 移动策略默认参数
- 道具默认参数
- 岩浆参数
- 重力参数
- 音效路径
- 图片素材路径
- 自动瓷砖配置
- 符号地图解析配置

---

### 11.3 data_config.py 示例结构

```python
# data_config.py

# =========================
# 棍子默认配置
# =========================
STICK_CONFIG = {
    # 左端点质量
    "left_endpoint_mass": 1.0,

    # 左端点半径
    "left_endpoint_radius": 12,

    # 右端点质量
    "right_endpoint_mass": 1.0,

    # 右端点半径
    "right_endpoint_radius": 12,

    # 中间棍体质量
    "rod_mass": 2.0,

    # 中间棍体半径
    "rod_radius": 4,

    # 初始棍长
    "length": 120,

    # 初始角速度，单位可使用 degrees_per_second 或 radians_per_second
    "angular_speed": 150,

    # 最小棍长
    "min_length": 70,

    # 最大棍长
    "max_length": 220,
}


# =========================
# 重力配置
# =========================
GRAVITY_CONFIG = {
    # y 方向重力，具体正负取决于引擎坐标系
    "gravity_vector": (0, -980),

    # 重力倍率
    "gravity_scale": 1.0,
}


# =========================
# 岩浆配置
# =========================
LAVA_CONFIG = {
    # 岩浆初始高度
    "start_y": -300,

    # 岩浆上升速度
    "rise_speed": 30,

    # 死亡判定容错
    "kill_margin": 5,

    # 岩浆素材
    "appearance": "arts/lava/lava_01.png",
}


# =========================
# 墙壁默认配置
# =========================
WALL_CONFIG = {
    # 默认墙壁长度
    "default_length": 64,

    # 普通墙壁外观
    "normal_appearance": "arts/walls/normal_wall.png",

    # 脆弱墙壁外观
    "fragile_appearance": "arts/walls/fragile_wall.png",

    # 终点墙壁外观
    "goal_appearance": "arts/walls/goal_wall.png",
}


# =========================
# 道具配置
# =========================
ITEM_CONFIG = {
    "length_up": {
        "effect": "LengthUp",
        "size": (32, 32),
        "value": 20,
        "trigger_condition": "OnAnchor",
        "appearance": "arts/items/length_up.png",
        "sound": "length_up",
    },
    "length_down": {
        "effect": "LengthDown",
        "size": (32, 32),
        "value": 20,
        "trigger_condition": "OnAnchor",
        "appearance": "arts/items/length_down.png",
        "sound": "length_down",
    },
    "speed_up": {
        "effect": "SpeedUp",
        "size": (32, 32),
        "value": 0.2,
        "trigger_condition": "OnAnchor",
        "appearance": "arts/items/speed_up.png",
        "sound": "speed_up",
    },
    "speed_down": {
        "effect": "SpeedDown",
        "size": (32, 32),
        "value": 0.2,
        "trigger_condition": "OnAnchor",
        "appearance": "arts/items/speed_down.png",
        "sound": "speed_down",
    },
    "hazard": {
        "effect": "Hazard",
        "size": (32, 32),
        "trigger_condition": "OnTouchStick",
        "appearance": "arts/items/hazard.png",
        "sound": "hazard",
    },
}


# =========================
# 音效配置
# =========================
SOUND_CONFIG = {
    "anchor_success": "arts/sounds/anchor_success.wav",
    "anchor_miss": "arts/sounds/anchor_miss.wav",
    "anchor_fragile": "arts/sounds/anchor_fragile.wav",
    "wall_break": "arts/sounds/wall_break.wav",
    "goal": "arts/sounds/goal.wav",
    "hazard": "arts/sounds/hazard.wav",
    "length_up": "arts/sounds/length_up.wav",
    "length_down": "arts/sounds/length_down.wav",
    "speed_up": "arts/sounds/speed_up.wav",
    "speed_down": "arts/sounds/speed_down.wav",
    "lava_death": "arts/sounds/lava_death.wav",
    "game_start": "arts/sounds/game_start.wav",
    "restart": "arts/sounds/restart.wav",
}


# =========================
# 地图符号配置
# =========================
TILE_SYMBOL_CONFIG = {
    "#": "normal_wall",
    "F": "fragile_wall",
    "G": "goal_wall",
    "H": "hazard",
    "+": "length_up",
    "-": "length_down",
    ">": "speed_up",
    "<": "speed_down",
    ".": "empty",
}
```

---

## 12. 素材文件夹设计

### 12.1 arts 文件夹

所有图片、音效、背景等资源统一放在 `arts` 文件夹中。

推荐结构：

```text
arts/
    backgrounds/
        level_01_bg.png
        level_02_bg.png

    walls/
        normal_wall.png
        fragile_wall.png
        goal_wall.png
        wall_tileset.png

    items/
        hazard.png
        length_up.png
        length_down.png
        speed_up.png
        speed_down.png

    stick/
        endpoint_left.png
        endpoint_right.png
        rod.png

    lava/
        lava_01.png

    sounds/
        anchor_success.wav
        anchor_miss.wav
        anchor_fragile.wav
        wall_break.wav
        goal.wav
        hazard.wav
        length_up.wav
        length_down.wav
        speed_up.wav
        speed_down.wav
        lava_death.wav
        game_start.wav
        restart.wav
```

---

## 13. 地图设计系统

### 13.1 地图文件命名

每个关卡使用独立地图文件：

```text
map01.py
map02.py
map03.py
```

---

### 13.2 地图设计原则

地图设计师不需要写逻辑代码，也不需要拖拽编辑。

地图设计师只需要通过符号绘制地图：

```text
# 表示普通墙壁
F 表示脆弱墙壁
G 表示终点墙壁
H 表示危险障碍物
+ 表示增长道具
- 表示缩短道具
> 表示加速道具
< 表示减速道具
. 表示空白
```

---

### 13.3 地图文件结构示例

```python
# map01.py

MAP_CONFIG = {
    "level_id": "map01",

    # 当前关卡背景图
    "background": "arts/backgrounds/level_01_bg.png",

    # 当前关卡岩浆速度
    "lava_rise_speed": 30,

    # 当前关卡起点
    "player_start": (320, 100),

    # 每个字符对应的格子大小
    "tile_size": 32,

    # 文本地图
    "layout": [
        "....................",
        ".........G..........",
        "....................",
        "....###.............",
        "....................",
        "............F.......",
        "....................",
        "...+................",
        "....................",
        "######.........######",
        "....................",
        ".......H............",
        "....................",
        "....###.............",
        "....................",
    ],

    # 移动墙壁额外配置
    "moving_walls": [
        {
            "symbol": "M",
            "positions": [(5, 10), (5, 14)],
            "strategy": "loop",
            "move_speed": 60,
            "move_points": [(160, 320), (160, 448)],
            "appearance": "arts/walls/normal_wall.png",
        }
    ]
}
```

---

### 13.4 地图符号建议

| 符号 | 含义 |
|---|---|
| `.` | 空白 |
| `#` | 普通墙壁 |
| `F` | 脆弱墙壁 |
| `G` | 终点墙壁 |
| `H` | 危险障碍物 |
| `+` | 增长道具 |
| `-` | 缩短道具 |
| `>` | 加速道具 |
| `<` | 减速道具 |
| `M` | 移动墙壁 |
| `S` | 玩家出生点 |

---

### 13.5 移动墙壁地图配置

因为移动墙壁需要移动路径，单纯字符地图无法表达完整信息。

因此移动墙壁可以采用：

1. 符号地图中用 `M` 标记初始位置。
2. 在 `moving_walls` 数组中配置移动策略。

示例：

```python
"moving_walls": [
    {
        "id": "moving_wall_01",
        "start_tile": (5, 10),
        "length": 96,
        "appearance": "arts/walls/normal_wall.png",
        "strategy": "loop",
        "move_speed": 80,
        "move_points": [
            (160, 320),
            (300, 320),
            (300, 500),
            (160, 500),
        ],
    }
]
```

---

## 14. 自动瓷砖系统

### 14.1 目标

地图设计师只写：

```text
#####
#...#
#####
```

程序自动根据周围墙壁关系选择正确图片，使墙壁连接自然美观。

---

### 14.2 自动瓷砖输入

自动瓷砖系统读取地图中的墙壁符号：

```text
#
F
G
M
```

根据上下左右是否存在同类或兼容墙壁，生成对应贴图。

---

### 14.3 自动瓷砖规则

对每一个墙壁格子，计算四个方向是否有相邻墙壁：

| 方向 | 是否有墙 |
|---|---|
| 上 | 0 或 1 |
| 下 | 0 或 1 |
| 左 | 0 或 1 |
| 右 | 0 或 1 |

形成一个 bitmask：

```text
上 = 1
右 = 2
下 = 4
左 = 8
```

根据 bitmask 选择贴图。

示例：

```python
AUTO_TILE_CONFIG = {
    0: "arts/walls/tile_single.png",
    1: "arts/walls/tile_up.png",
    2: "arts/walls/tile_right.png",
    3: "arts/walls/tile_up_right.png",
    4: "arts/walls/tile_down.png",
    5: "arts/walls/tile_vertical.png",
    6: "arts/walls/tile_right_down.png",
    7: "arts/walls/tile_t_no_left.png",
    8: "arts/walls/tile_left.png",
    9: "arts/walls/tile_left_up.png",
    10: "arts/walls/tile_horizontal.png",
    11: "arts/walls/tile_t_no_down.png",
    12: "arts/walls/tile_down_left.png",
    13: "arts/walls/tile_t_no_right.png",
    14: "arts/walls/tile_t_no_up.png",
    15: "arts/walls/tile_cross.png",
}
```

---

## 15. 代码模块建议

### 15.1 推荐项目结构

```text
project/
    main.py

    data_config.py

    core/
        game.py
        input_manager.py
        state_machine.py

    physics/
        stick.py
        gravity.py

    level/
        level_loader.py
        level_frame.py
        lava.py
        autotile.py

    entities/
        wall.py
        move_strategy.py
        game_object.py
        item.py
        hazard.py

    systems/
        sound_system.py
        render_system.py
        collision_system.py

    maps/
        map01.py
        map02.py
        map03.py

    arts/
        backgrounds/
        walls/
        items/
        stick/
        lava/
        sounds/
```

---

### 15.2 核心类概览

| 类名 | 作用 |
|---|---|
| Game | 游戏主循环 |
| Stick | 棍子实体 |
| GravitySystem | 重力系统 |
| Wall | 墙壁实体 |
| MoveStrategy | 移动策略基类 |
| LoopMoveStrategy | 循环移动策略 |
| OneShotMoveStrategy | 一次性移动策略 |
| GameObject | 场景物体基类 |
| Item | 道具 |
| Hazard | 危险障碍物 |
| LevelLoader | 读取地图 |
| LevelFrame | 地图框与岩浆高度 |
| Lava | 岩浆系统 |
| SoundSystem | 音效系统 |
| AutoTileSystem | 自动瓷砖系统 |

---

## 16. 核心流程

### 16.1 游戏初始化流程

```text
读取 data_config.py
↓
读取 map编号.py
↓
加载背景图片
↓
解析符号地图
↓
生成墙壁、道具、危险障碍物
↓
生成移动墙壁和移动策略
↓
生成自动瓷砖
↓
初始化棍子
↓
初始化岩浆高度
↓
开始游戏
```

---

### 16.2 每帧更新流程

```text
读取输入
↓
如果按下 Space，执行切换锚点逻辑
↓
更新墙壁移动策略
↓
更新棍子物理状态
↓
检测危险障碍物碰撞
↓
检测岩浆死亡
↓
检测胜利条件
↓
更新相机和地图框
↓
渲染画面
↓
播放音效
```

---

### 16.3 空格键流程

```text
按下 Space
↓
切换当前锚点端
↓
检查新锚点端是否位于墙壁区域
↓
如果抓住普通墙壁，进入 Anchored
↓
如果抓住脆弱墙壁，进入 Anchored 并记录墙壁
↓
如果抓住移动墙壁，进入 Anchored 并跟随移动墙壁
↓
如果抓住终点墙壁，胜利
↓
如果没有抓住墙壁，进入 Airborne
↓
播放对应音效
```

---

## 17. 胜利与失败

### 17.1 胜利条件

玩家抓住终点墙壁时胜利。

```text
新锚点端点位于终点墙壁区域
并且玩家按下 Space
```

---

### 17.2 失败条件

失败条件包括：

1. 棍子任意部分低于岩浆 y 坐标。
2. 棍子完全掉出地图框。
3. 其它关卡特殊失败条件。

---

## 18. 关卡设计建议

### 18.1 教学关

目标：

- 让玩家理解切换锚点。
- 让玩家理解抓空会下坠。
- 让玩家理解墙壁没有碰撞。

元素：

- 大块普通墙壁
- 慢速岩浆
- 少量危险物

---

### 18.2 进阶关

目标：

- 引入脆弱墙壁。
- 引入长度和速度道具。
- 让玩家学会规划路线。

元素：

- 普通墙壁
- 脆弱墙壁
- 增长 / 缩短道具
- 加速 / 减速道具

---

### 18.3 机关关

目标：

- 引入移动墙壁。
- 考验玩家等待和时机判断。

元素：

- 循环移动墙壁
- 一次性移动墙壁
- 危险障碍物
- 更快岩浆

---

### 18.4 终局关

目标：

- 综合所有机制。
- 高压攀登。
- 抓住终点墙壁完成胜利。

元素：

- 小型墙壁
- 脆弱墙壁
- 移动墙壁
- 危险物
- 快速岩浆
- 终点墙壁

---

## 19. 设计重点

### 19.1 必须优先保证的体验

1. 按空格切换锚点要清晰。
2. 抓住和抓空反馈要强烈。
3. 空中飞行要可预期。
4. 端点经过墙壁时要有明显视觉提示。
5. 岩浆压力不能过早压垮玩家。
6. 地图编辑必须简单。

---

### 19.2 视觉反馈

建议添加：

- 新锚点端接近墙壁时发光。
- 抓住墙壁时产生火花。
- 抓空时产生失重音效和小震动。
- 脆弱墙壁离开后碎裂。
- 终点墙壁发光。
- 岩浆接近时屏幕边缘发红。

---

### 19.3 音效反馈

音效是这个游戏手感的重要组成部分。

必须至少包含：

- 抓住音效
- 抓空音效
- 道具音效
- 危险音效
- 岩浆死亡音效
- 胜利音效

---

## 20. MVP 开发范围

### 20.1 第一版必须完成

- 棍子两状态运动
- 空格切换锚点
- 墙壁锚定判定
- 空中绕质心旋转
- 重力
- 岩浆上升
- 普通墙壁
- 终点墙壁
- 地图符号解析
- 基础音效接口

---

### 20.2 第二版加入

- 脆弱墙壁
- 危险障碍物
- 增长道具
- 缩短道具
- 加速道具
- 减速道具
- 数据配置文件

---

### 20.3 第三版加入

- 移动墙壁
- 策略模式移动系统
- 自动瓷砖
- 多关卡
- 背景图
- 更完整音效

---

## 21. 最终设计总结

**O---O** 是一款围绕 Anchor 主题设计的一键物理攀登游戏。

玩家并不直接控制角色移动，而是通过空格键不断改变棍子的锚点。  
每一次按键都可能成功抓住墙壁，也可能抓空坠落。  
墙壁没有碰撞，只在按键瞬间提供锚定判定，因此玩家必须精准判断端点经过墙壁的时机。

当棍子抓住墙壁时，它绕锚点旋转。  
当棍子抓空时，它绕质心旋转，并在重力作用下飞行下坠。  
不断上升的岩浆迫使玩家不能无限等待，只能在风险和时机之间做出选择。

游戏通过普通墙壁、脆弱墙壁、移动墙壁、终点墙壁、危险障碍物以及长度/速度道具构建关卡变化。  
所有数值和素材路径采用数据驱动设计，统一放入 `data_config.py`。  
地图通过 `map编号.py` 中的字符布局设计，方便快速制作关卡。  
自动瓷砖系统保证墙壁视觉美观。

游戏的核心体验可以概括为：

```text
放开旧锚点，赌上下一个锚点。
```
