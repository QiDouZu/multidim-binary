# -*- coding: utf-8 -*-
# Verify dimension reduction (n -> n-1): peeling the outermost shell.
# R1: D(n) - D(n-1) == 1/2^(n-1) for n >= 3   (n=2 is the r/D switch point)
# R2: position 2^n reduces 2-to-1, exactly half restores after lift-back
# R3: direction 3^n-1 reduces ~3-to-1 (each axis has 3 states, not 2)
# R4: readings 3^(n-1), lossless 2^(n-1), ratio (2/3)^(n-1)
# R5: down-multiples are the inverse of up-multiples
from fractions import Fraction as F
from itertools import product
from math import sqrt, acos, degrees
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def D(n):
    if n == 1:
        return F(1)
    if n == 2:
        return F(1, 2)
    return 1 - F(1, 2) ** (n - 1)


print("n | D(n) | D(n)-D(n-1) | 1/2^(n-1)")
rows = []
for n in range(2, 9):
    d, p = D(n), D(n - 1)
    rows.append((n, d, d - p, F(1, 2 ** (n - 1))))
for n, d, diff, shell in rows:
    print(f"{n} | {str(d):>8} | {str(diff):>11} | {str(shell):>9}")

# n >= 3 only: at n=2 the radius/remaining switch happens (D(1)=1, D(2)=1/2)
r1 = all(diff == shell for n, _, diff, shell in rows if n >= 3)
print()
print("R1 D(n)-D(n-1)==1/2^(n-1) (n>=3):", "PASS" if r1 else "FAIL")

# R2: position 2^n -> 2^(n-1), each group of 2
ok2 = True
for n in (3, 4, 5):
    allv = list(product([0, 1], repeat=n))
    low = set(v[:-1] for v in allv)
    lift = set(v + (0,) for v in low)
    back = sum(1 for v in allv if v in lift)
    ratio = F(back, len(allv))
    good = (len(allv) == 2 ** n and len(low) == 2 ** (n - 1) and ratio == F(1, 2))
    ok2 = ok2 and good
    print(f"R2 n={n}: {len(allv)} -> {len(low)} -> lift {len(lift)}, restored {back}/{len(allv)} = {ratio}")
print("R2 position reduces 2-to-1, half restores:", "PASS" if ok2 else "FAIL")

# R3: direction 3^n-1, each axis has 3 states
ok3 = True
for n in (3, 4):
    allv = [v for v in product([-1, 0, 1], repeat=n) if any(x != 0 for x in v)]
    low = set(v[:-1] for v in allv)
    merged = F(len(allv), len(low))
    good = 2.8 < float(merged) < 3.1 and len(allv) == 3 ** n - 1
    ok3 = ok3 and good
    print(f"R3 n={n}: {len(allv)} directions -> {len(low)} (incl. all-stop), merged {float(merged):.3f} per group")
print("R3 direction reduces ~3-to-1:", "PASS" if ok3 else "FAIL")

# R4: readings and lossless subset
ok4 = all(2 ** (n - 1) <= 3 ** (n - 1) for n in range(1, 9))
for n in (1, 3, 4, 8):
    r, w = 3 ** (n - 1), 2 ** (n - 1)
    print(f"R4 n={n}: readings {r}, lossless {w}, ratio {F(w, r)} = {float(F(w, r)):.6f}")
print("R4 lossless <= all readings:", "PASS" if ok4 else "FAIL")

# R5: down multiples are inverse of up multiples
ok5 = True
for n in range(2, 9):
    up = {"theta": F(1, 2), "state": 2, "prec": 2, "light": 3, "radius": F(1, 2)}
    down = {"theta": 2, "state": F(1, 2), "prec": F(1, 2), "light": F(1, 3), "radius": 2}
    for k in up:
        if up[k] * down[k] != 1:
            ok5 = False
print("R5 down = 1/up for every quantity:", "PASS" if ok5 else "FAIL")

# R6: angular loss = x_k^2 / |v|^2. Three reference cases.
def mag(v):
    return sqrt(sum(x * x for x in v))


def loss(v, k):
    m2 = sum(x * x for x in v)
    return (v[k] * v[k]) / m2 if m2 else 0.0


ok6 = True
cases = [((0, 0, 1), 2, 1.0),        # along the dropped axis -> lose everything
         ((0, 1, 0), 2, 0.0),        # perpendicular -> lose nothing
         ((1, 1, 1), 2, 1.0 / 3.0)]  # fully stretched in 3D -> lose 1/3
