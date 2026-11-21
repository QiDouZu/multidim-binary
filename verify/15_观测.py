# -*- coding: utf-8 -*-
# Verify observation = continuous dimension reduction.
# R1: keeping m of n axes keeps magnitude sqrt(m/n) (measured, n=4/6/8)
# R2: reducing step by step == reducing in one go (multiplication is associative)
# R3: 3D -> 2D, the 26 directions fall into four keep-ratios 0, 1/2, 2/3, 1
# R4: the complementary loss ratios 1, 1/2, 1/3, 0 have counts 8/8/8/2
from fractions import Fraction as F
from itertools import product
from math import sqrt
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def mag(v):
    return sqrt(sum(x * x for x in v))


# R1: random +/-1 vectors, keep first m of n axes, ratio = sqrt(m/n)
def lcg(seed):
    s = seed & 0xFFFFFFFF
    def nxt():
        nonlocal s
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        return s
    return nxt


ok1 = True
rnd = lcg(20261121)
for n in (4, 6, 8):
    for m in range(1, n):
        tot = 0.0
        cnt = 4000
        for _ in range(cnt):
            v = [1 if (rnd() % 2) else -1 for _ in range(n)]
            tot += mag(v[:m]) / mag(v)
        meas = tot / cnt
        want = sqrt(m / n)
        if abs(meas - want) > 2e-3:
            ok1 = False
        print(f"R1 n={n} m={m}: keep={meas:.6f} want={want:.6f}")
print("R1 magnitude ratio == sqrt(m/n):", "PASS" if ok1 else "FAIL")

# R2: step by step equals one go
ok2 = True
v = [3, 4, 0, 0]
one = mag(v[:2]) / mag(v)
step = (mag(v[:3]) / mag(v)) * (mag(v[:2]) / mag(v[:3]))
ok2 = abs(one - step) < 1e-12
print(f"R2 one-go={one:.6f} step-by-step={step:.6f}")
print("R2 step by step == one go:", "PASS" if ok2 else "FAIL")

# R3/R4: 3D -> 2D, four keep ratios, and the complementary loss counts
d3 = [w for w in product([-1, 0, 1], repeat=3) if any(x != 0 for x in w)]
keep = {}
for w in d3:
    r = round(mag(w[:2]) / mag(w), 6)
    keep[r] = keep.get(r, 0) + 1
want_keep = {0.0: 2, round(sqrt(0.5), 6): 8, round(sqrt(2 / 3), 6): 8, 1.0: 8}
ok3 = (keep == want_keep)
print(f"R3 3D->2D keep ratios: {dict(sorted(keep.items()))}")
print("R3 four keep-ratios 0/1/2/3/1:", "PASS" if ok3 else "FAIL")

loss = {}
for w in d3:
    L = round(1 - (mag(w[:2]) / mag(w)) ** 2, 6)
    loss[L] = loss.get(L, 0) + 1
want_loss = {0.0: 8, round(1 / 3, 6): 8, 0.5: 8, 1.0: 2}
ok4 = (loss == want_loss)
print(f"R4 loss ratios: {dict(sorted(loss.items()))}")
print("R4 loss 1/1/2/1/3/0 with counts 8/8/8/2:", "PASS" if ok4 else "FAIL")

# m = n keeps everything (trivial but should hold)
ok5 = all(abs(mag(w[:3]) / mag(w) - 1.0) < 1e-12 for w in d3)
print("R5 m=n keeps 100%:", "PASS" if ok5 else "FAIL")

print()
print("n=4 -> 1 dim keeps 1/2; n=16 -> 1 dim keeps 1/4; n=64 -> 1 dim keeps 1/8")
for n in (4, 16, 64):
    print(f"  n={n}: sqrt(1/{n}) = {sqrt(1/n):.6f}")

all_ok = ok1 and ok2 and ok3 and ok4 and ok5
print()
print("ALL:", "PASS" if all_ok else "FAIL")
sys.exit(0 if all_ok else 1)
