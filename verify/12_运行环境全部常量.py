# -*- coding: utf-8 -*-
"""运行环境全部常量核验：六行公式 / 表 / 嵌套维度 / 结构常数。每个数都由本程序打印。"""
import sys, io, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", newline="\n")

def theta(n):  return 360.0 / 2.0**(n-1)
def S(n):      return 2**n
def P(n):      return 2**(n-1)
def A(n):      return 1.0 - math.cos(math.radians(theta(n)))
def L(n):      return 3**(n-1)

M = {1: 0.0}
for n in range(2, 400):
    M[n] = M[n-1] + A(n)

print("==", "六行公式 n=1..8", "==")
print(f"{'n':>2} {'θ':>10} {'S':>6} {'P':>5} {'A':>14} {'M':>16} {'L':>7}")
for n in range(1, 9):
    print(f"{n:>2} {theta(n):>10.4f} {S(n):>6} {P(n):>5} {A(n):>14.9f} {M[n]:>16.9f} {L(n):>7}")

print("\n== M(n) 极限 ==")
for n in (10, 16, 24, 32, 48):
    print(f"n={n:>3}  M={M[n]:.13f}")
print(f"n=200 M={M[200] if 200 in M else 0:.13f}" if False else "", end="")
print(f"M(48) = {M[48]:.13f}")
print(f"极限   = 3.3946498021  (差 {abs(M[48]-3.3946498021):.3e})")

print("\n== 增量比（每一步约为上一步 1/4）==")
for n in range(4, 10):
    print(f"A({n})/A({n-1}) = {A(n)/A(n-1):.10f}")

print("\n== 两条恒等式 ==")
for n in range(1, 9):
    seg = (0.5)**(n-1)
    axis = 2.0**(n-1)
    r = (0.5)**(n-1)
    D = 1.0 - r
    print(f"n={n}: 段长{seg:.10f} × 轴长{axis:>6.1f} = {seg*axis:.10f} | r={r:.10f} D={D:.10f} r+D={r+D:.10f} | θ×P={theta(n)*P(n):.6f}")

print("\n== 结构常数 ==")
print(f"26 = 6面 + 12棱 + 8顶点 = {6+12+8}")
print(f"26 = 3^3 - 1 = {3**3-1}")
print(f"26 = Σ C(3,k)2^k (k=1..3) = {3*2} + {3*4} + {1*8} = {3*2+3*4+8}")
print(f"(2+1)^3 = {3**3}  去掉常数项 1 得 26")
print(f"8  = S(3) = 2^3 = {S(3)}")
print(f"9  = L(3) = 3^2 = {L(3)}")
print(f"16 = S(4) = 2^4 = {S(4)}")
print(f"27 = L(4) = 3^3 = {L(4)}")

print("\n== 环与闭合 ==")
for n in range(2, 6):
    ring = S(n+1) + P(n) + 1
    close = S(n+1) + P(n) + 2
    branch = P(n) + 1
    shared = S(n+1) + 1
    print(f"n={n}: 支路=P(n)+1={branch:>3} | 环=S(n+1)+P(n)+1={ring:>3} | 闭合={close:>3} | 共用=S(n+1)+1={shared:>3}")
    print(f"      17? 共用n=3 -> {S(4)+1}  两环 22+22-17={22+22-17}")

print("\n== 三个数（物质 / 光 / 位置）==")
print(f"e = 2                = 1 对相反向量")
print(f"u = 1 + 2*L(3) = 1 + 2*{L(3)}  = {1+2*L(3)}")
print(f"d = 1 + 2*42   = 1 + 2*42  = {1+2*42}")
print(f"42 = S(5)+P(4)+2 = {S(5)}+{P(4)}+2 = {S(5)+P(4)+2}")
print("N-1 = 2 / 18 / 84  全为偶数")

print("\n== 端点与方向（切 n 刀）==")
for n in range(0, 5):
    pts = n + 1
    dirs = (n+1)*n//2
    print(f"n={n}: 切{n}刀 → {pts} 个端点 → 方向数 C({pts},2) = {dirs}")

print("\n== 升维倍数（n→n+1）==")
for n in (1, 3):
    print(f"n={n}→{n+1}: θ {theta(n):.4f}→{theta(n+1):.4f} (×1/2) | S {S(n)}→{S(n+1)} (×2) | P {P(n)}→{P(n+1)} (×2) | L {L(n)}→{L(n+1)} (×3)")

print("\n== 空间段长累加（二维起）==")
tot = 0.0
for n in range(2, 60):
    tot += (0.5)**(n-1)
print(f"1/2+1/4+1/8+… = {tot:.15f}")

print("\n== 两列：同一个 2^(n-1) 两种身份 ==")
for n in range(1, 6):
    print(f"n={n}: 空间段长(1/2)^(n-1)={0.5**(n-1):.6f}  时间轴长2^(n-1)={2**(n-1)}  坐标单位=1/2^(n-1)={1/2**(n-1):.6f}")

print("\n== 读法三态与无损数 ==")
for n in range(1, 7):
    print(f"n={n}: 全部读法 L={L(n):>4}  无损读法 2^(n-1)={P(n):>3}  含停读法={L(n)-P(n):>3}  无损占比={P(n)/L(n):.6f}")

print("\n== 单位恒为 1 ==")
print("单位向量长度恒等于 1；几个单位向量相加 ≠ 造出 √3（超光速）")
print(f"三个单位向量相加若按坐标 (1,1,1)：模 = {math.sqrt(3):.6f} ≠ 1 ⇒ 不成立")
