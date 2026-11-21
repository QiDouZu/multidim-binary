# -*- coding: utf-8 -*-
# 运行环境: 8 维存储 + 时间轴
# 信息的位置 = 当时位置 + 时间演变（能算出来）
# 演变: 每帧整体沿格点平移 1 格（c = 1 格/帧），周期 = 256
import random
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

N = 8
TOTAL = 2 ** N          # 256

rnd = random.Random(42)
init = [rnd.randrange(2) for _ in range(TOTAL)]

def evolve(i, t):
    """第 i 格的信息, 经过 t 帧后在哪个格"""
    return (i + t) % TOTAL

def state_after(t):
    """t 帧后的世界: 位置 -> 值"""
    s = [None] * TOTAL
    for i in range(TOTAL):
        s[evolve(i, t)] = init[i]
    return s

print("=== 8 维存储 + 时间轴 ===")
print(f"  总格点 = 2^{N} = {TOTAL}")
print(f"  演变规则: 每帧整体平移 1 格（c = 1 格/帧），周期 {TOTAL}")
print()
print("帧 t | 信息从 0 号格跑到 | 算位置读(一致?) | 按原位置读(错几个)")

ok_all = True
for t in (0, 1, 2, 3, 7, 13, 64, 128, 255, 256, 300):
    st = state_after(t)
    # 算位置读
    got = [st[evolve(i, t)] for i in range(TOTAL)]
    ok = got == init
    ok_all = ok_all and ok
    # 反例: 按原位置读
    got_bad = [st[i] for i in range(TOTAL)]
    wrong = sum(1 for a, b in zip(got_bad, init) if a != b)
    print(f"{t:>4} | {evolve(0, t):>17} | {'一致' if ok else '错':>14} | {wrong:>4}/{TOTAL}")

print()
print(f"结论: 把时间算进去 -> {'t 全一致' if ok_all else '有错'}")

print()
print("=== 为什么必须算演变 ===")
print("  信息不在原地：t 帧后它跑到 evolve(i,t)")
print("  按原位置读 => 读到的是【别的信息】（t>0 时错一半左右）")
print("  按算出来的位置读 => 100% 一致")
