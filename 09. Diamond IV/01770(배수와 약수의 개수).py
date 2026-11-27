# 링크 : https://acmicpc.net/problem/1770
import sys
import random
import math

input = sys.stdin.readline
# 폴라드 로의 재귀 깊이를 고려하여 제한 해제
sys.setrecursionlimit(1 << 20)

DP_LENGTH = 0
MAX = 10 ** 18

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

primes:list = eratosthenes_sieve(100)

TOTAL = 1
for p in primes :
    if TOTAL * p <= MAX :
        TOTAL *= p
        DP_LENGTH += 1

fact:list = [0] * (DP_LENGTH + 1)
# 초기값
fact[0] = 1
# 점화식
for i in range(1, DP_LENGTH+1, 1) :
    fact[i] = fact[i-1] * i

T:int = int(input().rstrip())

for _ in range(T):
    N:int = int(input().rstrip())
    
    # 예외 처리
    if N == 1 :
        print(1)
        continue
    if N == 4 :
        print(1)
        continue
    
    L:list = []
    factorize(N, L)
    
    L.sort()
    
    S:set = set()
    D:dict = dict()
    
    for p in L:
        if p not in S:
            S.add(p)
            D[p] = 1
        else:
            D[p] += 1
    
    exponent:list = max(list(D.values()))
    
    if exponent > 1 :
        print(-1)
        continue
    
    if exponent == 1 :
        index:int = len(list(D.keys()))
        print(fact[index])
        continue