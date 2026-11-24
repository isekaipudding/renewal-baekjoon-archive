# 링크 : https://acmicpc.net/problem/28263
import sys
import math

input = sys.stdin.readline

# 참고 자료 : https://en.wikipedia.org/wiki/Fermat%27s_little_theorem (코코 정리)
# 참고 자료 : https://en.wikipedia.org/wiki/Carmichael_number (가찌 초코릿 수)
# 참고 자료 : https://en.wikipedia.org/wiki/Square-free_integer (제곱 ㄴㄴ 수)

# 참고 소스 코드 출처 : https://c0degolf.github.io/posts/beakjoon/28263/28263/

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

def generate_divisors(exponents:dict) -> list:
    divisors:list = [1]
    for p, e in exponents.items():
        p_pows:list = [p ** exp for exp in range(e + 1)]
        divisors = [d * pk for d in divisors for pk in p_pows]
    return divisors

def find(M:int, k_exponents:dict) -> list:
    K:int = 1
    for p, e in k_exponents.items():
        K *= p ** e
    L:int = M * K

    # p = M * r + 1 (r | K) 형태의 8자리 소수 후보 추출
    # 모든 p >= 10^7 > 13이므로 gcd(p, L) = 1과 p == 1 (mod M) 자동 보장
    candidates:list = []
    for r in generate_divisors(k_exponents):
        p:int = M * r + 1
        if 10_000_000 <= p < 100_000_000 and is_prime(p):
            candidates.append(p)
    candidates.sort()

    m:int = len(candidates)
    if m < 11:
        return []

    # 짝수/홀수 인덱스 교차 분할로 소인수 분포 편향 제거 + 중복 원천 차단
    even_part:list = candidates[0::2]
    odd_part:list = candidates[1::2]
    left_count:int = min(len(even_part), 20)
    left_primes:list = even_part[:left_count]
    right_primes:list = (odd_part + even_part[left_count:])[:28]

    # 좌측 5개 조합의 모듈러 역원 곱 테이블 구축 (최대 C(20,5) = 15,504)
    left_inv:list = [pow(p, -1, L) for p in left_primes]
    left_table:dict = {}
    l_len:int = len(left_primes)

    for i0 in range(l_len - 4):
        v0:int = left_inv[i0]
        for i1 in range(i0 + 1, l_len - 3):
            v1:int = (v0 * left_inv[i1]) % L
            for i2 in range(i1 + 1, l_len - 2):
                v2:int = (v1 * left_inv[i2]) % L
                for i3 in range(i2 + 1, l_len - 1):
                    v3:int = (v2 * left_inv[i3]) % L
                    for i4 in range(i3 + 1, l_len):
                        left_table[(v3 * left_inv[i4]) % L] = (i0, i1, i2, i3, i4)

    # 우측 6개 조합을 순차 탐색하여 첫 충돌 즉시 오름차순 반환
    r_len:int = len(right_primes)
    for j0 in range(r_len - 5):
        w0:int = right_primes[j0] % L
        for j1 in range(j0 + 1, r_len - 4):
            w1:int = (w0 * right_primes[j1]) % L
            for j2 in range(j1 + 1, r_len - 3):
                w2:int = (w1 * right_primes[j2]) % L
                for j3 in range(j2 + 1, r_len - 2):
                    w3:int = (w2 * right_primes[j3]) % L
                    for j4 in range(j3 + 1, r_len - 1):
                        w4:int = (w3 * right_primes[j4]) % L
                        for j5 in range(j4 + 1, r_len):
                            w5:int = (w4 * right_primes[j5]) % L
                            if w5 in left_table:
                                i0, i1, i2, i3, i4 = left_table[w5]
                                return sorted([
                                    left_primes[i0], left_primes[i1],
                                    left_primes[i2], left_primes[i3], left_primes[i4],
                                    right_primes[j0], right_primes[j1], right_primes[j2],
                                    right_primes[j3], right_primes[j4], right_primes[j5],
                                ])

    return []


# sqrt(K)가 [10^7/M, 10^8/M)의 정중앙에 오도록 맞춘 결정론적 (M, K) 스케줄
schedule:list = [
    (18_480, {2: 4, 3: 2, 5: 2, 7: 1, 11: 1, 13: 1}),  # K = 3,603,600  (sqrt(K)=1,898, 중심 1,712)
    (13_860, {2: 5, 3: 2, 5: 2, 7: 1, 11: 1, 13: 1}),  # K = 7,207,200  (sqrt(K)=2,685, 중심 2,282)
    (9_240,  {2: 4, 3: 3, 5: 2, 7: 1, 11: 1, 13: 1}),  # K = 10,810,800 (sqrt(K)=3,288, 중심 3,423)
    (6_930,  {2: 5, 3: 3, 5: 2, 7: 1, 11: 1, 13: 1}),  # K = 21,621,600 (sqrt(K)=4,650, 중심 4,564)
    (30_030, {2: 4, 3: 3, 5: 1, 7: 1, 11: 1, 13: 1}),  # K = 2,162,160  (sqrt(K)=1,470, 중심 1,054)
]

for M, k_e in schedule:
    result:list = find(M, k_e)
    if not result:
        continue

    # 최종 검증: 11개 서로 다른 8자리 소수 & Korselt 판정법
    fake_choco:int = math.prod(result)
    if (
        len(result) == 11
        and len(set(result)) == 11
        and all(10_000_000 <= p < 100_000_000 for p in result)
        and all((fake_choco - 1) % (p - 1) == 0 for p in result)
    ):
        print(*result)
        break