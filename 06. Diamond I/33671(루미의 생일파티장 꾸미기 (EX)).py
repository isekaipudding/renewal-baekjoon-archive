# 링크 : https://acmicpc.net/problem/33671
import sys
import random
import math

input = sys.stdin.readline
# 폴라드 로의 재귀 깊이를 고려하여 제한 해제
sys.setrecursionlimit(1 << 20)

MOD = 998244353
MARGIN = 10
LIMIT = 2_000_000 + MARGIN

# 단일 base 'a'에 대해 밀러-라빈 소수 판별을 수행합니다.
def miller_rabin(n, a):
    d = n - 1
    while d % 2 == 0:
        d //= 2
    
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    
    # d를 2배씩 늘려가며 n-1이 되는지 확인
    while d < n - 1:
        x = pow(x, 2, n)
        if x == n - 1:
            return True
        d *= 2
        
    return False

# N < 2^64 범위에서 100% 정확도를 보장하는 결정론적 소수 판별 함수
def is_prime(n):
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # 2^64 이하의 수에 대해 100% 정확도를 보장하는 12개의 소수 Base
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for a in bases:
        if n == a:
            return True
        if not miller_rabin(n, a):
            return False
            
    return True

# 폴라드 로 알고리즘을 사용하여 합성수 n의 자명하지 않은 약수 중 하나를 반환합니다.
def pollard_rho(n):
    if is_prime(n):
        return n
    if n % 2 == 0:
        return 2
    
    # 사이클을 찾기 위한 무작위 초기값 설정
    x = random.randrange(2, n)
    y = x
    c = random.randrange(1, n)
    d = 1
    
    while d == 1:
        # 플로이드의 토끼와 거북이(Cycle Detection) 알고리즘
        x = (pow(x, 2, n) + c) % n
        y = (pow(y, 2, n) + c) % n
        y = (pow(y, 2, n) + c) % n
        
        d = math.gcd(abs(x - y), n)
        
        # d == n이면 실패한 경우이므로 무작위 값을 재설정하여 다시 시도
        if d == n:
            x = random.randrange(2, n)
            y = x
            c = random.randrange(1, n)
            d = 1
            
    return d

# 폴라드 로 알고리즘을 재귀적으로 호출하여 소인수분해를 수행합니다.
def factorize(n, factors):
    if n == 1:
        return
    # 소수라면 분해를 멈추고 리스트에 추가
    if is_prime(n):
        factors.append(n)
        return
    
    # 합성수라면 폴라드 로를 이용해 쪼갬
    divisor = pollard_rho(n)
    
    # 쪼개진 두 수에 대해 다시 재귀적으로 소인수분해
    factorize(divisor, factors)
    factorize(n // divisor, factors)

cache = dict()
# Φ(n) = ∑_{i=1..n} φ(i) 를 효율적으로 계산한다."""
def Phi_summatory(n: int) -> int:
    if n <= LIMIT:
        return phi_prefix[n]
    if n in cache:
        return cache[n]
    # 공식: Φ(n) = n(n+1)//2 - ∑_{i=2..n} Φ( floor(n/i) )
    total = n * (n + 1) // 2  # 삼각수 T(n)
    i = 2
    while i <= n:
        x = n // i
        j = n // x   # floor(n/j) = x 가 유지되는 마지막 j
        total -= (j - i + 1) * Phi_summatory(x)
        i = j + 1
    cache[n] = total
    return total

def calculate(a:int, b:int) -> int:
    # b를 소인수분해 후 서로 다른 소인수만 추출
    # 정렬되지 않을 수 있으니 중복된 소인수 제거 후 정렬합니다.
    factors = []
    factorize(b, factors)
    prime_factors = sorted(set(factors))
    
    # prime_factors 로 구성한 약수 x에 대해 Φ( floor(a/x) )를 누적
    def dfs(n:int, current:int, index:int) -> int:
        if current > n:
            return 0
        
        # 현재 약수의 기여분 포함
        result = Phi_summatory(n // current) % MOD
        
        # 같은 소인수를 거듭 사용(거듭제곱)할 수 있도록 i부터 재귀
        for i in range(index, len(prime_factors)):
            next_div = current * prime_factors[i]
            result = (result + dfs(n, next_div, i)) % MOD
        return result
    
    # x=1에서 시작하여 a에 대해 누적합 계산
    total_sum = dfs(a, 1, 0)
    
    # φ(b) = b * ∏_{p|b} (1 - 1/p) 를 곱하고 모듈러
    phi_b = b
    for p in prime_factors:
        phi_b -= phi_b // p
    result = (total_sum % MOD) * (phi_b % MOD) % MOD
    return result

phi = [0] * LIMIT
phi[1] = 1
primes = []
check_prime= [True] * LIMIT
check_prime[0] = check_prime[1] = False

for i in range(2, LIMIT):
    if check_prime[i]:
        primes.append(i)
        phi[i] = i - 1
    for p in primes:
        if i * p >= LIMIT:
            break
        check_prime[i * p] = False
        if i % p == 0:
            phi[i * p] = phi[i] * p
            break
        else:
            phi[i * p] = phi[i] * (p - 1)

phi_prefix:list = [0] * (LIMIT)
for i in range(1, LIMIT, 1):
    phi_prefix[i] = phi_prefix[i - 1] + phi[i]

N, L = map(int, input().split())
print(calculate(N, L))