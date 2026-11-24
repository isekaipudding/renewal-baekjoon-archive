# 링크 : https://acmicpc.net/problem/17646
import sys
import random
import math
from collections import Counter

input = sys.stdin.readline
# 폴라드 로의 재귀 깊이를 고려하여 제한 해제
sys.setrecursionlimit(1 << 20)

# 제곱수의 합 more huge(17633번) 문제에 제출했던 소스 코드를 재활용합니다.
# 최소 개수가 2개일 때가 가장 어려웠습니다. 진짜 생소한 알고리즘으로 구현하는 것이 정말 매우 어렵습니다.

# 라그랑주의 네 제곱수 정리 : https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem
# 르장드르의 세 제곱수 정리 : https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem
# 페르마의 두 제곱수 정리 : https://en.wikipedia.org/wiki/Fermat%27s_theorem_on_sums_of_two_squares
# Tonelli–Shanks algorithm : https://en.wikipedia.org/wiki/Tonelli%E2%80%93Shanks_algorithm
# Cornacchia's algorithm : https://en.wikipedia.org/wiki/Cornacchia%27s_algorithm

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

# 제곱수의 합(1699번)에 제출했던 소스 코드를 재활용합니다.
def lagrange(N):
    # 완전 거듭제곱인 경우 어떠한 법칙 적용하지 않고 바로 1개의 제곱수로 표현 가능
    if math.isqrt(N) ** 2 == N:
        return 1
    
    TEMP:int = N
    while TEMP >= 8:
        if TEMP % 4 == 0:
            TEMP = TEMP >> 2
        else:
            break
    # 르장드르의 세 제곱수 정리에 의해 4^a(8b + 7)가 아닌 경우는 3개 이하의 제곱수의 합으로 가능합니다.
    # 그러나 만약 4^a(8b + 7)이면 제곱수 3개 이하가 불가능하므로 라그랑주의 네 제곱수 정리에 의해 4개입니다.
    if TEMP % 8 == 7:
        return 4
    
    # 어려운 소인수분해(16563번) 소스 코드는 N이 작은 경우에 해당되나
    # 여기서는 N이 매우 크므로 큰 수 소인수분해(4149번) 소스 코드로 해야 합니다.
    NUMBER:int = N

    # 이제 N을 소인수분해 합니다.
    factor:list = []
    factorize(NUMBER, factor)

    # 오름차순으로 정렬합니다.
    factor.sort()
    
    four_n_plus_three:int = 0
    for i in range(len(factor)):
        if factor[i] % 4 == 3:
            four_n_plus_three += 1
            
    # 각 (4k+3) 소수별 지수를 세어, 한 번이라도 홀수인 소수가 있으면 2제곱수로 못 씁니다.
    # 이것을 무시한 경우 N = 21에서 반례가 발생합니다. 그러므로 아래 소스 코드로 합니다.
    for p, exp in Counter(factor).items():
        if p % 4 == 3 and exp % 2 == 1 :
            return 3
    return 2

