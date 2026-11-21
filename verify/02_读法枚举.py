# -*- coding: utf-8 -*-
# 光 = 二进制的读取顺序（光为向量，一维固定方向）
# 读法: n 位, 前 n-1 位(空间轴)每位三选 {正向, 反向, 不动}, 末位(时间轴)固定一个方向
# 总数 应 = 3^(n-1) = 光
# 不动的读法 = 2^(n-1) = 方向数 = 张角分母
import itertools
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

NAME = {1: "+", -1: "-", 0: "·"}   # 正向 / 反向 / 不动

def read_ways(n):
    """前 n-1 位 in {+1,-1,0}; 末位(时间)固定 +1 (一维固定方向)"""
    free = n - 1
    return [tuple(c) + (1,) for c in itertools.product([1, -1, 0], repeat=free)]

print("=== 读法枚举：光 = 二进制的读取顺序（末位时间轴固定 + 方向）===")
for n in range(1, 5):
    ways = read_ways(n)
    total = len(ways)
    no_still = [w for w in ways if 0 not in w]      # 全部是方向，没有「不动」
    exp = 3 ** (n - 1)
    dirs = 2 ** (n - 1)
    ok = total == exp and len(no_still) == dirs
    print(f"\nn={n}: 位={n}  读法={total} (3^{n-1}={exp}) {'OK' if ok else 'X'}"
          f"  纯方向(不含·)={len(no_still)} (2^{n-1}={dirs})")
    if n <= 3:
        for w in ways:
            print("      ", "".join(NAME[x] for x in w))

print()
print("=== 一维/二维/三维二进制 × 全维度公式 ===")
hdr = "n | 二进制态2^n | 位 | 读法=光3^(n-1) | 纯方向2^(n-1) | 张角360/2^(n-1) | 段长1/2^(n-1)"
print(hdr)
print("-" * len(hdr))
for n in range(1, 9):
    states = 2 ** n
    dirs = 2 ** (n - 1)
    glow = 3 ** (n - 1)
    print(f"{n} | {states:>10} | {n:>2} | {glow:>12} | {dirs:>13} | {360/dirs:>15g} | {1/dirs:>14g}")

print()
print("=== 三个维度展开（他要的：一维/二维/三维）===")
for n in (1, 2, 3):
    states = 2 ** n
    dirs = 2 ** (n - 1)
    glow = 3 ** (n - 1)
    print(f"\n--- n={n} ---")
    print(f"  二进制: {n} 位 -> {states} 个状态: " + ", ".join(format(i, f'0{n}b') for i in range(states)))
    print(f"  光(读法): {glow} 种")
    for w in read_ways(n):
        print("      ", "".join(NAME[x] for x in w))
    print(f"  方向(不动的读法): {dirs}  张角 = 360/{dirs} = {360/dirs:g}°  段长 = 1/{dirs} = {1/dirs:g}")

print()
print("恒等式: 光 = 3^(n-1) = 纯方向2^(n-1) + 含不动(3^(n-1)-2^(n-1))")
for n in range(1, 6):
    g, d = 3 ** (n - 1), 2 ** (n - 1)
    print(f"  n={n}: {g} = {d} + {g-d}")
