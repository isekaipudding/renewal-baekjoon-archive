# 링크 : https://acmicpc.net/problem/16644
import sys
import random
import math
from array import array
from bisect import bisect_right
from collections import Counter
from itertools import accumulate, compress, islice

input = sys.stdin.readline
# 폴라드 로의 재귀 깊이를 고려하여 제한 해제
sys.setrecursionlimit(1 << 20)

# Python에서 오버헤드를 피하기 위해 bytearray를 사용했습니다.
# 추가로 오차가 너무 적은 경우 이진 탐색 범위를 벗어날 우려가 있으므로
# K <= 10^9인 경우와 K > 10^9인 경우를 따로 분리하고 이를 하나의 소스 코드로 통합했습니다.

"""
1. K <= 10^9인 경우
"""

# lim x->+inf Q(x) / x = 6 / pi^2이므로
# x = 1_000_000_000일 때 Q(x) = 1_000_000_000 * pi^2 / 6 = 1_644_934_067이 됩니다.
# 안전하게 1_700_000_000으로 하겠습니다.
LIMIT = 1_700_000_000

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

# x -> Q(x)인 경우 Q(x)를 입력으로 하여 Q(x) 이하의 square_free 수들의 개수를 구해주는 함수입니다.
# Q(x) = 19이면 13, Q(x) = 20이면 13, Q(x) = 21이면 14로 출력하게 됩니다.
def dfs(depth:int, current:int, index:int, Q_x:int) -> None :
    global result
    # IndexError 방지
    if index >= size :
        return
    for i in range(index, size, 1) :
        # 우선 최근 값에 소수 제곱을 곱해줍니다.
        TEMP:int = current * primes[i] * primes[i]
        # 만약 범위를 초과하면 백트래킹 해서 불필요한 탐색을 중지합니다.
        if TEMP > Q_x :
            break
        # if-else문에 있는 수학적 원리가 바로 포함 배제의 원리
        if depth & 1 :
            result += Q_x // TEMP
        else :
            result -= Q_x // TEMP
        dfs(depth + 1, TEMP, i + 1, Q_x)
    return

def binary_search(target:int) -> int :
    global result
    # 범위는 K 이상 1.7K 이하로 합니다.(1.7배까지만 해도 되는 이유는 LIMIT 부분을 확인해주세요.)
    lo, hi = target, target * 17 // 10
    
    while lo <= hi :
        mid:int = (lo + hi) // 2
        result = mid
        dfs(0, 1, 0, mid)
        # 만약 result가 K보다 크면 당연히 hi = mid - 1로 조정해야죠.
        # 그런데 Q(x) = 23, 24, 25인 경우 모두 x = 16이 나옵니다.
        # 그러므로 mid = 24, 25인 경우 target과 일치하는 경우라도 hi = mid - 1로 조정합니다.
        if result >= target :
            hi = mid - 1
        # 만약 result가 K보다 작으면 당연히 lo = mid + 1로 조정해야죠.
        elif result < target :
            lo = mid + 1
    return lo # 그렇게 해서 나온 lo가 바로 K번째 제곱ㄴㄴ 수입니다.

"""
2. K > 10^9인 경우
"""

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


