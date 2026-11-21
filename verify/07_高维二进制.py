# -*- coding: utf-8 -*-
# v2: fix unpacking bug in v1 (angden / n were not bound -> false FAIL)
from fractions import Fraction as F
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

rows = []
for n in range(1, 9):
    states = 2 ** n            # binary: each dim 2 states
    angden = 2 ** (n - 1)      # angle denominator (time dim excluded)
    deg = F(360, angden)
    light = 3 ** (n - 1)       # ternary: each dim 3 states, time dim 1 state
    seg = F(1, angden)
    rows.append({"n": n, "states": states, "angden": angden,
                 "deg": deg, "light": light, "seg": seg})

print("n | states=2^n | angden=2^(n-1) | deg=360/angden | light=3^(n-1) | seg=1/angden")
for r in rows:
    print(f'{r["n"]} | {r["states"]:>10} | {r["angden"]:>13} | {str(r["deg"]):>14} | '
          f'{r["light"]:>13} | {str(r["seg"]):>12}')

ok1 = ok2 = ok3 = ok4 = True
for r in rows:
    if not (r["states"] == 2 * r["angden"]):
        ok1 = False
    if not (r["deg"] * r["angden"] == 360):
        ok2 = False
    if not (r["seg"] * r["angden"] == 1):
        ok3 = False
    if not (len(bin(r["states"] - 1)) - 2 == r["n"]):
        ok4 = False

print()
print("R1 states == 2*angden          :", "PASS" if ok1 else "FAIL")
print("R2 deg * angden == 360         :", "PASS" if ok2 else "FAIL")
print("R3 seg * angden == 1           :", "PASS" if ok3 else "FAIL")
print("R4 states needs exactly n bits :", "PASS" if ok4 else "FAIL")

# geometry: binary states == vertices of n-cube ; ternary == full grid ; minus 1 == neighbours
print()
print("--- 二进制 = 顶点, 三态 = 全格点, 减 1 = 邻居 ---")
for n in range(1, 9):
    verts = 2 ** n
    grid = 3 ** n
    nbr = grid - 1
    print(f"n={n}: 2^n={verts:>4} (顶点)  3^n={grid:>6} (全格点)  3^n-1={nbr:>6} (邻居)")

# ratio light/angden = (3/2)^(n-1)
print()
print("light / angden = (3/2)^(n-1):")
for r in rows:
    print(f'  n={r["n"]}: {r["light"]}/{r["angden"]} = {F(r["light"], r["angden"])} = {r["light"]/r["angden"]:.6f}')

# per-step deltas
print()
print("--- 每切一刀 ---")
for i in range(1, len(rows)):
    a, b = rows[i - 1], rows[i]
    print(f'n={a["n"]}->{b["n"]}: states x{b["states"]//a["states"]}  '
          f'angden x{b["angden"]//a["angden"]}  deg /2  light x{b["light"]//a["light"]}')
