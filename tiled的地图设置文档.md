# tiled地图设计和接口设计.md

本文档定义 `O---O` 项目的 **Tiled 地图设计接口**。

目标：

```text
1. 地图设计师从第一天起就可以使用全部功能设计正式关卡。
2. 设计师通过拖拽插入物体，通过下拉菜单和复选框选择属性，而不是手写字符串。
3. 每个墙壁、道具、障碍物都是独立实例，拥有独立属性和外观。
4. 设计师不需要写任何 Python 代码。
5. 保存后一键导入游戏。
```

---

# 第一部分：交互式编辑机制

要实现“设计师插入物体并选择属性”，需要利用 Tiled 的三个官方机制。

---

# 1. Tiled 项目文件（.tiled-project）

Tiled 1.8+ 支持项目文件。项目文件让整个团队共享：

```text
1. 自定义属性类型（枚举、类）
2. 对象模板目录
3. 素材目录
```

## 1.1 创建项目

在 Tiled 中：

```text
File -> New -> New Project
```

保存为：

```text
project/oopz.tiled-project
```

## 1.2 项目文件内容

```json
{
    "automappingRulesFile": "",
    "commands": [],
    "extensionsPath": "tiled/extensions",
    "folders": [
        "maps",
        "arts",
        "tiled/templates"
    ],
    "propertyTypes": []
}
```

设计师以后只需要：

```text
双击打开 oopz.tiled-project
```

就能得到全部模板、类型和素材目录。

---

# 2. 自定义属性类型（Custom Types）

这是实现“下拉选择而不是手打字符串”的核心。

在 Tiled 中：

```text
View -> Custom Types Editor
```

可以定义两种类型：

```text
枚举（Enum）  → 属性面板中显示为下拉菜单
类（Class）   → 属性面板中显示为一组结构化属性
```

定义会保存在项目文件的 `propertyTypes` 中，全团队共享。

---

## 2.1 必须定义的枚举

### MoveStrategy 移动策略

```json
{
    "name": "MoveStrategy",
    "type": "enum",
    "storageType": "string",
    "values": ["loop", "pingpong", "once"],
    "valuesAsFlags": false
}
```

设计师看到的效果：

```text
move_strategy: [下拉菜单] loop / pingpong / once
```

---

### TriggerCondition 触发方式

```json
{
    "name": "TriggerCondition",
    "type": "enum",
    "storageType": "string",
    "values": ["OnAnchor", "OnTouch"],
    "valuesAsFlags": false
}
```

---

### TiltDirection 倾斜方向

```json
{
    "name": "TiltDirection",
    "type": "enum",
    "storageType": "string",
    "values": ["both", "clockwise", "counter_clockwise"],
    "valuesAsFlags": false
}
```

---

### KeyPairResult 钥匙结果

```json
{
    "name": "KeyPairResult",
    "type": "enum",
    "storageType": "string",
    "values": ["solid", "ghost", "toggle"],
    "valuesAsFlags": false
}
```

---

### ItemEffect 道具效果

```json
{
    "name": "ItemEffect",
    "type": "enum",
    "storageType": "string",
    "values": [
        "LengthUp",
        "LengthDown",
        "SpeedUp",
        "SpeedDown",
        "KeyPair",
        "Checkpoint"
    ],
    "valuesAsFlags": false
}
```

---

### WallType 墙壁逻辑类型

```json
{
    "name": "WallType",
    "type": "enum",
    "storageType": "string",
    "values": ["normal", "fragile", "goal"],
    "valuesAsFlags": false
}
```

---

## 2.2 必须定义的类（Class）

Tiled 的 Class 会成为对象的 `class` 字段（旧版叫 `type`），并自动带出一整套属性面板。

设计师选中对象后，只需要在 Class 下拉框选择：

```text
Wall / Item / Hazard / PlayerStart / Path
```

属性面板就会自动出现全部可配置属性，带默认值。

---

### Wall 类定义