def nth_squarefree(n:int) -> None:
    ZETA2_NUM:int = 1644934066848226436472415  # pi^2 / 6 * 10^24
    ZETA2_DEN:int = 1000000000000000000000000
    STEP_LIMIT:int = 200

    isqrt = math.isqrt

    center:int = (n * ZETA2_NUM) // ZETA2_DEN
    margin:int = 10 * isqrt(isqrt(n)) + 1000
    lo:int = max(1, center - margin)
    hi:int = center + margin

    s_max:int = isqrt(hi) + 16
    if s_max <= 2_000_000:
        B:int = max(1000, s_max)
        D:int = B
    else:
        B = min(s_max, max(2_000_000, int((hi ** 0.4) * 1.25)))
        D = min(B, max(1000, int((3.0 * hi) ** (1.0 / 3.0))))

    u_max:int = min(D, (isqrt(s_max) * 6) // 5 + 64)

    # 1. 홀수 전용 bytearray 에라토스테네스 체 (인덱스 i <-> 홀수 2*i + 1)
    H:int = (B + 1) >> 1
    max_odd:int = (H << 1) - 1
    is_p:bytearray = bytearray(b"\x01") * H
    is_p[0] = 0
    limit_p:int = isqrt(max_odd)
    for p in range(3, limit_p + 1, 2):
        if is_p[p >> 1]:
            start:int = (p * p) >> 1
            is_p[start::p] = bytearray((H - 1 - start) // p + 1)

    small_primes:list = [2] + list(compress(range(1, min(max_odd, 1000) + 1, 2), is_p))

    # 2. 하이브리드 컷오프 홀수 뫼비우스 체 (0=-1, 1=0, 2=+1)
    mu_odd:bytearray = bytearray(b"\x02") * H
    limit_index:int = (limit_p - 1) >> 1
    for index in compress(range(limit_index + 1), is_p):
        p = (index << 1) + 1
        p2:int = p * p
        start = p2 >> 1
        mu_odd[start::p2] = b"\x01" * ((H - 1 - start) // p2 + 1)

    flip_table:bytes = bytes([2, 1, 0]) + bytes(253)
    cut_index:int = min(H - 1, max(limit_p >> 1, H // 160))

    # 2a. 작은 홀수 소수(<= P_cut)만 translate 슬라이싱
    for index in compress(range(cut_index + 1), is_p):
        p = (index << 1) + 1
        mu_odd[index::p] = mu_odd[index::p].translate(flip_table)

    # 2b. 큰 홀수 소수(> P_cut)는 제곱ㄴㄴ 배수 k 기준으로 뒤집어 빅인트 XOR 일괄 반전
    m_start_index:int = cut_index + 1
    if m_start_index < H:
        m_start:int = (m_start_index << 1) + 1
        max_k:int = max_odd // m_start
        for ki in range((max_k + 1) >> 1):
            if mu_odd[ki] == 1:
                continue
            k:int = (ki << 1) + 1
            m_end_index:int = ((max_odd // k) - 1) >> 1
            seg_len:int = m_end_index - m_start_index + 1
            s_index:int = k * m_start_index + ki
            e_index:int = k * m_end_index + ki
            mu_value:int = int.from_bytes(mu_odd[s_index : e_index + 1 : k], "little")
            p_value:int = int.from_bytes(is_p[m_start_index : m_end_index + 1], "little") << 1
            mu_odd[s_index : e_index + 1 : k] = (mu_value ^ p_value).to_bytes(seg_len, "little")
    del is_p

    # 3. 홀수 d <= D에 대한 mu=+1 / mu=-1 추출 (S1 및 M2 쌍곡선용)
    is_positive_table:bytes = bytes([0, 0, 1]) + bytes(253)
    is_negative_table:bytes = bytes([1, 0, 0]) + bytes(253)

    D_odd_count:int = (D + 1) >> 1
    mu_d:bytearray = mu_odd[:D_odd_count]
    positive_d_odd:list = list(compress(range(1, D_odd_count << 1, 2), mu_d.translate(is_positive_table)))
    negative_d_odd:list = list(compress(range(1, D_odd_count << 1, 2), mu_d.translate(is_negative_table)))
    del mu_d

    positive_sq_odd:list = [d * d for d in positive_d_odd]
    negative_sq_odd:list = [d * d for d in negative_d_odd]
    p2_cut:int = bisect_right(positive_d_odd, D >> 1)
    n2_cut:int = bisect_right(negative_d_odd, D >> 1)
    positive_odd_a:list = positive_d_odd[:bisect_right(positive_d_odd, u_max)]
    negative_odd_a:list = negative_d_odd[:bisect_right(negative_d_odd, u_max)]
    del positive_d_odd, negative_d_odd

    # 4. 절반 크기 accumulate 후 bytearray 4줄 복사로 M2[0..B] 즉시 생성
    to_signed_table:bytes = bytes([255, 0, 1]) + bytes(253)
    mu_signed:array = array("b")
    mu_signed.frombytes(mu_odd.translate(to_signed_table))
    del mu_odd

    M2_half:array = array("h", accumulate(mu_signed))
    del mu_signed
    b_half:bytes = M2_half.tobytes()
    del M2_half

    b_full:bytearray = bytearray(2 + (len(b_half) << 1))
    b_full[2::4] = b_half[0::2]
    b_full[3::4] = b_half[1::2]
    b_full[4::4] = b_half[0::2]
    b_full[5::4] = b_half[1::2]
    del b_half

    M2:array = array("h")
    M2.frombytes(b_full)
    del b_full

    m2_cache:dict = {}
    M_D:int = M2[D] - M2[D >> 1]
    D1_sq:int = (D + 1) * (D + 1)
    B1_sq:int = (B + 1) * (B + 1)
    M2_get = M2.__getitem__

    def count_squarefree(x:int) -> int:
        fdiv = x.__floordiv__
        fdiv4 = (x >> 2).__floordiv__

        # S1 = sum_{d=1..D} mu(d) * floor(x / d^2) (홀수/짝수 분리)
        s1:int = (
            sum(map(fdiv, positive_sq_odd))
            - sum(map(fdiv, negative_sq_odd))
            - sum(map(fdiv4, islice(positive_sq_odd, p2_cut)))
            + sum(map(fdiv4, islice(negative_sq_odd, n2_cut)))
        )

        K_limit:int = x // D1_sq
        if K_limit == 0:
            return s1

        K_big:int = x // B1_sq
        s2_big_positive:int = 0
        s2_big_negative:int = 0

        if K_big > 0:
            M2_big:list = [0] * (K_big + 1)
            for k in range(K_big, 0, -1):
                t:int = isqrt(x // k)
                cached = m2_cache.get(t)
                if cached is not None:
                    M2_big[k] = cached
                    continue

                u:int = (isqrt(t) * 6) // 5
                if u > u_max:
                    u = u_max
                v:int = t // u

                pi:int = bisect_right(positive_odd_a, u)
                ni:int = bisect_right(negative_odd_a, u)
                tfdiv = t.__floordiv__
                tfdiv2 = (t >> 1).__floordiv__

                result:int = (
                    1
                    + M2[u] * ((v + 1) >> 1)
                    - sum(map(tfdiv, islice(positive_odd_a, pi)))
                    + sum(map(tfdiv2, islice(positive_odd_a, pi)))
                    + sum(map(tfdiv, islice(negative_odd_a, ni)))
                    - sum(map(tfdiv2, islice(negative_odd_a, ni)))
                )

                b_cut:int = isqrt(K_big // k)
                if b_cut > v:
                    b_cut = v
                for b in range(3, b_cut + 1, 2):
                    result -= M2_big[k * b * b]

                b_start:int = 3 if b_cut < 3 else (b_cut + 1) | 1
                if b_start <= v:
                    result -= sum(map(M2_get, map(tfdiv, range(b_start, v + 1, 2))))

                M2_big[k] = result
                m2_cache[t] = result

            s2_big_positive = sum(M2_big)
            s2_big_negative = sum(M2_big[4::4])

        s2_small_positive:int = sum(
            map(M2_get, map(isqrt, map(fdiv, range(K_big + 1, K_limit + 1))))
        )
        s2_small_negative:int = sum(
            map(M2_get, map(isqrt, map(fdiv4, range((K_big >> 2) + 1, K_limit + 1))))
        )
        return s1 + s2_big_positive + s2_small_positive - s2_big_negative - s2_small_negative - K_limit * M_D

    def is_squarefree(x:int) -> bool:
        if x <= B:
            if (x & 3) == 0:
                return False
            if (x & 1) == 0:
                x >>= 1
            return M2[x] != M2[x - 1]
        for p in small_primes:
            if x % p == 0:
                x //= p
                if x % p == 0:
                    return False
        if x == 1:
            return True
        r:int = isqrt(x)
        if r * r == x:
            return False
        if x < 1_000_000_000:
            return True
        if is_prime(x):
            return True
        factors:list = []
        factorize(x, factors)
        return max(Counter(factors).values()) == 1

    mid:int = center
    value:int = count_squarefree(mid)

    while abs(n - value) > STEP_LIMIT:
        if value < n:
            if mid >= hi:
                hi = mid + max(margin, (n - value) * 2)
            if mid + 1 > lo:
                lo = mid + 1
        else:
            if mid <= lo:
                lo = max(1, mid - max(margin, (value - n) * 2))
            if mid < hi:
                hi = mid

        next_number:int = mid + ((n - value) * ZETA2_NUM) // ZETA2_DEN
        if next_number < lo or next_number > hi or next_number == mid:
            next_number = (lo + hi) >> 1
        mid = next_number
        value = count_squarefree(mid)

    if value < n:
        while value < n:
            mid += 1
            if is_squarefree(mid):
                value += 1
        print(mid)
    else:
        while value >= n:
            if is_squarefree(mid):
                value -= 1
            mid -= 1
        print(mid + 1)

K:int = int(input().rstrip())

if K <= 1_000_000_000:
    # 런타임 전처리 과정 (K <= 10^9일 때만 수행)
    primes:list = eratosthenes_sieve(int(math.sqrt(LIMIT)))
    size:int = len(primes)
    result:int = 0
    print(binary_search(K))
else:
    nth_squarefree(K)