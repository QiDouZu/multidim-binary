# -*- coding: utf-8 -*-
# Verify the three columns of the precision table are one n.
# R1: seg * axis == 1  (seg = (1/2)^(n-1), axis = 2^(n-1))
# R2: deg * 2^(n-1) == 360
# R3: light == 3^(n-1) and light * (360/light_deg) == 360
from fractions import Fraction as F
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

rows = []
for n in range(1, 9):
    seg = F(1, 2) ** (n - 1)
    axis = 2 ** (n - 1)
    deg = F(360, 2 ** (n - 1))
    light = 3 ** (n - 1)
    rows.append((n, seg, axis, deg, light))

print("n | seg=(1/2)^(n-1) | axis=2^(n-1) | deg=360/2^(n-1) | light=3^(n-1)")
for n, seg, axis, deg, light in rows:
    print(f"{n} | {str(seg):>10} | {str(axis):>10} | {str(deg):>12} | {str(light):>8}")

r1 = all(seg * axis == 1 for _, seg, axis, _, _ in rows)
r2 = all(deg * axis == 360 for _, _, axis, deg, _ in rows)
r3 = all(light == 3 ** (n - 1) for n, _, _, _, light in rows)
# one angle from light: 360/light  (n=1..8 exact fractions)
r4 = all(F(360, light) * light == 360 for *_, light in rows)

print()
print("R1 seg*axis==1        :", "PASS" if r1 else "FAIL")
print("R2 deg*axis==360      :", "PASS" if r2 else "FAIL")
print("R3 light==3^(n-1)     :", "PASS" if r3 else "FAIL")
print("R4 (360/light)*light  :", "PASS" if r4 else "FAIL")

# cross check: n=3 -> seg 1/4, deg 90, light 9, one angle 40
n = 3
seg = F(1, 2) ** (n - 1)
deg = F(360, 2 ** (n - 1))
light = 3 ** (n - 1)
print()
print(f"n=3 check: seg={seg} deg={deg} light={light} one_angle=360/{light}={F(360, light)}")
print("n=3 seg*axis =", seg * 2 ** (n - 1), "| 90*axis =", deg * 2 ** (n - 1))