```json
{
    "name": "Wall",
    "type": "class",
    "useAs": ["object"],
    "members": [
        { "name": "wall_type",        "type": "string", "propertyType": "WallType", "value": "normal" },
        { "name": "image",            "type": "file",   "value": "arts/wall/normal_wall.png" },
        { "name": "isSolid",          "type": "bool",   "value": true },

        { "name": "fragile",          "type": "bool",   "value": false },
        { "name": "break_on_detach",  "type": "bool",   "value": true },

        { "name": "goal",             "type": "bool",   "value": false },

        { "name": "moving",           "type": "bool",   "value": false },
        { "name": "move_strategy",    "type": "string", "propertyType": "MoveStrategy", "value": "pingpong" },
        { "name": "move_speed",       "type": "float",  "value": 80 },
        { "name": "path_id",          "type": "string", "value": "" },

        { "name": "unstable",         "type": "bool",   "value": false },
        { "name": "max_tilt_angle",   "type": "float",  "value": 35 },
        { "name": "tilt_direction",   "type": "string", "propertyType": "TiltDirection", "value": "both" },
        { "name": "inertia",          "type": "float",  "value": 120 },
        { "name": "torque_scale",     "type": "float",  "value": 1.0 },
        { "name": "damping",          "type": "float",  "value": 1.5 },
        { "name": "return_speed",     "type": "float",  "value": 20 },
        { "name": "break_at_max_tilt","type": "bool",   "value": false },

        { "name": "beat_solid_switch","type": "bool",   "value": false },
        { "name": "switchSecond",     "type": "float",  "value": 2.0 },
        { "name": "initial_delay",    "type": "float",  "value": 0.0 },
        { "name": "start_solid",      "type": "bool",   "value": true },

        { "name": "key_pair_solid",   "type": "bool",   "value": false },
        { "name": "key_pair_id",      "type": "string", "value": "" },
        { "name": "key_pair_result",  "type": "string", "propertyType": "KeyPairResult", "value": "solid" }
    ]
}
```

重点说明：

```text
1. image 使用 type="file"。
   Tiled 会显示一个文件选择器，设计师直接从 arts/wall/ 中选图。

2. 布尔属性显示为复选框。
   设计师勾选 fragile / moving / unstable 即可开关能力。

3. 枚举属性显示为下拉菜单。
   move_strategy / tilt_direction / key_pair_result 均不需要手打。
```

---

### Item 类定义

```json
{
    "name": "Item",
    "type": "class",
    "useAs": ["object"],
    "members": [
        { "name": "effect",             "type": "string", "propertyType": "ItemEffect", "value": "LengthUp" },
        { "name": "image",              "type": "file",   "value": "arts/item/length_up.png" },
        { "name": "value",              "type": "float",  "value": 20 },
        { "name": "trigger_condition",  "type": "string", "propertyType": "TriggerCondition", "value": "OnAnchor" },
        { "name": "consume_on_trigger", "type": "bool",   "value": true },
        { "name": "key_pair_id",        "type": "string", "value": "" },
        { "name": "checkpoint_id",      "type": "string", "value": "" }
    ]
}
```

重点：

```text
trigger_condition 是下拉菜单：OnAnchor / OnTouch
设计师可以自由决定每个道具是碰到触发还是抓住触发。
```

---

### Hazard 类定义

```json
{
    "name": "Hazard",
    "type": "class",
    "useAs": ["object"],
    "members": [
        { "name": "image",             "type": "file",   "value": "arts/hazard/spike.png" },
        { "name": "trigger_condition", "type": "string", "propertyType": "TriggerCondition", "value": "OnTouch" }
    ]
}
```

---

### PlayerStart 类定义

```json
{
    "name": "PlayerStart",
    "type": "class",
    "useAs": ["object"],
    "members": [
        { "name": "angle",            "type": "float", "value": 270 },
        { "name": "anchor_side",      "type": "string", "value": "left" },
        { "name": "stick_image",      "type": "file",  "value": "arts/stick/rod_default.png" },
        { "name": "left_ball_image",  "type": "file",  "value": "arts/left_ball/left_default.png" },
        { "name": "right_ball_image", "type": "file",  "value": "arts/right_ball/right_default.png" },
        { "name": "ball_image",       "type": "file",  "value": "" }
    ]
}
```

