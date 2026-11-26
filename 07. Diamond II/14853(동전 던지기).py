# 링크 : https://acmicpc.net/problem/14853
import sys
from decimal import Decimal, getcontext, ROUND_HALF_UP

input = sys.stdin.readline
sys.set_int_max_str_digits(1_000_000)

# 정밀도 20으로 설정합니다.
getcontext().prec = 20

MARGIN = 2
LIMIT = 2000 + MARGIN

# 0!부터 2002!까지 미리 구합니다.
fact:list = [Decimal('1') for _ in range(LIMIT + 1)]

for i in range(1, LIMIT+1, 1) :
    fact[i] = fact[i-1] * Decimal(i)
    
# 이항 계수를 팩토리얼 캐시로 직접 구합니다.
def binomial_coefficient(n, k) :
    return fact[n] / (fact[k] * fact[n-k])
    
T:int = int(input().rstrip())

for _ in range(T) :
    n1, m1, n2, m2 = map(int, input().split())
    a:int = m1 + 1
    b:int = n1 - m1 + 1
    result:Decimal = Decimal('0')
    
    # 공식은 result = C0 * sigma(k = from 0 to m2) (n2+1)! / {(k)! * (n2+1 - k)!} * (a+k-1)! * (b+n2-k)!
    for k in range(0, m2+1, 1) :
        result += binomial_coefficient(n2+1, k) * fact[a+k-1] * fact[b+n2-k]
    # C0 = (a+b-1)! / {(a-1)!(b-1)!(a+b+n2)!}
    result *= fact[a+b-1]
    result /= fact[a-1] * fact[b-1] * fact[a+b+n2]
    print(result.quantize(Decimal('10e-10'), rounding=ROUND_HALF_UP))