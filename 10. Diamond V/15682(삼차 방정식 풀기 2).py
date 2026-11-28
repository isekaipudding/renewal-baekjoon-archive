# 링크 : https://acmicpc.net/problem/15682
import sys
import math
from decimal import Decimal, getcontext

input = sys.stdin.readline
getcontext().prec = 120

EPS_DISC = Decimal("1e-70")
EPS_ZERO = Decimal("1e-50")
EPS_MERGE = Decimal("1e-9")

def compute_pi() -> Decimal:
    # 마친(Machin) 공식: pi = 16 * arctan(1/5) - 4 * arctan(1/239)
    def atan_inv(inv_x:int) -> Decimal:
        x_sq = Decimal(inv_x * inv_x)
        term = Decimal(1) / Decimal(inv_x)
        total = term
        step:int = 1
        while True:
            term = -term / x_sq
            next_total = total + term / Decimal(2 * step + 1)
            if next_total == total:
                break
            total = next_total
            step += 1
        return total

    return Decimal(16) * atan_inv(5) - Decimal(4) * atan_inv(239)

PI = compute_pi()
TWO_PI = Decimal(2) * PI
HALF_PI = PI / Decimal(2)
QUARTER_PI = PI / Decimal(4)

def dec_cos_small(x:Decimal) -> Decimal:
    # |x| <= pi/4 구간 테일러 급수 (약 40항 내외에서 120자리 수렴)
    x_sq = x * x
    term = Decimal(1)
    total = term
    k = 1
    while True:
        term = -term * x_sq / Decimal((2 * k - 1) * (2 * k))
        next_total = total + term
        if next_total == total:
            break
        total = next_total
        k += 1
    return total

def dec_sin_small(x:Decimal) -> Decimal:
    # |x| <= pi/4 구간 테일러 급수
    x_sq = x * x
    term = x
    total = term
    k:int = 1
    while True:
        term = -term * x_sq / Decimal((2 * k) * (2 * k + 1))
        next_total = total + term
        if next_total == total:
            break
        total = next_total
        k += 1
    return total

def dec_cos(angle:Decimal) -> Decimal:
    # 대칭성을 이용해 [0, pi/4] 구간으로 축소 후 계산
    x = angle % TWO_PI
    if x < 0:
        x += TWO_PI
    if x > PI:
        x = TWO_PI - x
    sign = 1
    if x > HALF_PI:
        x = PI - x
        sign = -1

    value = dec_cos_small(x) if x <= QUARTER_PI else dec_sin_small(HALF_PI - x)
    return -value if sign < 0 else value

def dec_asin_small(u:Decimal) -> Decimal:
    # |u| <= 0.5 (|arcsin(u)| <= pi/6 < pi/4) 구간 뉴턴 법
    if u == 0:
        return Decimal(0)
    if abs(u) < Decimal("1e-15"):
        x = u
    else:
        x = Decimal(str(math.asin(float(u))))

    for _ in range(4):
        x -= (dec_sin_small(x) - u) / dec_cos_small(x)
    return x

def dec_acos(y:Decimal) -> Decimal:
    # 끝점(+-1) 근처 정밀도 손실을 막기 위해 반각 항등식으로 |u| <= 0.5 변환
    one = Decimal(1)
    half = Decimal("0.5")
    if y >= one:
        return Decimal(0)
    if y <= -one:
        return PI
    if y > half:
        return Decimal(2) * dec_asin_small(((one - y) / Decimal(2)).sqrt())
    if y < -half:
        return PI - Decimal(2) * dec_asin_small(((one + y) / Decimal(2)).sqrt())
    return HALF_PI - dec_asin_small(y)

def dec_cbrt(value:Decimal) -> Decimal:
    # 실수 세제곱근: 10진 지수 스케일링 초기값 + 뉴턴 법 6회
    if value == 0:
        return Decimal(0)
    is_neg:bool = value < 0
    mag = -value if is_neg else value

    exp3:int = mag.adjusted() // 3
    mantissa = mag.scaleb(-3 * exp3)
    x = Decimal(str(float(mantissa) ** (1.0 / 3.0))).scaleb(exp3)

    two = Decimal(2)
    three = Decimal(3)
    for _ in range(6):
        x = (two * x + mag / (x * x)) / three
    return -x if is_neg else x

def cardano(a_str:str, b_str:str, c_str:str, d_str:str) -> None:
    A = Decimal(a_str)
    B = Decimal(b_str)
    C = Decimal(c_str)
    D = Decimal(d_str)

    # 축약 삼차방정식 t^3 + p*t + q = 0 (x = t - B / (3A))
    shift = B / (Decimal(3) * A)
    p = (Decimal(3) * A * C - B * B) / (Decimal(3) * A * A)
    q = (
        Decimal(2) * B * B * B - Decimal(9) * A * B * C + Decimal(27) * A * A * D
    ) / (Decimal(27) * A * A * A)

    half_q = q / Decimal(2)
    third_p = p / Decimal(3)
    disc = half_q * half_q + third_p * third_p * third_p  # (q/2)^2 + (p/3)^3

    depressed_roots:list = []

    if disc > EPS_DISC:
        # 1. 실근 1개, 허근 2개: -q/2와 같은 부호의 sqrt(disc) 선택으로 유효숫자 상실 방지
        sqrt_disc = disc.sqrt()
        if half_q <= 0:
            u = dec_cbrt(-half_q + sqrt_disc)
        else:
            u = dec_cbrt(-half_q - sqrt_disc)
        v = -third_p / u if u != 0 else Decimal(0)
        depressed_roots.append(u + v)

    elif disc >= -EPS_DISC:
        # 2. 중근 또는 삼중근
        if abs(p) <= EPS_ZERO and abs(q) <= EPS_ZERO:
            depressed_roots.append(Decimal(0))
        else:
            double_root = -(Decimal(3) * q) / (Decimal(2) * p)
            single_root = (Decimal(3) * q) / p
            depressed_roots.extend([double_root, single_root])

    else:
        # 3. Casus irreducibilis (서로 다른 세 실근): 비에트 삼각함수 공식
        radius = Decimal(2) * (-third_p).sqrt()
        cos_3theta = (-half_q) / ((-third_p) ** 3).sqrt()
        if cos_3theta > Decimal(1):
            cos_3theta = Decimal(1)
        elif cos_3theta < Decimal(-1):
            cos_3theta = Decimal(-1)

        theta = dec_acos(cos_3theta) / Decimal(3)
        for k in range(3):
            angle = theta - (TWO_PI * Decimal(k)) / Decimal(3)
            depressed_roots.append(radius * dec_cos(angle))

    roots = sorted(t - shift for t in depressed_roots)
    merged = []
    for root in roots:
        if abs(root) < Decimal("5e-13"):
            root = Decimal(0)
        if not merged or abs(root - merged[-1]) > EPS_MERGE:
            merged.append(root)

    print(" ".join(f"{r:.10f}" for r in merged))

T:int = int(input().rstrip())
for _ in range(T):
    a_str, b_str, c_str, d_str = input().split()
    cardano(a_str, b_str, c_str, d_str)