---

### Path 类定义

```json
{
    "name": "Path",
    "type": "class",
    "useAs": ["object"],
    "members": [
        { "name": "path_id", "type": "string", "value": "" }
    ]
}
```

---

# 3. 对象模板（Object Templates）

模板让设计师“拖拽即插入完整配置的物体”。

模板目录：

```text
tiled/templates/
```

## 3.1 全量模板清单

墙壁类：

```text
normal_wall.tx
ghost_wall.tx
fragile_wall.tx
goal_wall.tx
moving_wall.tx
unstable_wall.tx
beat_solid_wall.tx
key_pair_wall_to_solid.tx
key_pair_wall_to_ghost.tx
fragile_moving_wall.tx
fragile_unstable_moving_wall.tx
```

道具类：

```text
length_up.tx
length_down.tx
speed_up.tx
speed_down.tx
key.tx
checkpoint.tx
```

障碍物类：

```text
spike.tx
laser.tx
```

其他：

```text
player_start.tx
path.tx
```

## 3.2 制作模板的方法

```text
1. 在任意地图中创建一个 Rectangle Object
2. 设置 Class = Wall
3. 调整属性（例如勾选 fragile）
4. 设置默认尺寸和默认贴图
5. 右键 -> Save As Template
6. 保存到 tiled/templates/
```

## 3.3 模板的关键特性

```text
1. 拖出的对象自动带全部属性和默认值。
2. 设计师只需要修改差异属性。
3. 修改模板文件后，所有引用该模板的对象可以同步更新。
```

---

# 4. 设计师的交互体验总结

配置好上面三样东西后，设计师的实际操作是：

```text
1. 双击打开 oopz.tiled-project
2. 打开或新建关卡
3. 从模板面板拖出 fragile_wall 到 Walls 层
4. 拉伸墙壁到想要的长度
5. 在属性面板：
   - image：点击文件选择器，从 arts/wall/ 选一张图
   - 勾选 moving 复选框
   - move_strategy：下拉选择 pingpong
   - path_id：填 path_wall_01
6. 在 Paths 层画折线，Class 选 Path，path_id 填 path_wall_01
7. Ctrl+S 保存
8. 运行游戏查看
```

全程没有手写代码，没有手打枚举字符串。

---

# 第二部分：地图文件与图层规范

---

# 5. 目录结构

```text
project/
    oopz.tiled-project

    maps/
        _template/
            level.tiled.json
        level1/
            level.tiled.json
            level.json

    tiled/
        templates/
        extensions/

    arts/
        stick/
        left_ball/
        right_ball/
        ball/
        wall/
        item/
        hazard/
        lava/
            lava.gif
        backgrounds/

    tools/
        tiled_converter.py
        convert_all_maps.py
```

---

# 6. 地图设置

```text
Orientation = Orthogonal
Tile size = 32 x 32（仅作网格参考）
Format = JSON
```

注意：

```text
本项目的对象尺寸不固定。
32x32 只是吸附网格，墙壁 / 道具 / 障碍物可以是任意尺寸。
设计师可以自由拉伸对象，游戏必须尊重 Tiled 中的实际 width/height。
```

---

# 7. 图层规范

```text
Player        玩家出生点（Point Object，Class=PlayerStart）
Walls         墙壁（Rectangle Object，Class=Wall）
Items         道具（Rectangle Object，Class=Item）
Hazards       障碍物（Rectangle Object，Class=Hazard）
Paths         移动路径（Polyline Object，Class=Path）
Triggers      触发区（可选）
Decorations   装饰（不参与逻辑）
```

---

# 8. 关卡整体属性（Map Properties）

