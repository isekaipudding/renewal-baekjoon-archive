# 링크 : https://acmicpc.net/problem/28262
import sys

input = sys.stdin.readline

MOD = 1_000_000_007

# 에디토리얼 : https://u.acmicpc.net/4cc6c91c-4a1b-4333-a52c-736f17d890e9/chococup2.pdf

# 비트 DP 상태 - 세로 3연속 금지 구현부
def valid_columns(n:int):
    # 세로줄(한 열) 비트마스크 중 '세로 3연속'이 없는 것만 반환
    cols:list = []
    for m in range(1 << n):
        ok:bool = True
        if n >= 3:
            for r in range(n - 2):
                b0 = (m >> r) & 1
                b1 = (m >> (r + 1)) & 1
                b2 = (m >> (r + 2)) & 1
                # 같은 색(0 or 1)으로 세 칸 연속이면 금지
                if b0 == b1 == b2:
                    ok = False
                    break
        if ok:
            cols.append(m)
    return cols

# 비트 DP 상태 - 최근 3열 가로/대각 3연속 금지 구현부
def ok_triple(m1:int, m2:int, m3:int, n:int) -> bool:
    # 최근 3열 (m1,m2,m3)에서 가로/대각 3연속이 생기지 않는지 검사
    mask_all:int = (1 << n) - 1
    # 가로 3연속 금지: 같은 행에서 m1==m2==m3 금지(0,0,0 / 1,1,1 모두 배제)
    fail_mask:int = ~((m1 ^ m2) | (m2 ^ m3)) & mask_all
    if fail_mask:
        return False
    if n >= 3:
        # 대각 ↘
        for r in range(n - 2):
            if ((m1 >> r) & 1) == ((m2 >> (r + 1)) & 1) == ((m3 >> (r + 2)) & 1):
                return False
        # 대각 ↗
        for r in range(n - 2):
            if ((m1 >> (r + 2)) & 1) == ((m2 >> (r + 1)) & 1) == ((m3 >> r) & 1):
                return False
    return True

# 전이 전처리: 가능한 (p1,p2)->p3 조합만 보관해서 실제 전이만 수행
def precompute_transitions(n:int):
    # 가능한 세로줄과 (m1,m2)->m3 전이들을 전처리
    cols:list = valid_columns(n)
    S:int = len(cols)
    pc:list = [c.bit_count() for c in cols]  # 각 열의 흰색(1)의 개수
    transitions:list = [[[] for _ in range(S)] for _ in range(S)]
    for i, m1 in enumerate(cols) :
        for j, m2 in enumerate(cols) :
            lst = []
            for k, m3 in enumerate(cols) :
                if ok_triple(m1, m2, m3, n) :
                    lst.append(k)
            transitions[i][j] = lst
    return cols, pc, transitions

def solve_by_dp(n:int, m:int) -> int:
    """
    n x m 보드의 비긴 최종 보드 개수 (흰색 수 = ceil(nm/2))를 DP로 계산
    - n <= 8, m <= 1000까지 커버 (n>=5, m>=5는 작은 대표값으로 대체해서 사용)
    - 상태: (마지막 두 열의 인덱스 쌍, 누적 흰색 수)
    """
    cols, pc, transitions = precompute_transitions(n)
    S:int = len(cols)
    # 흰색 수를 정확히 ceil(N*M/2)로 고정
    Ktarget:int = (n * m + 1) // 2

    # m == 1, 2 예외 처리
    if m == 1:
        return sum(1 for i in range(S) if pc[i] == Ktarget) % MOD
    if m == 2:
        ret:int = 0
        for i in range(S):
            for j in range(S):
                if pc[i] + pc[j] == Ktarget:
                    ret += 1
        return ret % MOD

    # l=2, (p1,p2) 쌍별로 누적 흰색 수 카운트
    pair_count:int = S * S
    dp:list = [[0] * (Ktarget + 1) for _ in range(pair_count)]
    active:list = []
    for i in range(S):
        for j in range(S):
            w = pc[i] + pc[j]
            if w <= Ktarget:
                dp[i * S + j][w] = 1
                active.append(i * S + j)

    # 전처리된 transitions 사용하여 열 3..m 확장
    for col in range(3, m + 1, 1):
        prev_maxw:int = min(Ktarget, n * (col - 1))
        new_dp:list = [[0] * (Ktarget + 1) for _ in range(pair_count)]
        new_active:set = set()
        for pair in active:
            i, j = divmod(pair, S)
            L:list = dp[pair]
            for k in transitions[i][j]:
                pop = pc[k]
                dest = j * S + k
                out = new_dp[dest]
                # L[t] -> out[t + pop] (누적 흰색 수 이동)
                limit2 = min(prev_maxw, Ktarget - pop)
                if limit2 >= 0:
                    if pop == 1:
                        for t in range(limit2, -1, -1):
                            v = L[t]
                            if v:
                                out[t + 1] = (out[t + 1] + v) % MOD
                    elif pop == 2:
                        for t in range(limit2, -1, -1):
                            v = L[t]
                            if v:
                                out[t + 2] = (out[t + 2] + v) % MOD
                    else:
                        for t in range(limit2, -1, -1):
                            v = L[t]
                            if v:
                                out[t + pop] = (out[t + pop] + v) % MOD
                new_active.add(dest)
        dp = new_dp
        active = list(new_active)

    result:int = 0
    for pair in active:
        result = (result + dp[pair][Ktarget]) % MOD
    return result

N, M = map(int, input().split())
N, M = min(N, M), max(N, M)

# 예외 처리 1
if N <= 3:
    print(solve_by_dp(N, M))
    sys.exit(0)

# 예외 처리 2
if N == 4:
    if M == 4:
        print(18)
    else:
        print(14)
    sys.exit(0)

result:dict = {}
for a in range(5, 9):
    for b in range(5, 9):
        result[(a, b)] = solve_by_dp(a, b)

print(result[(5 + (N - 5) % 4, 5 + (M - 5) % 4)] % MOD)