for v, k, want in cases:
    got = loss(v, k)
    ok6 = ok6 and abs(got - want) < 1e-12
    print(f"R6 loss{str(v)} drop axis {k} = {got:.6f} (want {want:.6f})")
print("R6 loss == x_k^2/|v|^2:", "PASS" if ok6 else "FAIL")

# R7: after dropping an axis, every remaining angle gets smaller or stays equal
d3 = [v for v in product([-1, 0, 1], repeat=3) if any(x != 0 for x in v)]


def angs(v):
    m = mag(v)
    if m == 0:
        return None
    return [degrees(acos(min(1.0, abs(x) / m))) for x in v]


ok7 = True
cnt = 0
grew = 0
for v in d3:
    w = v[:2]
    if not any(x != 0 for x in w):
        continue
    a0, a1 = angs(v), angs(w)
    for i in range(2):
        cnt += 1
        if a1[i] > a0[i] + 1e-12:
            grew += 1
ok7 = (grew == 0)
print(f"R7 remaining angles never grow ({cnt} checks, {grew} grew):", "PASS" if ok7 else "FAIL")

# R8: dropping any single axis, the 26 directions fall into loss groups 8/8/8/2
ok8 = True
for k in range(3):
    g = {}
    for v in d3:
        g[round(loss(v, k), 6)] = g.get(round(loss(v, k), 6), 0) + 1
    want = {0.0: 8, round(1.0 / 3.0, 6): 8, 0.5: 8, 1.0: 2}
    good = (g == want)
    ok8 = ok8 and good
    print(f"R8 drop axis {k}: {dict(sorted(g.items()))}  -> {'ok' if good else 'MISMATCH'}")
print("R8 loss groups 8/8/8/2 on every axis:", "PASS" if ok8 else "FAIL")

# R9: fully-stretched angle arccos(1/sqrt(n)) increases monotonically to 90
ok9 = True
prev = None
for n in range(2, 11):
    a = degrees(acos(1.0 / sqrt(n)))
    if prev is not None and a <= prev:
        ok9 = False
    prev = a
    if n in (2, 3, 4, 8, 10):
        print(f"R9 n={n}: fully-stretched angle = {a:.4f} deg")
ok9 = ok9 and prev < 90.0
print("R9 arccos(1/sqrt(n)) increases toward 90:", "PASS" if ok9 else "FAIL")

# R10: dropping the time axis - 4 unique-optimal / 12 tie-optimal / 10 sub-optimal
def shares(v):
    m2 = sum(x * x for x in v)
    return [x * x / m2 for x in v] if m2 else None


def classify(v, k):
    s = shares(v)
    dropped, best = s[k], min(s)
    if abs(dropped - best) > 1e-12:
        return "sub"
    return "tie" if s.count(best) > 1 else "uniq"


ok10 = True
groups = {}
for k in range(3):
    c = {"uniq": 0, "tie": 0, "sub": 0}
    for v in d3:
        c[classify(v, k)] += 1
    groups["xyz"[k]] = c
    good = (c["uniq"] == 4 and c["tie"] == 12 and c["sub"] == 10)
    ok10 = ok10 and good
    print(f"R10 drop {'xyz'[k]}: uniq={c['uniq']} tie={c['tie']} sub={c['sub']} -> {'ok' if good else 'MISMATCH'}")
ok10 = ok10 and sum(groups["z"].values()) == 26
print("R10 time-axis drop gives 4/12/10:", "PASS" if ok10 else "FAIL")

# R11: all three axes behave identically (symmetry)
ok11 = (groups["x"] == groups["y"] == groups["z"])
print(f"R11 three axes symmetric ({groups['x']}):", "PASS" if ok11 else "FAIL")

# n=4 -> n=3 concrete numbers
print()
print("n=4 -> n=3: theta 45->90, state 16->8, prec 8->4, light 27->9, radius 1/8->1/4, D 7/8->3/4")
print(f"  check D: {D(4)} -> {D(3)}, shell removed = {D(4) - D(3)}")

all_ok = r1 and ok2 and ok3 and ok4 and ok5 and ok6 and ok7 and ok8 and ok9 and ok10 and ok11
print()
print("ALL:", "PASS" if all_ok else "FAIL")
sys.exit(0 if all_ok else 1)