```text
level_id          string   level1
level_name        string   First Climb
background        file     arts/backgrounds/level_01.png
music             file     arts/sounds/bgm_level1.ogg

lava_enabled      bool     true
lava_gif          file     arts/lava/lava.gif
lava_start_y      float    1200
lava_rise_speed   float    30
lava_alpha        int      160
```

## 8.1 岩浆说明

岩浆是一个半透明 gif：

```text
1. 程序加载 lava_gif 并逐帧播放。
2. 以 lava_alpha 半透明渲染。
3. 高度由 lava_start_y 和 lava_rise_speed 决定。
4. 不需要晃动、波浪等额外属性。
```

---

# 第三部分：对象接口完整定义

---

# 9. Wall 墙壁接口

## 9.1 基本规则

```text
1. Class = Wall
2. 放在 Walls 层
3. Rectangle Object，尺寸任意
4. 每面墙都是独立实例，属性互不共享
5. 能力通过布尔属性组合，可任意叠加
```

## 9.2 完整属性表

| 属性 | 类型 | 交互形式 | 默认值 | 说明 |
|---|---|---|---|---|
| `wall_type` | enum | 下拉 | `normal` | normal / fragile / goal |
| `image` | file | 文件选择器 | 按 prefab | 从 arts/wall/ 选图，自动平铺 |
| `isSolid` | bool | 复选框 | `true` | 初始实体 / 虚体 |
| `fragile` | bool | 复选框 | `false` | 脱锚后碎裂 |
| `break_on_detach` | bool | 复选框 | `true` | 配合 fragile |
| `goal` | bool | 复选框 | `false` | 抓住通关 |
| `moving` | bool | 复选框 | `false` | 沿路径移动 |
| `move_strategy` | enum | 下拉 | `pingpong` | loop / pingpong / once |
| `move_speed` | float | 数字框 | `80` | 像素/秒 |
| `path_id` | string | 文本框 | 空 | 绑定 Paths 层路径 |
| `unstable` | bool | 复选框 | `false` | 抓住后倾斜 |
| `max_tilt_angle` | float | 数字框 | `35` | 最大倾角（度） |
| `tilt_direction` | enum | 下拉 | `both` | 倾斜方向限制 |
| `inertia` | float | 数字框 | `120` | 转动惯量 |
| `torque_scale` | float | 数字框 | `1.0` | 力矩倍率 |
| `damping` | float | 数字框 | `1.5` | 阻尼 |
| `return_speed` | float | 数字框 | `20` | 回正速度（度/秒） |
| `break_at_max_tilt` | bool | 复选框 | `false` | 达到极限碎裂 |
| `beat_solid_switch` | bool | 复选框 | `false` | 节拍虚实切换 |
| `switchSecond` | float | 数字框 | `2.0` | 切换周期（秒） |
| `initial_delay` | float | 数字框 | `0.0` | 初始延迟 |
| `start_solid` | bool | 复选框 | `true` | 节拍初始状态 |
| `key_pair_solid` | bool | 复选框 | `false` | 钥匙控制虚实 |
| `key_pair_id` | string | 文本框 | 空 | 匹配钥匙 ID |
| `key_pair_result` | enum | 下拉 | `solid` | solid / ghost / toggle |

## 9.3 能力组合规则

所有布尔能力可以任意组合，例如：

```text
fragile + moving                      移动的脆弱墙
moving + unstable                     移动且会倾斜的墙
beat_solid_switch + moving            移动的节拍墙
key_pair_solid + goal                 钥匙解锁的终点墙
fragile + moving + unstable           三合一机关墙
isSolid=false + key_pair_solid        初始虚体、钥匙变实体
```

冲突规则：

```text
1. key_pair_solid 触发后会锁定墙壁，beat_solid_switch 自动失效。
2. goal=true 时建议 wall_type=goal，以获得终点视觉效果。
3. fragile=true 时建议 wall_type=fragile，以获得脆弱视觉效果。
```

---

# 10. Item 道具接口

## 10.1 基本规则

