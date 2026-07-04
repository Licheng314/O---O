"""
physics/geometry.py
几何工具函数
"""

import math


def line_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    """两条线段是否相交"""
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-10:
        return False
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
    return 0 <= t <= 1 and 0 <= u <= 1


def point_to_segment_distance(px, py, ax, ay, bx, by):
    """点到线段的最短距离"""
    abx = bx - ax
    aby = by - ay
    apx = px - ax
    apy = py - ay

    t = max(0, min(1, (apx * abx + apy * aby) / max(abx * abx + aby * aby, 1e-10)))
    closest_x = ax + t * abx
    closest_y = ay + t * aby
    return math.sqrt((px - closest_x) ** 2 + (py - closest_y) ** 2)


def clamp(value, min_val, max_val):
    """夹紧值"""
    return max(min_val, min(max_val, value))


def move_towards(current, target, max_delta):
    """朝目标移动"""
    diff = target - current
    if abs(diff) <= max_delta:
        return target
    return current + max_delta if diff > 0 else current - max_delta
