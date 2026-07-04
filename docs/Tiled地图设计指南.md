# O---O 地图设计指南 — 使用 Tiled Map Editor

本指南面向**地图设计师**，教你如何用 Tiled Map Editor 可视化地创建关卡。
你**不需要写任何代码**。

---

## 1. 安装 Tiled Map Editor

1. 官网下载: https://www.mapeditor.org/
2. 安装后打开 Tiled

---

## 2. 创建新地图

### 2.1 新建地图

`文件 → 新建 → 新地图`

| 设置项 | 值 | 说明 |
|--------|-----|------|
| 方向 | 正交 | 标准 2D 俯视图 |
| 地图尺寸 | 宽度 20, 高度 35 | 格子数 |
| 图块大小 | 宽度 32px, 高度 32px | 每个格子 32×32 |

> **最终世界尺寸**: 20×35 格 × 32px = **640 × 1120 像素**
>
> 如果关卡更大，可以调整地图尺寸。运行游戏后查看 `arts/needs/` 文件夹确认实际需要的背景图尺寸。

### 2.2 保存

`文件 → 保存` → 选择 `maps/level1/level.tiled.json`

> **格式必须选 JSON (.json)**，不要选 TMX。

---

## 3. 创建图层

在右侧图层面板，新建以下 **对象图层 (Object Layer)**：

| 图层名 | 类型 | 用途 |
|--------|------|------|
| `Player` | 对象层 | 玩家出生点 |
| `Walls` | 对象层 | 所有墙壁 |
| `Items` | 对象层 | 道具 |
| `Hazards` | 对象层 | 危险障碍物 |
| `Paths` | 对象层 | 移动墙壁的路径 |

最终图层结构：

```
Paths          ← 移动路径（Polyline）
Hazards        ← 危险物（矩形）
Items          ← 道具（矩形/点）
Walls          ← 墙壁（矩形）
Player         ← 出生点（点）
```

---

## 4. 放置玩家出生点

1. 选中 `Player` 图层
2. 工具栏选择 **插入点对象** (Insert Point)
3. 在地图上点击放置
4. 在左侧属性面板中设置：

| 属性名 | 类型 | 示例值 | 说明 |
|--------|------|--------|------|
| `object_type` | string | `player_start` | 必须为此值 |
| `angle` | float | `270` | 棍子初始角度（度），270=指向上方 |
| `anchor_side` | string | `left` | 锚点端，"left" 或 "right" |

### 自定义属性操作方法：
1. 选中对象
2. 左侧面板找到 `自定义属性 (Custom Properties)`
3. 点击 `+` 添加属性
4. 填入名称、类型、值

---

## 5. 放置墙壁

### 5.1 普通墙壁

1. 选中 `Walls` 图层
2. 工具栏选择 **插入矩形对象** (Insert Rectangle)
3. 在画布上拖拽出墙壁矩形

墙壁的大小和位置就是游戏中的实际墙面。例如：

```
x = 160, y = 288
width = 192, height = 32
```

表示一面长 192px、厚 32px 的水平墙壁，位于 y=288 处。

### 5.2 墙壁自定义属性

| 属性名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `object_type` | string | `wall` | 必须为 `wall` |
| `prefab` | string | `normal_wall` | 墙壁预制类型 |
| `fragile` | bool | `false` | 锚点离开后墙壁碎裂 |
| `goal` | bool | `false` | 终点墙壁（抓住即通关） |
| `moving` | bool | `false` | 移动墙壁 |
| `unstable` | bool | `false` | 不稳定墙壁（会倾斜） |

### 5.3 墙壁 prefab 类型

| prefab | 效果 |
|--------|------|
| `normal_wall` | 普通墙壁 |
| `fragile_wall` | 脆弱墙壁（锚点离开后碎裂） |
| `goal_wall` | 终点墙壁（抓住通关） |

> **组合使用**: 一个墙壁可以同时勾选多个 bool 属性
> 
> 例如：`fragile=true` + `unstable=true` + `moving=true` = 一个会倾斜的脆弱移动墙

---

## 6. 放置道具

1. 选中 `Items` 图层
2. 工具栏选择 **插入矩形对象** (Insert Rectangle)
3. 在画布上拖拽出道具矩形

道具使用**自由尺寸的矩形碰撞检测**，不绑定网格。道具矩形可以和墙壁矩形**完全重叠**——玩家抓住重叠位置的墙壁时，会同时获得道具。

### 道具属性

| 属性名 | 类型 | 示例值 | 说明 |
|--------|------|--------|------|
| `object_type` | string | `item` | 必须为 `item` |
| `prefab` | string | `length_up` | 道具类型 |

### 道具 prefab 列表

| prefab | 效果 | 推荐尺寸 |
|--------|------|---------|
| `length_up` | 棍子变长 | 32×32 |
| `length_down` | 棍子变短 | 32×32 |
| `speed_up` | 转速变快 | 32×32 |
| `speed_down` | 转速变慢 | 32×32 |

---

## 7. 放置危险物

1. 选中 `Hazards` 图层
2. 工具栏选择 **插入矩形对象**
3. 在画布上拖拽

### 危险物属性

| 属性名 | 类型 | 示例值 | 说明 |
|--------|------|--------|------|
| `object_type` | string | `hazard` | 必须为 `hazard` |
| `prefab` | string | `spike` | 危险物类型 |

---

## 8. 移动墙壁 + 路径（高级）

