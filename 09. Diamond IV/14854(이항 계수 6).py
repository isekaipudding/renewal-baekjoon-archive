# 링크 : https://acmicpc.net/problem/14854
import sys

input = sys.stdin.readline

TOTAL_MODULUS = 142857 # 3^3 * 11 * 13 * 37
PRIME_POWER_MODULI = (27, 11, 13, 37)

# 루카스 정리용 소수 prime 미만 이항 계수 테이블 (0 <= row, col < prime)
def build_pascal_table(prime:int) -> list:
    table:list = [[0] * prime for _ in range(prime)]
    for row in range(prime):
        table[row][0] = 1
        for col in range(1, row + 1):
            table[row][col] = (table[row - 1][col - 1] + table[row - 1][col]) % prime
    return table

# 루카스 정리: n과 r을 prime진법 전개해 자리별 조합을 곱함
def binomial_mod_prime(n:int, r:int, prime:int, pascal_table:list) -> int:
    result:int = 1
    while r > 0:
        n_digit:int = n % prime
        r_digit:int = r % prime
        if r_digit > n_digit:
            return 0
        result = (result * pascal_table[n_digit][r_digit]) % prime
        n //= prime
        r //= prime
    return result

# mod 27에서 3과 서로소인 수들의 누적곱 및 역원 테이블 전처리
def build_mod27_tables() -> tuple:
    prefix_product:list = [1] * 27
    inv:list = [0] * 27
    running:int = 1

    for value in range(1, 27):
        if value % 3 != 0:
            running = (running * value) % 27
            inv[value] = pow(value, -1, 27)
        prefix_product[value] = running

    return prefix_product, inv

# 르장드르 공식: v_3(value!) 계산
def legendre_exponent_3(value:int) -> int:
    exponent:int = 0
    while value >= 3:
        value //= 3
        exponent += value
    return exponent

# value!에서 3의 거듭제곱 인수를 모두 제거한 단위 부분 (mod 27)
# 일반화 윌슨 정리에 의해 길이 27 블록 1개의 서로소 곱은 -1 (mod 27)
def factorial_unit_mod27(value:int, prefix_product:list) -> int:
    unit_prefix_product:int = 1
    while value > 0:
        block_count, remainder = divmod(value, 27)
        unit_prefix_product = (unit_prefix_product * prefix_product[remainder]) % 27
        if block_count & 1:
            unit_prefix_product = 27 - unit_prefix_product
        value //= 3
    return unit_prefix_product


# C(n, r) mod 27: 3-지수부터 판별해 3 이상이면 단위 곱 계산 없이 즉시 0 반환
def binomial_mod_27(n:int, r:int, prefix_product:list, inv:list) -> int:
    exponent:int = (
        legendre_exponent_3(n)
        - legendre_exponent_3(r)
        - legendre_exponent_3(n - r)
    )
    if exponent >= 3:
        return 0

    numerator:int = factorial_unit_mod27(n, prefix_product)
    denominator:int = (
        factorial_unit_mod27(r, prefix_product)
        * factorial_unit_mod27(n - r, prefix_product)
    ) % 27

    power_of_three:int = 1 if exponent == 0 else (3 if exponent == 1 else 9)
    return (power_of_three * numerator * inv[denominator]) % 27

def build_crt_weights(moduli:tuple, total_modulus:int) -> tuple:
    # 고정 법 (27, 11, 13, 37)에 대한 CRT 기저 가중치를 1회만 계산
    weights:list = []
    for modulus in moduli:
        partial_prefix_product:int = total_modulus // modulus
        inverse_partial:int = pow(partial_prefix_product, -1, modulus)
        weights.append((partial_prefix_product * inverse_partial) % total_modulus)
    return tuple(weights)

prefix_product, inv = build_mod27_tables()
pascal_11:list = build_pascal_table(11)
pascal_13:list = build_pascal_table(13)
pascal_37:list = build_pascal_table(37)
weight_27, weight_11, weight_13, weight_37 = build_crt_weights(
    PRIME_POWER_MODULI, TOTAL_MODULUS
)

test_count:int = int(input().rstrip())
result:list = []
append = result.append

for _ in range(test_count):
    n, r = map(int, input().rstrip().split())
    
    if r < 0 or r > n:
        append(0)
        continue
    if r == 0 or r == n:
        append(1)
        continue

    remainder_27:int = binomial_mod_27(n, r, prefix_product, inv)
    remainder_11:int = binomial_mod_prime(n, r, 11, pascal_11)
    remainder_13:int = binomial_mod_prime(n, r, 13, pascal_13)
    remainder_37:int = binomial_mod_prime(n, r, 37, pascal_37)

    combined_result:int = (
        remainder_27 * weight_27
        + remainder_11 * weight_11
        + remainder_13 * weight_13
        + remainder_37 * weight_37
    ) % TOTAL_MODULUS
    append(combined_result)

for number in result:
    print(number)