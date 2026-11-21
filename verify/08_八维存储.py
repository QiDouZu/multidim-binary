# -*- coding: utf-8 -*-
# 运行环境: 8 维存储信息
# 8 维, 每维 2 个位置 => 2^8 = 256 个格点 = 32 字节
# 全维度公式在 n=8: 段长 1/128, 张角 360/128, 光 3^7 = 2187, 方向 2^7 = 128
import random
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

N = 8
SIDE = 2
TOTAL = SIDE ** N

print("=== 8 维的运行环境参数（全维度公式）===")
print(f"  维数 n        = {N}")
print(f"  每维位置      = {SIDE}")
print(f"  总格点 2^n    = {TOTAL}  （= 32 字节）")
print(f"  段长 1/2^(n-1)= 1/{2**(N-1)} = {1/2**(N-1):.10f}")
print(f"  张角 360/2^(n-1) = {360/2**(N-1):.4f}°")
print(f"  光 3^(n-1)    = {3**(N-1)}")
print(f"  方向 2^(n-1)  = {2**(N-1)}")
print()
print("=== 同一个 256 的几种写法 ===")
print(f"  2^8 = {2**8}   8 维二态")
print(f"  4^4 = {4**4}   4 维四态")
print(f"  3^8 = {3**8}   8 维三态（= 全格点）")
print(f"  2^8 = 256 = 一字节 = 8 bit")

# ---- 存: 把 256 bit 铺到 8 维格点 ----
rnd = random.Random(42)
data = [rnd.randrange(2) for _ in range(TOTAL)]

def flat_to_coord(i, n=N, side=SIDE):
    c = []
    for _ in range(n):
        c.append(i % side)
        i //= side
    return tuple(reversed(c))

store = {}
for i, bit in enumerate(data):
    store[flat_to_coord(i)] = bit

# ---- 读: 按同一坐标读回 ----
got = [store[flat_to_coord(i)] for i in range(TOTAL)]
ok_full = got == data
print()
print("=== 存 / 取 ===")
print(f"  存了 {TOTAL} 个 bit")
print(f"  原样取回: {'100% 一致' if ok_full else '不一致'}")

# ---- 降一维: 去掉最后一维 ----
nd = N - 1
seen = {}
for c, v in store.items():
    key = c[:-1]          # 丢掉最后一位
    seen.setdefault(key, []).append((c[-1], v))

pair_loss = sum(1 for k, vs in seen.items() if len(vs) == 2 and vs[0][1] != vs[1][1])
print()
print("=== 降到 7 维（丢掉最后一维）===")
print(f"  7 维格点 2^7 = {2**nd}")
print(f"  有多少格点是「两个值不同、只能留一个」: {pair_loss} / {2**nd}")
print(f"  信息丢失: {pair_loss / TOTAL * 100:.1f}% 的原始 bit 无法区分")

# ---- 升回 8 维: 能恢复吗 ----
recover = []
for i in range(TOTAL):
    c = flat_to_coord(i)
    key = c[:-1]
    vs = seen[key]
    # 只能拿到「这一对里的第一个」, 不知道原值
    recover.append(vs[0][1])
ok_back = recover == data
print()
print("=== 升回 8 维（把降维后的值补回去）===")
print(f"  恢复: {'一致' if ok_back else '不一致（降到 7 维丢掉的那一半回不来）'}")
