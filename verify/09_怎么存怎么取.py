# -*- coding: utf-8 -*-
# 怎么存就怎么取: 用全维度公式的坐标做存储结构, 验往返
# 位置 = 对半切 k 刀出来的格点: 每维 2^k 个位置, 段长 = 1/2^k, 张角 = 360/2^k
# 存: 把值写到 n 维坐标上;  取: 按【同一个坐标】读回
import random
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def run(k, n, count, seed=42):
    rnd = random.Random(seed)
    side = 2 ** k                      # 每维位置数 = 2^k
    total = side ** n                  # 总格点
    count = min(count, total)          # 不能超过总格点数
    seg = 1 / side                     # 段长 = 1/2^k
    ang = 360 / side                   # 张角 = 360/2^k
    light = 3 ** k                     # 光 = 3^k

    # 造数据: 从全部坐标里无放回抽样
    all_coords = []
    idx = list(range(total))
    rnd.shuffle(idx)
    for j in idx[:count]:
        c, rem = [], j
        for _ in range(n):
            c.append(rem % side)
            rem //= side
        all_coords.append(tuple(reversed(c)))
    coords = [(c, rnd.randrange(1000)) for c in all_coords]

    store = {c: v for c, v in coords}

    # 取 A: 按同一个坐标取
    got_a = [(c, store[c]) for c, _ in coords]
    ok_a = got_a == coords

    # 取 B: 打乱顺序, 但坐标跟着值走
    order = list(range(len(coords)))
    rnd.shuffle(order)
    got_b = [(coords[i][0], coords[i][1]) for i in order]
    ok_b = all(store[c] == v for c, v in got_b)

    # 取 C: 反例 -- 只按位置序号取, 不看坐标
    flat = [v for _, v in coords]
    shuffled_vals = [flat[i] for i in order]
    ok_c = shuffled_vals == flat

    return dict(k=k, n=n, side=side, total=total, seg=seg, ang=ang, light=light,
                ok_a=ok_a, ok_b=ok_b, ok_c=ok_c, count=count)

print("=== 全维度公式的存储结构 ===")
print("k 刀 | 每维位置2^k | 段长1/2^k | 张角360/2^k | 光3^k")
for k in range(1, 7):
    print(f"{k:>4} | {2**k:>10} | {1/2**k:>10g} | {360/2**k:>11g} | {3**k:>6}")

print()
print("=== 怎么存怎么取（n=3）===")
print("k | 位置数/维 | 总格点 | 取样 | 存取(带坐标) | 打乱顺序(带坐标) | 只按序号(反例)")
for k in (1, 2, 3, 4):
    r = run(k, n=3, count=60)
    print(f'{r["k"]} | {r["side"]:>9} | {r["total"]:>6} | {r["count"]:>4} | '
          f'{"一致" if r["ok_a"] else "错":>12} | '
          f'{"一致" if r["ok_b"] else "错":>16} | '
          f'{"一致" if r["ok_c"] else "错":>15}')

print()
print("结论:")
print("  1) 带坐标存、带坐标取 -> 永远一致（存的位置就是取的位置）")
print("  2) 坐标带着值走，顺序怎么打乱都一致")
print("  3) 只记顺序、不记坐标 -> 顺序一变就错")
print("  => 「存的位置就是取的位置」= 必须【坐标跟着数据】")
