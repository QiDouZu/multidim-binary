# -*- coding: utf-8 -*-
# 极其高维的坐标, 试试取值
# 全维度公式在 n 极大时: 段长 -> 0, 张角 -> 0, 光 -> 无限
# 而「无限 = 1」 => 归一化之后应该都回到 1
import math
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

print("=== 极其高维：浮点装得下吗 ===")
print("n 维 | ln(光)=(n-1)ln3 | 段长 2^-(n-1) | 张角 360/2^(n-1) | 状态")
for n in (10, 50, 100, 200, 500, 1000, 1024, 1074, 1100, 2000):
    lnlight = (n - 1) * math.log(3)
    seg = math.ldexp(1.0, -(n - 1))
    ang = math.ldexp(360.0, -(n - 1))
    state = []
    if seg == 0.0:
        state.append("段长下溢为 0")
    if not math.isfinite(lnlight):
        state.append("ln(光) 溢出")
    if 3 ** min(n - 1, 3) and n - 1 > 700:
        state.append("光已超浮点上限")
    if not state:
        state.append("正常")
    print(f"{n:>4} | {lnlight:>17.3f} | {seg:>15.3e} | {ang:>15.3e} | {', '.join(state)}")

print()
print("=== 浮点上限/下限在哪 ===")
max_exp = sys.float_info.max_exp
min_exp = sys.float_info.min_exp
print(f"  双精度上限 2^{max_exp} ≈ {sys.float_info.max:.3e}")
print(f"  双精度最小正规数 2^{min_exp} ≈ {sys.float_info.min:.3e}")
print(f"  => 光 3^(n-1) 要溢出: n > {(max_exp*math.log(2))/math.log(3) + 1:.1f}")
print(f"  => 段长 2^-(n-1) 要下溢: n > {-min_exp + 1}")
print(f"  => 二进制能表示的维数上限（段长不归零）约 n = {-min_exp + 1}")

print()
print("=== 归一化之后: 每个量除以它自己的系数, 都是 1 ===")
print("n 维 | 段长 x 2^(n-1) | 张角/360 x 2^(n-1) | 光 / 3^(n-1)")
for n in (1, 3, 10, 100, 1000):
    # 全用对数算, 避免溢出
    a = -(n - 1) + (n - 1)            # ln(段长) + ln(2^(n-1))
    b = (math.log(360) - (n - 1) * math.log(2)) - math.log(360) + (n - 1) * math.log(2)
    c = (n - 1) * math.log(3) - (n - 1) * math.log(3)
    print(f"{n:>4} | exp({a:>5.1f}) = {math.exp(a):.1f} | exp({b:>5.1f}) = {math.exp(b):.1f} | exp({c:>5.1f}) = {math.exp(c):.1f}")

print()
print("=== 结论 ===")
print("  极其高维时，浮点数装不下（段长下溢、光溢出）")
print("  但「每个量除以它自己的系数」恒等于 1 —— 对任何 n 都成立")
print("  => 极高维看到的仍然是一个 1，不是无穷")
print("  => 这就是「无限 = 1」：往上加到装不下，归一化回来还是 1")