```text
1. Class = Item
2. 放在 Items 层
3. Rectangle Object，尺寸任意
4. 道具可以且经常应该与墙壁重叠
```

## 10.2 为什么道具必须允许与墙壁重叠

```text
本游戏中棍子抓住道具的瞬间同时需要墙壁作为锚点。
如果道具区域内没有墙壁，抓取动作会落空，玩家直接掉落。
因此程序按空格时会同时检测：
    - 端点是否命中墙壁（锚定）
    - 端点是否命中道具（触发）
二者互不排斥。
```

## 10.3 完整属性表

| 属性 | 类型 | 交互形式 | 默认值 | 说明 |
|---|---|---|---|---|
| `effect` | enum | 下拉 | `LengthUp` | 道具效果 |
| `image` | file | 文件选择器 | 按 effect | 从 arts/item/ 选图 |
| `value` | float | 数字框 | `20` | 效果数值 |
| `trigger_condition` | enum | 下拉 | `OnAnchor` | OnAnchor / OnTouch |
| `consume_on_trigger` | bool | 复选框 | 按类型 | 触发后是否消失 |
| `key_pair_id` | string | 文本框 | 空 | effect=KeyPair 时必填 |
| `checkpoint_id` | string | 文本框 | 空 | effect=Checkpoint 时使用 |

## 10.4 各效果推荐配置

| effect | trigger_condition | consume_on_trigger | value |
|---|---|---|---|
| `LengthUp` | OnAnchor | true | 20 |
| `LengthDown` | OnAnchor | true | 20 |
| `SpeedUp` | OnAnchor | true | 0.2 |
| `SpeedDown` | OnAnchor | true | 0.2 |
| `KeyPair` | OnAnchor | true | - |
| `Checkpoint` | OnTouch | false | - |

注意：

```text
trigger_condition 是每个道具实例独立可选的。
同一种道具在不同位置可以有不同触发方式。
例如某个 SpeedUp 可以改成 OnTouch，做成飞过即加速的效果。
```

---

# 11. Hazard 障碍物接口

## 11.1 基本规则

```text
1. Class = Hazard
2. 放在 Hazards 层
3. Rectangle Object，尺寸任意
4. 可以与墙壁重叠，制造"半危险平台"
```

## 11.2 属性表

| 属性 | 类型 | 交互形式 | 默认值 | 说明 |
|---|---|---|---|---|
| `image` | file | 文件选择器 | `arts/hazard/spike.png` | 外观 |
| `trigger_condition` | enum | 下拉 | `OnTouch` | 通常保持 OnTouch |

效果固定为：

```text
棍子任意部分触碰 → 强制脱锚，进入失控飞行
```

---

# 12. PlayerStart 玩家接口

## 12.1 基本规则

```text
1. Class = PlayerStart
2. 放在 Player 层
3. Point Object
4. 每张地图必须有且只有一个
```

## 12.2 属性表

| 属性 | 类型 | 交互形式 | 默认值 | 说明 |
|---|---|---|---|---|
| `angle` | float | 数字框 | `270` | 棍子初始角度（度） |
| `anchor_side` | string | 文本框 | `left` | 初始锚点端 |
| `stick_image` | file | 文件选择器 | rod_default | 棍体贴图，选自 arts/stick/ |
| `left_ball_image` | file | 文件选择器 | left_default | 左端点贴图，选自 arts/left_ball/ |
| `right_ball_image` | file | 文件选择器 | right_default | 右端点贴图，选自 arts/right_ball/ |
| `ball_image` | file | 文件选择器 | 空 | 通用端点贴图，选自 arts/ball/ |

## 12.3 端点贴图优先级

```text
1. 如果设置了 left_ball_image / right_ball_image，分别使用。
2. 否则如果设置了 ball_image，两端都用它。
3. 否则使用游戏默认贴图。
```

---

# 13. Path 路径接口

## 13.1 基本规则

```text
1. Class = Path
2. 放在 Paths 层
3. Polyline Object
4. path_id 必须与某面 moving 墙的 path_id 一致
5. 路径第一个点应尽量与墙壁初始位置重合
```

