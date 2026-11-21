# -*- coding: utf-8 -*-
# 存读同序: 按读法存, 按同一读法读, 验往返
# 读法 w[i] in {+1, -1, 0}
#   +1 / -1  => 该位【读值】(反向读信息一致, 只是位序反) => 可无损恢复
#    0       => 该位【读位置】(坐标) => 值不进来 => 该位丢失
# 于是: 恢复率 = 读值的位数 / n  ; 读法不同 -> 信息量不同
import itertools
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def roundtrip(bits, w):
    """按 w 存, 按同一 w 读. 返回读回的串(丢的位置用 '?')"""
    n = len(bits)
    out = [None] * n
    for i, (b, d) in enumerate(zip(bits, w)):
        if d == 0:
            out[i] = "?"          # 只读了位置, 值没读
        else:
            out[i] = b            # 读值: 反向读拿到的仍是同一位(方向反, 内容一致)
    return "".join(out)

print("=== n=3: 9 种读法各自的往返 ===")
n = 3
data = "101"
print(f"原始数据: {data}\n")
NAMES = {1: "+", -1: "-", 0: "·"}
ok_full = 0
total_ok = 0
for w in itertools.product([1, -1, 0], repeat=n - 1):
    w = tuple(w) + (1,)          # 末位时间轴固定 +
    got = roundtrip(data, w)
    keep = sum(1 for d in w if d != 0)
    full = got == data
    ok_full += 1 if full else 0
    total_ok += keep
    print(f'{ "".join(NAMES[d] for d in w) }  ->  {got}   保留 {keep}/{n}  {"(无损)" if full else "(丢 %d 位)" % (n-keep)}')

print(f"\n9 种读法里无损的: {ok_full} 种（应为 2^(n-1)=4）")
print(f"总保留率(按位算): {total_ok}/{9*n} = {total_ok/(9*n):.4f}")

print()
print("=== n=1..6: 读法与信息量 ===")
print("n | 读法3^(n-1) | 无损2^(n-1) | 含丢3^(n-1)-2^(n-1) | 平均保留率")
for n in range(1, 7):
    ways = 3 ** (n - 1)
    lossless = 2 ** (n - 1)
    lossy = ways - lossless
    # 平均保留位数: 全体读法里每位被读值的概率 = 2/3 (对前 n-1 位), 末位恒读
    # 精确枚举: 每位是 · 的读法数 / 总读法数 = (1/3)^(n-1)*... 逐位枚举
    keep_sum = 0
    for w in itertools.product([1, -1, 0], repeat=n - 1):
        keep_sum += sum(1 for d in w if d != 0) + 1   # +1 是末位时间轴恒读
    avg = keep_sum / (ways * n)
    print(f"{n} | {ways:>10} | {lossless:>10} | {lossy:>18} | {avg:.4f}")