### 8.1 创建移动墙壁

1. 在 `Walls` 图层画一面墙
2. 设置属性:

| 属性 | 值 |
|------|-----|
| `object_type` | `wall` |
| `moving` | `true` |
| `move_strategy` | `pingpong`（或 `loop`、`once`） |
| `move_speed` | `80`（像素/秒） |
| `path_id` | `path_wall_01` |

### 8.2 绘制移动路径

1. 选中 `Paths` 图层
2. 工具栏选择 **插入折线对象** (Insert Polyline)
3. 在画布上点击画出路径点
4. 按 `Enter` 完成绘制
5. 设置路径属性:

| 属性 | 值 |
|------|-----|
| `object_type` | `path` |
| `path_id` | `path_wall_01`（与墙壁的 path_id 一致） |

> **重要**: 路径的 `path_id` 必须与墙壁的 `path_id` 相同，才能绑定。
>
> 路径的第一个点应靠近墙壁当前位置。

### 8.3 移动策略

| strategy | 行为 |
|----------|------|
| `loop` | 循环移动（到终点后回到起点） |
| `once` | 单次移动（到终点后停止） |
| `pingpong` | 来回移动（到终点后反向） |

---

## 9. 不稳定墙壁（高级）

勾选 `unstable = true` 后，可以配置以下属性：

| 属性名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `max_tilt_angle` | float | `35` | 最大倾斜角度（度） |
| `tilt_direction` | string | `both` | `both` / `clockwise` / `counter_clockwise` |
| `inertia` | float | `120` | 转动惯量（越大越难倾斜） |
| `torque_scale` | float | `1.0` | 力矩缩放（越大倾斜越快） |
| `damping` | float | `1.5` | 阻尼（越大回正越快） |
| `return_speed` | float | `20` | 无锚点时回正速度（度/秒） |
| `break_at_max_tilt` | bool | `false` | 达到最大倾斜后是否碎裂 |

---

## 10. 关卡整体属性

点击菜单 `地图 → 地图属性`，在自定义属性中设置：

| 属性名 | 类型 | 示例值 | 说明 |
|--------|------|--------|------|
| `level_id` | string | `level1` | 关卡 ID |
| `level_name` | string | `First Oopz` | 关卡名称 |
| `background` | string | `arts/backgrounds/level_01_bg.png` | 背景图路径 |
| `lava_enabled` | bool | `true` | 是否启用岩浆 |
| `lava_start_y_below_player` | float | `200` | 岩浆初始位置（玩家下方多少像素） |
| `lava_rise_speed` | float | `25` | 岩浆上升速度（像素/秒） |
| `lava_kill_margin` | float | `10` | 岩浆死亡容差 |

---

## 11. 导出与转换

### 11.1 导出

Tiled 中 `文件 → 另存为` → 选择 JSON 格式：

```
maps/level1/level.tiled.json
```

### 11.2 转换为游戏格式

打开终端，运行：

```powershell
python tools/tiled_converter.py maps/level1/level.tiled.json
```

这会在同级目录生成 `level.json`，游戏直接读取这个文件。

### 11.3 运行游戏查看效果

```powershell
python main.py
```

游戏启动后会自动加载 `maps/level1/level.json`（如果存在）。

---

## 12. 查看美术需求

运行游戏后，`arts/needs/` 文件夹下会自动生成：

- `level1_needs.json` — 背景图需求规格
- `level1_needs.txt` — 人类可读版本

美术设计师打开 `level1_needs.txt` 即可看到：
- 地图实际尺寸 (如 640×1120)
- 摄像机视野范围 (800×600)
- 推荐的背景图尺寸

---

## 13. 完整示例：创建 level2

```text
1. 打开 Tiled
2. 新建 20×35 格, 32×32px 地图
3. 创建图层: Player, Walls, Items, Hazards, Paths
4. 在 Player 层放置出生点 (object_type=player_start, angle=270)
5. 在 Walls 层画墙壁矩形，勾选 fragile/goal/moving 等属性
6. 在 Items 层放道具矩形 (object_type=item, prefab=length_up)
7. 在 Hazards 层放危险物矩形 (object_type=hazard, prefab=spike)
8. 在 Paths 层画 Polyline 路径 (object_type=path, path_id=...)
9. 给移动墙和路径设置相同的 path_id
10. 保存为 maps/level2/level.tiled.json
11. 运行: python tools/tiled_converter.py maps/level2/level.tiled.json
12. 修改 core/game.py 中的 start_game 加载 level2
13. 运行游戏测试
```

---

## 14. 常见问题

### Q: 道具可以和墙壁放在同一个位置吗？
**可以。** 道具使用独立的 Rect 碰撞检测。在 Tiled 中直接把道具矩形拖到墙壁矩形上即可。玩家抓住该位置的墙壁时会同时获得道具。

### Q: 墙壁可以不按格子对齐吗？
**可以。** 矩形对象支持任意 x/y/width/height，不限于格子边界。你可以创建任意尺寸和位置的墙壁。

### Q: 如何让一面墙同时是脆弱的又是终点？
同时勾选 `fragile=true` 和 `goal=true`。但注意：如果 fragile 会导致脱锚后碎裂，那 goal 的胜利条件可能不会触发——建议不要这样组合。

### Q: 背景图要画多大？
运行一次游戏后查看 `arts/needs/level1_needs.txt`，里面有精确的推荐尺寸。