## 13.2 属性表

| 属性 | 类型 | 说明 |
|---|---|---|
| `path_id` | string | 唯一路径 ID，如 `path_wall_001` |

---

# 第四部分：转换与导入接口

---

# 14. 转换管线

```text
maps/levelX/level.tiled.json
        ↓
tools/tiled_converter.py
        ↓
maps/levelX/level.json
        ↓
LevelLoader → ObjectFactory → 游戏对象
```

## 14.1 转换器职责

```text
1. 展平 Tiled properties 数组为字典。
2. 读取对象 Class 字段决定对象大类。
3. 读取 x / y / width / height，保持任意尺寸。
4. 保留 image 等文件路径（转为项目相对路径）。
5. Polyline 相对坐标转换为世界坐标。
6. path_id 匹配 moving 墙并注入 path 点列表。
7. 根据布尔能力属性生成 components 字典。
8. 读取 Map Properties 生成 lava / background / music。
9. 执行校验并输出报错。
10. 输出 level.json。
```

## 14.2 组件生成规则

| Tiled 属性 | 生成组件 |
|---|---|
| `fragile=true` | `"fragile": {"break_on_detach": ...}` |
| `goal=true` | `"goal": {}` |
| `moving=true` | `"moving": {"strategy", "speed", "path"}` |
| `unstable=true` | `"unstable": {全部倾斜参数}` |
| `beat_solid_switch=true` | `"beat_solid_switch": {"switchSecond", "initial_delay", "start_solid"}` |
| `key_pair_solid=true` | `"key_pair_solid": {"key_pair_id", "key_pair_result"}` |

## 14.3 输出示例

```json
{
    "id": "wall_017",
    "type": "wall",
    "wall_type": "fragile",
    "position": [320, 560],
    "width": 160,
    "height": 32,
    "image": "arts/wall/fragile_wall.png",
    "isSolid": true,
    "components": {
        "fragile": { "break_on_detach": true },
        "moving": {
            "strategy": "pingpong",
            "speed": 80,
            "path": [[320, 560], [480, 560], [480, 420]]
        }
    }
}
```

---

# 15. ObjectFactory 接口

每个对象都创建为独立实例：

```python
def create_wall(obj):
    wall = Wall(
        x=obj["position"][0],
        y=obj["position"][1],
        width=obj["width"],
        height=obj["height"],
        wall_type=obj.get("wall_type", "normal"),
        wall_id=obj["id"],
        isSolid=obj.get("isSolid", True),
    )
    wall.appearance = obj.get("image")

    for name, cfg in obj.get("components", {}).items():
        wall.add_component(name, create_component(name, cfg))

    return wall
```

保证：

```text
每面墙是独立 Wall 实例
每个组件是独立组件实例
每个移动策略是独立策略实例
不同墙之间不共享任何运行时状态
```

---

# 16. 校验规则（转换器强制执行）

转换器在导出时必须检查并报错：

```text
E01  缺少 Player 层或 player_start 数量不为 1
E02  moving=true 但 path_id 为空
E03  path_id 找不到对应 Path 对象
E04  两条 Path 使用了相同 path_id
E05  key_pair_solid=true 但 key_pair_id 为空
E06  存在 key_pair_id 的墙，但地图中没有对应钥匙
E07  effect=KeyPair 的道具没有 key_pair_id
E08  image 指向的文件不存在
E09  goal 墙数量为 0（警告）
E10  Checkpoint 的 consume_on_trigger=true（警告，通常应为 false）
E11  对象 Class 缺失或非法
E12  对象放错图层（如 Item 放在 Walls 层）
```

报错格式：

```text
[E02] Walls 层 对象 id=23 (x=320, y=560): moving=true 但未填写 path_id
```

---

# 17. 一键测试（提升设计师迭代速度）

## 17.1 转换脚本

提供双击脚本：

```text
tools/convert_all_maps.bat
```

内容：

```bat
@echo off
python tools/convert_all_maps.py
pause
```

