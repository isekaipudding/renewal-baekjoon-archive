# 링크 : https://acmicpc.net/problem/17468
import sys
from decimal import Decimal, setcontext, Context, MAX_PREC, MAX_EMAX

input = sys.stdin.readline
sys.set_int_max_str_digits(0)

setcontext(Context(prec=MAX_PREC, Emax=MAX_EMAX))

# Python의 오버헤드를 피하면서 다항식 합성곱을 위해
# 다항식을 거대한 정수로 바꾼 뒤 두 수를 곱합니다.
# 이것은 큰 수 곱셈 문제를 보면 왜 그런지 바로 이해할 수 있을 것입니다.
def kronecker_multiply_decimal(
    poly_a:list,
    poly_b_str:str,
    len_b:int,
    pad_size:int,
    f_str:str,
) -> list:
    d:int = len(poly_a) - 1

    dec_a:Decimal = Decimal("".join(format(x, f_str) for x in poly_a))
    dec_b:Decimal = Decimal(poly_b_str)
    dec_c:Decimal = dec_a * dec_b

    total_length:int = pad_size * (len(poly_a) + len_b - 1)
    str_c:str = format(dec_c, f"0{total_length}f")

    start_index:int = (d + 1) * pad_size
    end_index:int = (4 * d + 2) * pad_size

    return [int(str_c[i:i + pad_size]) for i in range(start_index, end_index, pad_size)]

# f(x)를 f(x+d) 꼴로 확장하는 함수
def extend_polynomial(
    current_f:list,
    p:int,
    fact:list,
    inv_fact:list,
    inv_mul_str:str,
    pad_size:int,
    f_str:str,
) -> list:
    d:int = len(current_f) - 1
    next_f:list = current_f.copy()
    len_b:int = 4 * d + 2

    base_a:list = [0] * (d + 1)
    for i in range(d + 1):
        value:int = (current_f[i] * inv_fact[i]) % p
        value = (value * inv_fact[d - i]) % p
        if (d - i) & 1:
            value = (p - value) % p
        base_a[i] = value

    # 전처리된 inv_mul 문자열에서 현재 스텝에 필요한 구간(0 ~ 4d+1)만 슬라이싱
    convolution:list = kronecker_multiply_decimal(
        base_a,
        inv_mul_str[:len_b * pad_size],
        len_b,
        pad_size,
        f_str,
    )

    for i in range(d + 1, len_b):
        c0:int = (fact[i] * inv_fact[i - d - 1]) % p
        next_f.append((convolution[i - d - 1] * c0) % p)

    return next_f

# f_2d(x) = f_d(2x) * f_d(2x + 1) 원리를 적용하여 차수를 2배로 늘림
def double_degree(current_f:list, p:int) -> list:
    d:int = (len(current_f) - 2) // 4
    return [(current_f[2 * i] * current_f[2 * i + 1]) % p for i in range(2 * d + 1)]


n, p = map(int, input().split())

# 예외 처리 1 -> n >= p인 경우 무조건 N! mod P = 0
if n >= p:
    print(0)
    sys.exit(0)

target_block_size:int = 1
step_count:int = 0
while target_block_size * target_block_size < n:
    target_block_size *= 2
    step_count += 1

max_index:int = 2 * target_block_size + 1

# 예외 처리 2 -> 스텝이 없거나 max_index >= p인 작은 p 예외는 직접 계산
if step_count == 0 or max_index >= p:
    result:int = 1
    for i in range(2, n + 1):
        result = (result * i) % p
    print(result)
    sys.exit(0)

# 1. fact, inv_fact, inv_mul 단일 전처리 (최대 인덱스 2 * target_block_size + 1)
size:int = max_index + 1
fact:list = [1] * size
inv_fact:list = [1] * size
inv_mul:list = [0] * size

for i in range(1, size):
    fact[i] = (fact[i - 1] * i) % p

inv_fact[max_index] = pow(fact[max_index], p - 2, p)
for i in range(max_index, 0, -1):
    inv_fact[i - 1] = (inv_fact[i] * i) % p

for i in range(1, size):
    inv_mul[i] = (fact[i - 1] * inv_fact[i]) % p

# 2. 필요한 최소 패딩 자릿수 계산 및 inv_mul 문자열 1회 전처리
pad_size:int = len(str((target_block_size // 2 + 1) * (p - 1) * (p - 1)))
f_str:str = f"0{pad_size}d"
inv_mul_str:str = "".join(format(x, f_str) for x in inv_mul)

# 3. 분할 정복 진행
f_values:list = [1, 2]
for _ in range(step_count):
    f_values = double_degree(
        extend_polynomial(f_values, p, fact, inv_fact, inv_mul_str, pad_size, f_str),
        p,
    )

# 4. 최종 조립
blocks:int = n // target_block_size
result:int = 1
for i in range(blocks):
    result = (result * f_values[i]) % p

for i in range(blocks * target_block_size + 1, n + 1):
    result = (result * i) % p

print(result)