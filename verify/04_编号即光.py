# -*- coding: utf-8 -*-
# 形式: 多维二进制存 + 坐标定位 + 编号读取
# 编号 = 光的顺序 = 三进制数 (每位 0=正读 1=反读 2=读坐标)
# 末位 = 时间轴, 恒为「正读」
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SYM = {0: "+", 1: "-", 2: "·"}

def num_to_order(k, n):
    """编号 k -> 读法 (长度 n). 前 n-1 位是三进制, 末位恒 +"""
    free = n - 1
    digits = []
    for _ in range(free):
        digits.append(k % 3)
        k //= 3
    digits.reverse()
    return tuple(digits) + (0,)   # 0 = 正读

def read(bits, order):
    """按 order 读 bits. 返回 (读回的串, 读到的坐标列表)"""
    out = []
    coords = []
    for i, (b, d) in enumerate(zip(bits, order)):
        if d == 2:                 # 读坐标: 值不进来, 记位置编号
            out.append("?")
            coords.append(i)
        elif d == 1:               # 反读: 内容一致, 方向反
            out.append(b)
        else:                      # 正读
            out.append(b)
    return "".join(out), coords

for n in (2, 3):
    total = 3 ** (n - 1)
    data = "1" * n if n == 2 else "101"
    print(f"\n=== n={n}  数据(存在多维二进制里, 不动) = {data}  编号 0..{total-1} ===")
    print("编号 | 三进制 | 读法 | 读到 | 读到的坐标")
    for k in range(total):
        order = num_to_order(k, n)
        got, coords = read(data, order)
        tri = "".join(str(d) for d in order[:-1])
        print(f"{k:>4} | {tri:>6} | {''.join(SYM[d] for d in order)} | {got} | {coords}")

print("\n=== 关键: 数据不动, 只换编号 ===")
n = 3
data = "101"
print(f"存储不变: {data}")
for k in (0, 1, 2, 3, 4, 8):
    order = num_to_order(k, n)
    got, coords = read(data, order)
    print(f"  编号 {k} ({''.join(SYM[d] for d in order)}) -> {got}")

print("\n=== 编号数 = 光 = 3^(n-1) ===")
for n in range(1, 6):
    print(f"  n={n}: 编号 0..{3**(n-1)-1}  共 {3**(n-1)} 个")