## 17.2 游戏启动自动转换

游戏加载关卡前检查：

```python
if mtime("level.tiled.json") > mtime("level.json"):
    run_converter()
```

效果：

```text
设计师在 Tiled 里 Ctrl+S
直接运行游戏
自动使用最新地图
```

## 17.3 Tiled 自定义命令（可选）

在 Tiled 中配置 Command：

```text
名称：Run Game
命令：python main.py --level %mapfile
快捷键：F5
```

设计师在 Tiled 里按 F5 即可直接启动游戏测试当前关卡。

---

# 第五部分：设计师完整工作流

---

# 18. 首次配置（程序员做一次）

```text
1. 创建 oopz.tiled-project
2. 在 Custom Types Editor 中导入全部枚举和类定义
3. 制作全部对象模板到 tiled/templates/
4. 建立 maps/_template/level.tiled.json（含全部图层和 Map Properties）
5. 配置 F5 运行命令
6. 把整个项目目录交给设计师
```

---

# 19. 设计师制作正式关卡流程

```text
1. 双击 oopz.tiled-project 打开项目
2. 复制 maps/_template/ 为 maps/level5/
3. 打开 level.tiled.json
4. 修改 Map Properties：
   - level_id / level_name
   - background（文件选择器）
   - lava_gif / lava_start_y / lava_rise_speed
5. 拖入 player_start，选择棍子和端点贴图
6. 拖入各种墙壁模板，拉伸尺寸，勾选能力，选择贴图
7. 需要移动墙时：填 path_id，在 Paths 层画折线并填相同 path_id
8. 拖入道具，选择 effect、触发方式、贴图；可直接叠放在墙上
9. 拖入障碍物，可与墙壁重叠制造危险平台
10. 拖入 checkpoint（OnTouch，不消耗）
11. 拖入 key 与 key_pair 墙配对
12. Ctrl+S 保存
13. 按 F5 直接测试
14. 根据体验反复调整属性数值
```

---

# 20. 设计准则（推荐值）

```text
墙壁厚度            ≥ 24px，推荐 32px
普通墙宽度          ≥ 64px
终点墙尺寸          ≥ 64 x 32
节拍周期            switchSecond ≥ 1.0，推荐 1.5 ~ 3.0
移动速度            40 ~ 120 px/s
Checkpoint 尺寸     ≥ 64 x 64
道具与墙叠放        道具中心应落在墙壁矩形内
危险物密度          同屏不超过 3 个为宜
```

---

# 21. 接口稳定性约定

程序员与设计师之间的契约：

```text
1. 本文档中的属性名一经发布不得更名，只能新增。
2. 新增能力时：
   - 程序员新增组件 + Custom Type 成员 + 模板
   - 更新本文档
   - 旧地图无需修改，缺省属性使用默认值
3. 转换器对未知属性只警告不报错，保证向前兼容。
4. 所有默认值以 Custom Types 定义为准，代码中的默认值必须与之一致。
```

---

# 22. 总结

本接口通过三层机制实现"设计师全功能、零代码、交互式"设计：

```text
交互层    Tiled Custom Types + Templates + 文件选择器
          → 插入物体靠拖拽，选择属性靠下拉菜单和复选框

数据层    level.tiled.json → tiled_converter.py → level.json
          → 强制校验，错误在导出时暴露而不是运行时

运行层    LevelLoader + ObjectFactory + ComponentFactory
          → 每个对象都是独立实例，属性组合自由，逻辑互不共享
```

设计师从第一张正式关卡开始，就可以使用：

```text
任意尺寸和贴图的墙壁 / 道具 / 障碍物
脆弱、移动、不稳定、终点、虚实、节拍、钥匙的任意组合
每个道具独立可选的触发方式（OnAnchor / OnTouch）
道具、障碍物与墙壁的自由叠加
自定义棍子、左右端点外观
半透明 gif 岩浆
存档点与钥匙机关
```

而这一切都不需要写一行 Python 代码。
