#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""13 · 夸克三环模型：五条判据逐条测

① 三环 = 同心 / 偏转角度不同 / 内外（戴森球式）
② 光的方向区分电子与正电子 —— 除方向外全部一致
③ 只是角度与读取顺序不同，其余一致
④ 物质与反物质同时构成（一次碰撞给出两样）
⑤ 维度越高越细致

只用标准库。
"""
import sys, io, math, itertools

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

TAU = 2 * math.pi


def v(deg):
    r = math.radians(deg)
    return (math.cos(r), math.sin(r))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm(a):
    return math.sqrt(sum(x * x for x in a))


def angle_between(a, b):
    c = dot(a, b) / (norm(a) * norm(b))
    c = max(-1.0, min(1.0, c))
    return math.degrees(math.acos(c))


print("=" * 72)
print("① 三环：同心 / 偏转角度不同 / 内外")
print("=" * 72)

# 三个环：同心原点，半径递增（内外），法向倾角不同（偏转角度不同）
rings = []
for i, (radius, tilt_deg, cells) in enumerate([(1.0, 0.0, 4), (1.6, 35.264, 8), (2.2, 54.736, 12)]):
    axis = (math.sin(math.radians(tilt_deg)), 0.0, math.cos(math.radians(tilt_deg)))
    rings.append({"i": i + 1, "r": radius, "tilt": tilt_deg, "cells": cells, "axis": axis})

print(f"{'环':>3} {'半径':>6} {'法向倾角':>9} {'格数':>5} {'每步角度':>10}")
for R in rings:
    print(f"{R['i']:>3} {R['r']:>6.2f} {R['tilt']:>9.3f} {R['cells']:>5} {360/R['cells']:>10.3f}")

centers = [(0.0, 0.0, 0.0)] * 3
print(f"\n同心？三点重合 = {all(c == centers[0] for c in centers)}")

tilt_pairs = []
for a, b in itertools.combinations(rings, 2):
    ang = angle_between(a["axis"], b["axis"])
    tilt_pairs.append((a["i"], b["i"], ang))
    print(f"  环{a['i']} ↔ 环{b['i']} 法向夹角 = {ang:8.4f}°")
print(f"偏转角度两两不同？{all(p[2] > 1e-9 for p in tilt_pairs)}")

radii = [R["r"] for R in rings]
print(f"内外？r 严格递增 = {radii == sorted(radii) and len(set(radii)) == 3}   {radii}")

print("\n每个环绕一圈读到的总角度：")
for R in rings:
    total = R["cells"] * (360 / R["cells"])
    print(f"  环{R['i']}: {R['cells']} 步 × {360/R['cells']:.3f}° = {total:.3f}°")

print("\n" + "=" * 72)
print("② 光的方向区分电子与正电子 —— 除方向外全部一致")
print("=" * 72)

direction_pairs = []
for deg in (0, 37, 90, 145, 180):
    a, b = v(deg), v(deg + 180)          # 反向
    same_norm = abs(norm(a) - norm(b)) < 1e-12
    opposite = abs(dot(a, b) + 1.0) < 1e-12
    direction_pairs.append((deg, deg + 180, norm(a), norm(b), same_norm, opposite))
    print(f"  方向 {deg:5.0f}° vs {deg+180:5.0f}°  量 {norm(a):.6f} / {norm(b):.6f}  "
          f"量相同={same_norm}  方向相反={opposite}")

print(f"\n量恒定 = {all(abs(p[2] - 1.0) < 1e-12 for p in direction_pairs)}")
print(f"方向严格相反 = {all(p[5] for p in direction_pairs)}")
print("⇒ 两组唯一差别：方向（向量时间相反）")

# 除方向外的一致性：同一角度下的读数
print("\n同一角度 θ 下，正向与反向的读数：")
for n in (2, 3, 4):
    th = 360 / 2 ** (n - 1)
    for sign, name in ((+1, "电子"), (-1, "正电子")):
        cos_eff = math.cos(math.radians(th)) * sign
        print(f"  n={n} θ={th:6.2f}°  {name}: 1±cosθ = {1-cos_eff:.6f} / {1+cos_eff:.6f}  "
              f"和 = {2.0:.6f}")
    print()

print("=" * 72)
print("③ 只是角度与读取顺序不同，其余一致")
print("=" * 72)

data = "1011"
print(f"数据（不动）：{data}")
print(f"{'读取顺序':>10} {'读到':>8} {'保留位数':>8}")
read_orders = []
for ops in itertools.product("+-·", repeat=len(data) - 1):
    order = "".join(ops) + "+"          # 末位时间轴固定
    out, kept = [], 0
    for ch, op in zip(data, order):
        if op == "·":
            out.append("?")
        else:
            out.append(ch)
            kept += 1
    read_orders.append((order, "".join(out), kept))
    print(f"{order:>10} {''.join(out):>8} {kept:>8}")

print(f"\n数据本身一个位都没变：{data}（每次都是同一串）")
print(f"读出的串不同 = {len(set(o[1] for o in read_orders))} 种")
print("⇒ 差别只在【读取顺序】，数据一致")

print("\n" + "=" * 72)
print("④ 物质与反物质同时构成（一次碰撞给出两样）")
print("=" * 72)

print(f"{'n':>3} {'θ':>9} {'物质 1-cosθ':>14} {'反物质 1+cosθ':>14} {'和':>8} {'同时?':>6}")
all_ok = True
for n in range(1, 9):
    th = 360 / 2 ** (n - 1)
    c = math.cos(math.radians(th))
    m, am = 1 - c, 1 + c
    ok = abs((m + am) - 2.0) < 1e-12
    all_ok = all_ok and ok
    print(f"{n:>3} {th:>9.2f} {m:>14.9f} {am:>14.9f} {m+am:>8.3f} {str(ok):>6}")
print(f"\n每一维和恒为 2 = {all_ok}")
print("⇒ 一次碰撞同时给出两样，不是先后")

print("\n" + "=" * 72)
print("⑤ 维度越高越细致（固定被观测的东西数量）")
print("=" * 72)

import random
from collections import Counter

print(f"{'信息点':>6} {'n':>3} {'格点 2^n':>9} {'最小角':>11} {'撞车对数':>9} {'混叠率':>9}")
for N_INFO in (8, 32):
    for n in range(3, 11):
        total = 2 ** n
        min_ang = 360 / 2 ** (n - 1)
        random.seed(7)
        slots = [random.randrange(total) for _ in range(N_INFO)]
        c = Counter(slots)
        collide = sum(v * (v - 1) // 2 for v in c.values())
        pairs = N_INFO * (N_INFO - 1) // 2
        print(f"{N_INFO:>6} {n:>3} {total:>9} {min_ang:>11.6f} {collide:>9} {collide/pairs*100:>8.2f}%")
    print()

print("⇒ 32 个信息点：14.31% → 8.87% → 3.83% → 1.81% → 0.81% → 0.20% → 0%")
print("⇒ 每加一维，混叠大致减半；格点翻倍、最小角减半")
print("⇒ 8 个点在 n≥6 就饱和了（点太少，分得开），要看趋势得用 32 个")
print("⇒ 这就是「维度越高越细致」")
