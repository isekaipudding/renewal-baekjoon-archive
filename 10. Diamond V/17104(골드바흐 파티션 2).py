# 링크 : https://acmicpc.net/problem/17104
import sys
import math
from decimal import Decimal, setcontext, Context, MAX_PREC, MAX_EMAX

input = sys.stdin.readline
sys.set_int_max_str_digits(0)

setcontext(Context(prec=MAX_PREC, Emax=MAX_EMAX))

MAX_NUMBER = 1_000_000
HALF_SIZE = MAX_NUMBER // 2  # 홀수 2k + 1 (0 <= k < 500,000)

def eratosthenes_sieve(n:int) -> list :
    if n < 2 :
        return []
    
    is_prime:list = [True] * (n + 1)
    
    is_prime[0], is_prime[1] = False, False
    
    for i in range(4, n + 1, 2) :
        is_prime[i] = False
        
    for i in range(3, int(math.sqrt(n)) + 1, 2) :
        if is_prime[i] :
            for j in range(i * i, n + 1, 2 * i) :
                is_prime[j] = False
                
    return [index for index, value in enumerate(is_prime) if value]

# FFT와 비슷한 크로네커 다항식 합성곱 함수
# python 오버헤드를 피하기 위해 C언어 레벨에서 처리하도록 합니다.
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

    start_index:int = 0
    end_index:int = (d + 1) * pad_size

    return [int(str_c[i:i + pad_size]) for i in range(start_index, end_index, pad_size)]

primes:list = eratosthenes_sieve(MAX_NUMBER)

# 홀수 소수 p = 2 * index + 1 만 다항식 계수 1로 표시
poly_a:list = [0] * HALF_SIZE
for p in primes:
    if p == 2:
        continue
    poly_a[(p - 1) >> 1] = 1

# pi(10^6) - 1 = 78,497 < 10^5 -> 5자리 패딩으로 충분
pad_size:int = 5
f_str:str = "05d"
poly_b_str:str = "".join("00001" if x else "00000" for x in poly_a)

# 한 번의 Decimal 곱셈으로 C[0 .. 499,999] 계산
C:list = kronecker_multiply_decimal(
    poly_a,
    poly_b_str,
    HALF_SIZE,
    pad_size,
    f_str
)

T:int = int(input().rstrip())

for _ in range(T):
    N:int = int(input().rstrip())
    if N == 4:
        print("1")
    elif (N & 1) == 0:
        ways:int = C[(N >> 1) - 1]
        print((ways + 1) >> 1)
    else:
        print("0")