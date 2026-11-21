# -*- coding: utf-8 -*-
# 运行环境的维度表: 一维二进制 -> 二维 -> 三维 ... 每次加完都是定值
# 每维: 状态数 2^n, 最小角 360/2^(n-1), 新增物质 1-cos(最小角), 累计定值 M(n)
import math
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

print("=== 运行环境 · 维度表（每次加完都是定值）===")
print("n | 二进制状态2^n | 新增位 | 最小角° | 这一维新增 | 累计定值 M(n) | 精度 2^(n-1)")
print("-" * 92)

M = 0.0
rows = []
for n in range(1, 13):
    states = 2 ** n
    if n == 1:
        tmin = 360.0
        add = 0.0
    else:
        tmin = 360.0 / 2 ** (n - 1)
        add = 1 - math.cos(math.radians(tmin))
    M += add
    prec = 2 ** (n - 1)
    rows.append(dict(n=n, states=states, tmin=tmin, add=add, M=M, prec=prec))
    print(f"{n:>2} | {states:>13} | +1 位 | {tmin:>7.3f} | {add:>10.6f} | {M:>13.9f} | {prec:>9}")

print()
print("=== 每一层的定值（可直接当运行环境参数）===")
for r in rows:
    print(f"  n={r['n']}: 状态 {r['states']:>5}｜最小角 {r['tmin']:>8.4f}°｜物质定值 {r['M']:.9f}")

print()
print("=== 校验点 ===")
print(f"  n=2: M = {rows[1]['M']:.6f}  （应为 2）")
print(f"  n=3: M = {rows[2]['M']:.6f}  （应为 3）")
print(f"  n=12: M = {rows[-1]['M']:.10f}")
print()
print("=== 定值的性质 ===")
print("  每加一维, M 涨一截然后停住（不再变）")
print("  后一维的增量 = 前一维增量的约 1/4")
for i in range(2, len(rows)):
    a = rows[i - 1]["add"]
    b = rows[i]["add"]
    if a:
        print(f"  n={rows[i]['n']}: 新增 {b:.8f}, 是上一次的 {b/a:.6f}")
