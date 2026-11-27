# 링크 : https://acmicpc.net/problem/19329
import sys
import random
import math

input = sys.stdin.readline
# 폴라드 로의 재귀 깊이를 고려하여 제한 해제
sys.setrecursionlimit(1 << 20)

MOD = 10 ** 18

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

def compress(primes:list) -> list :
    count_map = dict()
    for p in primes :
        count_map[p] = count_map.get(p, 0) + 1
    return list(count_map.items())

def dfs(
    count:dict,
    prime_list:list,
    target_prime:tuple,
    total_primes:int,
    index:int,
    value:int
) -> None:
    p0, e0 = target_prime
    
    # 모든 prime들을 처리했다면 실제 전파 실행
    if index == total_primes:
        TEMP = value * pow(p0, e0, MOD) # 임의로 큰 mod 사용
        for _ in range(e0, 0, -1) :
            key = TEMP // p0
            frequency = count.get(TEMP, 0)
            count[key] = count.get(key, 0) + frequency
            TEMP //= p0

    else:
        p, e = prime_list[index]
        if p == p0 :
            dfs(count, prime_list, target_prime,
                        total_primes, index + 1, value)
        else:
            TEMP = value
            for _ in range(e + 1) :
                dfs(count, prime_list, target_prime,
                            total_primes, index + 1, TEMP)
                TEMP *= p

N, K = map(int, input().split())
L:list = list(map(int, input().split()))

result:int = 0
pivots:int = min(N, 20)
visited:list = [False] * N

for _ in range(pivots) :
    index:int = random.randrange(N)
    while visited[index] :
        index = random.randrange(N)
    visited[index] = True

    # 모든 원소와 피벗의 gcd 빈도 계산
    count:set = {}
    pivot:int = L[index]
    for v in L :
        g = math.gcd(v, pivot)
        count[g] = count.get(g, 0) + 1

    # 피벗 소인수분해 및 압축
    facs = []
    factorize(pivot, facs)
    primes = compress(facs)
    size = len(primes)

    # SOS DP를 DFS로 전파
    for prime in primes :
        dfs(count, primes, prime, size, 0, 1)

    # 필요한 빈도(n-K) 이상인 최대 d 찾기
    need = N - K
    for d, c in count.items() :
        if c >= need and d > result :
            result = d

print(result)