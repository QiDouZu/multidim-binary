# -*- coding: utf-8 -*-
# 两点相撞: 撞出的物质也是维度固定
# n 维里取两个单位向量, 夹角 = 最小角 theta_n = 360/2^(n-1)
# 相撞 -> 向内(物质) = 1 - cos(theta), 弹回(反射) = 1 + cos(theta), 和 = 2
# 下一维在上个维度基础上再加 (M 累加)
import math
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def two_points(n):
    """两个单位向量, 夹角 = 最小角. 返回 (v1, v2, 夹角)"""
    tmin = 360.0 / 2 ** (n - 1)          # 最小角（度）
    th = math.radians(tmin)
    v1 = [0.0] * n
    v1[0] = 1.0
    v2 = [0.0] * n
    v2[0] = math.cos(th)
    v2[1] = math.sin(th)
    return v1, v2, tmin

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

print("=== 两点相撞：撞出的物质是维度固定 ===")
print("n | 维数 | 夹角° | 点积(cos) | 物质 1-cos | 弹回 1+cos | 和 | 累计 M(n)")
print("-" * 100)

M = 0.0
rows = []
for n in range(2, 10):
    v1, v2, tmin = two_points(n)
    c = dot(v1, v2)
    m = 1 - c
    r = 1 + c
    M += m
    rows.append((n, tmin, m, M))
    print(f"{n:>2} | {n:>4} | {tmin:>6.3f} | {c:>9.6f} | {m:>10.6f} | {r:>10.6f} | {m+r:>3.1f} | {M:>10.6f}")

print()
print("=== 对照: 理论值 1 - cos(360/2^(n-1)) 是否一致 ===")
ok = True
for n, tmin, m, _ in rows:
    theo = 1 - math.cos(math.radians(tmin))
    if abs(theo - m) > 1e-12:
        ok = False
print("  两点夹角算出来的 vs 直接代入最小角:", "完全一致" if ok else "有差")

print()
print("=== 每一维撞出的物质（定值）===")
for n, tmin, m, cum in rows:
    print(f"  n={n}: 最小角 {tmin:>8.4f}°  ⇒ 撞出物质 {m:.9f}   累计 {cum:.9f}")

print()
print("=== 反向: 物质 = 2 - 反物质，成对出现 ===")
for n, tmin, m, cum in rows[:4]:
    print(f"  n={n}: 物质 {m:.6f} + 反物质 {2-m:.6f} = 2.000000")