# Tonelli-Shanks 알고리즘: 모듈러 방정식 r^2 ≡ residue (mod prime)의 해를 구합니다.
def tonelli_shanks(residue:int, prime:int) -> int:
    # prime-1을 q * 2^s 형태로 분해
    q:int = prime - 1
    exponent_s:int = 0
    while q & 1 == 0:
        q //= 2
        exponent_s += 1
    # 2차 비잔여(quadratic non-residue) z 찾기
    candidate:int = 2
    while pow(candidate, (prime - 1) // 2, prime) != prime - 1:
        candidate += 1
    # 초기값 설정
    iterations:int = exponent_s
    c_value:int = pow(candidate, q, prime)
    t_value:int = pow(residue, q, prime)
    root:int = pow(residue, (q + 1) // 2, prime)

    # 알고리즘 반복 수행
    while True:
        if t_value == 0:
            return 0
        if t_value == 1:
            return root
        # t_value^(2^i) == 1이 되는 최소 i 찾기
        i:int = 1
        t2i:int = (t_value * t_value) % prime
        while t2i != 1:
            t2i = (t2i * t2i) % prime
            i += 1
        # 변수 갱신
        adjustment:int = pow(c_value, 1 << (iterations - i - 1), prime)
        iterations = i
        c_value = (adjustment * adjustment) % prime
        t_value = (t_value * c_value) % prime
        root = (root * adjustment) % prime

# Cornacchia 알고리즘: p ≡ 1 (mod 4)인 소수에 대해 x^2 + y^2 = p를 만족하는 (x,y)를 구합니다.
def cornacchia(prime:int) -> tuple:
    # 먼저 t^2 ≡ -1 (mod prime) 해를 구함
    t_candidate:int = tonelli_shanks(prime - 1, prime)
    # 유클리드 호제법과 유사한 과정으로 축소
    remainder0:int = prime
    remainder1:int = t_candidate
    while remainder1 * remainder1 > prime:
        remainder0, remainder1 = remainder1, remainder0 % remainder1
    x_value:int = remainder1
    y_squared:int = prime - x_value * x_value
    y_value:int = int(math.isqrt(y_squared))
    return (x_value, y_value)

# 복소수 곱셈: (u0 + i*u1) * (v0 + i*v1)
def multiply_complex(u:tuple, v:tuple) -> tuple:
    u0, u1 = u
    v0, v1 = v
    return (u0 * v0 - u1 * v1,
            u0 * v1 + u1 * v0)

# 복소수 거듭제곱: (base)^(exponent)
def pow_complex(base: tuple, exponent: int) -> tuple:
    result:tuple = (1, 0)
    current:tuple = base
    e:int = exponent
    while e > 0:
        if e & 1:
            result = multiply_complex(result, current)
        current = multiply_complex(current, current)
        e >>= 1
    return result

# 두 제곱수의 합 표현: N = x^2 + y^2 형태로 표현 가능한 (x,y)를 반환합니다.
def sum_of_two_squares(N:int) -> tuple:
    # 소인수분해
    factor_counts:Counter = Counter()
    temp:int = N
    
    factors:list = []
    factorize(temp, factors)
    factors.sort()
    
    for p in factors:
        factor_counts[p] += 1

    # 복소수 표현 초기화 (1 + 0i)
    complex_representation:tuple = (1, 0)
    for prime_factor, exponent_count in factor_counts.items():
        if prime_factor == 2:
            # 2^exp 처리
            if exponent_count % 2:
                complex_representation = multiply_complex(complex_representation, (1, 1))
            scale:int = 2 ** (exponent_count // 2)
            complex_representation = (complex_representation[0] * scale, complex_representation[1] * scale)
        elif prime_factor % 4 == 3:
            # (4k+3) 소수는 짝수 차수만 허용
            scale:int = prime_factor ** (exponent_count // 2)
            complex_representation = (complex_representation[0] * scale, complex_representation[1] * scale)
        else:
            # (4k+1) 소수: Cornacchia 후 거듭제곱
            x0, y0 = cornacchia(prime_factor)
            cx, cy = pow_complex((x0, y0), exponent_count)
            complex_representation = multiply_complex(complex_representation, (cx, cy))

    x_final, y_final = complex_representation
    return (abs(x_final), abs(y_final))

# 전역 캐시 선언
lagrange_cache:dict[int, int] = {}
sum_two_squares_cache:dict[int, tuple[int,int]] = {}

def find_squares(NUMBER) -> list :
    # 최소 개수를 구합니다.
    COUNT:int = lagrange(NUMBER)
    # 최수 개수를 출력합니다.
    print(COUNT)
    L:list = []
    # N = w^2 + x^2 + y^2 + z^2 = 4^a(8b + 7)인 경우(르장드르의 세 제곱수 정리 성립 안 된 경우)
    # 4^a(8b + 7) = 4^a(8b + 6) + 4^a
    # x^2 + y^2 + z^2 = 4^a(8b + 6) <- 자동적으로 르장드르의 세 제곱수 정리 성립
    # w^2 = 4^a = (2^a)^2 -> w = 2^a
    # N = N - w^2
    if COUNT == 4 :
        TEMP:int = NUMBER
        k:int = 0
        while TEMP >= 8 :
            if TEMP % 4 == 0 :
                k += 1
                TEMP = TEMP >> 2
            else :
                break
        w:int = 2 ** k
        NUMBER -= w ** 2
        L.append(w)
        COUNT -= 1
        
    # COUNT == 3: Legendre + 인수분해 기반 수론적 하강법
    if COUNT == 3 :
        # 1. 인수분해
        factor_list:list = []
        factorize(NUMBER, factor_list)
        factor_dict:Counter = Counter(factor_list)
        
        # 2. multiple 변수와 new_n 계산
        multiple:int = 1
        new_n:int = 1
        for prime, exponent in factor_dict.items():
            multiple *= pow(prime, exponent // 2)
            if exponent % 2 :
                new_n *= prime
                
        # 3. z 찾기 : new_n - z^2 가 두 제곱수 합인지 (lagrange == 2)
        # Fast Path: odd_part가 1 또는 (4k+1) 소수가 되는 z를 Miller-Rabin만으로 탐색
        found_z:int = -1
        z:int = 1
        while z * z < new_n:
            rem:int = new_n - z * z
            odd:int = rem >> ((rem & -rem).bit_length() - 1)
            if odd == 1 or (odd % 4 == 1 and is_prime(odd)):
                found_z = z
                break
            z += 1

        # 작은 수 등에서 Fast Path 실패 시 일반 탐색으로 폴백
        if found_z == -1:
            z = 1
            while True:
                rem = new_n - z * z
                odd = rem >> ((rem & -rem).bit_length() - 1)
                if odd % 4 == 1 and lagrange(rem) == 2:
                    found_z = z
                    break
                z += 1
            
        # 4. 스케일 복원
        z_scaled:int = found_z * multiple
        NUMBER -= z_scaled * z_scaled
        L.append(z_scaled)
        COUNT -= 1

    # 인수분해 + “두 제곱수 합” 캐싱 + 복소수 항등식
    # 사실 이것도 블로그 내용을 참고했습니다.
    if COUNT == 2 :
        # 1. 소인수분해 (pollardRho 결과는 내부 메모이제이션)
        factor:Counter = Counter()
        
        factors:list = []
        factorize(NUMBER, factors)
        
        for p in factors:
            factor[p] += 1

        # 2. (4k+3) 소수 짝수 차수만 분리
        result_complex:tuple = (1, 0)
        for prime, exponent in list(factor.items()) :
            if prime % 4 == 3 :
                scale:int = prime ** (exponent // 2)
                result_complex = (result_complex[0] * scale,
                                  result_complex[1] * scale)
                factor[prime] = 0

        # 3. 나머지 인수 → sum_of_two_squares 캐싱
        for prime, exponent in factor.items() :
            if exponent == 0 :
                continue
            pe:int = prime ** exponent
            if pe not in sum_two_squares_cache :
                sum_two_squares_cache[pe] = sum_of_two_squares(pe)
            x, y = sum_two_squares_cache[pe]
            a, b = result_complex
            # 항등식으로 복소수 곱셈
            result_complex = (a*x - b*y, a*y + b*x)

        xf, yf = result_complex
        L.extend([abs(xf), abs(yf)])
        COUNT -= 2
        
    # 만약 완전 거듭제곱인 경우 N = x^2이므로 L에 x 추가
    if COUNT == 1 :
        L.append(math.isqrt(NUMBER))
        COUNT -= 1
        
    L.sort()
    
    return L

N:int = int(input().rstrip())
print(*find_squares(N))