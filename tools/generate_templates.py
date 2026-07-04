"""
tools/generate_templates.py
一键生成 tiled/templates/ 下所有对象模板 (.tx 文件)
设计师在 Tiled 模板面板中即可拖拽插入预配置的物体。
"""
import json, os

TEMPLATES = {
    # === 墙壁 ===
    "normal_wall.tx": {
        "type": "Wall", "name": "Normal Wall",
        "width": 160, "height": 32,
        "properties": [
            {"name": "wall_type", "type": "string", "value": "normal"},
            {"name": "isSolid", "type": "bool", "value": True},
        ]
    },
    "fragile_wall.tx": {
        "type": "Wall", "name": "Fragile Wall",
        "width": 160, "height": 32,
        "properties": [
            {"name": "wall_type", "type": "string", "value": "fragile"},
            {"name": "fragile", "type": "bool", "value": True},
            {"name": "isSolid", "type": "bool", "value": True},
        ]
    },
    "goal_wall.tx": {
        "type": "Wall", "name": "Goal Wall",
        "width": 96, "height": 32,
        "properties": [
            {"name": "wall_type", "type": "string", "value": "goal"},
            {"name": "goal", "type": "bool", "value": True},
            {"name": "isSolid", "type": "bool", "value": True},
        ]
    },
    "moving_wall.tx": {
        "type": "Wall", "name": "Moving Wall",
        "width": 160, "height": 32,
        "properties": [
            {"name": "wall_type", "type": "string", "value": "normal"},
            {"name": "moving", "type": "bool", "value": True},
            {"name": "move_strategy", "type": "string", "value": "pingpong"},
            {"name": "move_speed", "type": "float", "value": 80},
            {"name": "isSolid", "type": "bool", "value": True},
        ]
    },
    "unstable_wall.tx": {
        "type": "Wall", "name": "Unstable Wall",
        "width": 160, "height": 32,
        "properties": [
            {"name": "wall_type", "type": "string", "value": "normal"},
            {"name": "unstable", "type": "bool", "value": True},
            {"name": "max_tilt_angle", "type": "float", "value": 35},
            {"name": "isSolid", "type": "bool", "value": True},
        ]
    },
    "beat_solid_wall.tx": {
        "type": "Wall", "name": "Beat Solid Wall",
        "width": 160, "height": 32,
        "properties": [
            {"name": "wall_type", "type": "string", "value": "normal"},
            {"name": "beat_solid_switch", "type": "bool", "value": True},
            {"name": "switchSecond", "type": "float", "value": 2.0},
            {"name": "start_solid", "type": "bool", "value": True},
            {"name": "isSolid", "type": "bool", "value": True},
        ]
    },
    "key_pair_wall_to_solid.tx": {
        "type": "Wall", "name": "KeyPair -> Solid",
        "width": 160, "height": 32,
        "properties": [
            {"name": "wall_type", "type": "string", "value": "normal"},
            {"name": "key_pair_solid", "type": "bool", "value": True},
            {"name": "key_pair_result", "type": "string", "value": "solid"},
            {"name": "isSolid", "type": "bool", "value": False},
        ]
    },
    "key_pair_wall_to_ghost.tx": {
        "type": "Wall", "name": "KeyPair -> Ghost",
        "width": 160, "height": 32,
        "properties": [
            {"name": "wall_type", "type": "string", "value": "normal"},
            {"name": "key_pair_solid", "type": "bool", "value": True},
            {"name": "key_pair_result", "type": "string", "value": "ghost"},
            {"name": "isSolid", "type": "bool", "value": True},
        ]
    },
    "ghost_wall.tx": {
        "type": "Wall", "name": "Ghost Wall",
        "width": 160, "height": 32,
        "properties": [
            {"name": "wall_type", "type": "string", "value": "normal"},
            {"name": "isSolid", "type": "bool", "value": False},
        ]
    },

    # === 道具 ===
    "length_up.tx": {
        "type": "Item", "name": "Length Up",
        "width": 32, "height": 32,
        "properties": [
            {"name": "effect", "type": "string", "value": "LengthUp"},
            {"name": "value", "type": "float", "value": 20},
            {"name": "trigger_condition", "type": "string", "value": "OnAnchor"},
        ]
    },
    "length_down.tx": {
        "type": "Item", "name": "Length Down",
        "width": 32, "height": 32,
        "properties": [
            {"name": "effect", "type": "string", "value": "LengthDown"},
            {"name": "value", "type": "float", "value": 20},
            {"name": "trigger_condition", "type": "string", "value": "OnAnchor"},
        ]
    },
    "speed_up.tx": {
        "type": "Item", "name": "Speed Up",
        "width": 32, "height": 32,
        "properties": [
            {"name": "effect", "type": "string", "value": "SpeedUp"},
            {"name": "value", "type": "float", "value": 0.2},
            {"name": "trigger_condition", "type": "string", "value": "OnAnchor"},
        ]
    },
    "speed_down.tx": {
        "type": "Item", "name": "Speed Down",
        "width": 32, "height": 32,
        "properties": [
            {"name": "effect", "type": "string", "value": "SpeedDown"},
            {"name": "value", "type": "float", "value": 0.2},
            {"name": "trigger_condition", "type": "string", "value": "OnAnchor"},
        ]
    },
    "key.tx": {
        "type": "Item", "name": "Key",
        "width": 32, "height": 32,
        "properties": [
            {"name": "effect", "type": "string", "value": "KeyPair"},
            {"name": "trigger_condition", "type": "string", "value": "OnAnchor"},
            {"name": "consume_on_trigger", "type": "bool", "value": True},
        ]
    },
    "checkpoint.tx": {
        "type": "Item", "name": "Checkpoint",
        "width": 64, "height": 64,
        "properties": [
            {"name": "effect", "type": "string", "value": "Checkpoint"},
            {"name": "trigger_condition", "type": "string", "value": "OnTouch"},
            {"name": "consume_on_trigger", "type": "bool", "value": False},
        ]
    },

    # === 障碍物 ===
    "spike.tx": {
        "type": "Hazard", "name": "Spike",
        "width": 32, "height": 32,
        "properties": [
            {"name": "trigger_condition", "type": "string", "value": "OnTouch"},
        ]
    },

    # === 其他 ===
    "player_start.tx": {
        "type": "PlayerStart", "name": "Player Start",
        "width": 0, "height": 0,
        "properties": [
            {"name": "angle", "type": "float", "value": 270},
            {"name": "anchor_side", "type": "string", "value": "left"},
        ]
    },
    "path.tx": {
        "type": "Path", "name": "Path",
        "width": 0, "height": 0,
        "properties": [
            {"name": "path_id", "type": "string", "value": ""},
        ]
    },
}


def main():
    out_dir = "tiled/templates"
    os.makedirs(out_dir, exist_ok=True)
    for filename, obj in TEMPLATES.items():
        template = {"object": obj}
        filepath = os.path.join(out_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(TEMPLATES)} templates → {out_dir}/")


if __name__ == "__main__":
    main()
