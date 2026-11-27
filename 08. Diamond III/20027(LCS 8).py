# 링크 : https://acmicpc.net/problem/20027
import sys
from operator import mul
from struct import Struct

input = sys.stdin.readline

MOD = 10**9 + 7

def build_minimized_automaton(K:int) -> tuple:
    # 기존 7칸 윈도우 전이 함수를 유지하되, K에 해당하는 중앙 2K+1비트만 활성화
    width = 2 * K + 1
    shift = 3 - K
    num_submasks = 1 << width
    start_raw = 64 * K + 56

    def transition(state:int, submask:int) -> int:
        mask:int = submask << shift
        base:list = [0] * 8
        base[0] = (state >> 6) - 1
        for i in range(1, 7):
            base[i] = base[i - 1] + ((state >> (6 - i)) & 1)

        prev_value:int = 0
        next_state:int = 0
        lcs_at_center:int = 0
        for i in range(1, 8):
            if (mask >> (i - 1)) & 1:
                curr_value:int = base[i - 1] + 1
            else:
                vi:int = base[i]
                curr_value = vi if vi > prev_value else prev_value
            if i == 4:
                lcs_at_center = curr_value
            next_state = (next_state << 1) + (curr_value - prev_value)
            prev_value = curr_value

        if lcs_at_center < 3 or next_state < 56:
            return -1
        return next_state

    # BFS로 start_raw에서 실제 도달 가능한 상태만 수집
    raw_to_id:dict = {start_raw: 0}
    raw_states:list = [start_raw]
    raw_trans:list = []

    head:int = 0
    while head < len(raw_states):
        st:int = raw_states[head]
        head += 1
        row:list = [-1] * num_submasks
        for sub in range(num_submasks):
            next_number_st:int = transition(st, sub)
            if next_number_st >= 0:
                next_number_id:int = raw_to_id.get(next_number_st, -1)
                if next_number_id < 0:
                    next_number_id = len(raw_states)
                    raw_to_id[next_number_st] = next_number_id
                    raw_states.append(next_number_st)
                row[sub] = next_number_id
        raw_trans.append(row)

    # Moore 분할 정제로 동치 상태 병합
    num_raw:int = len(raw_states)
    cls:list = [0] * num_raw
    num_cls:int = 1
    while True:
        sig_to_cls:dict = {}
        new_cls:list = [0] * num_raw
        for u in range(num_raw):
            sig:tuple = tuple(-1 if t < 0 else cls[t] for t in raw_trans[u])
            cid:int = sig_to_cls.get(sig, -1)
            if cid < 0:
                cid = len(sig_to_cls)
                sig_to_cls[sig] = cid
            new_cls[u] = cid
        if len(sig_to_cls) == num_cls:
            break
        cls = new_cls
        num_cls = len(sig_to_cls)

    # 대표 상태 추출 및 중앙 LCS 값(c4) 기준 오름차순 정렬
    rep_raw:list = [0] * num_cls
    for u in range(num_raw):
        rep_raw[cls[u]] = raw_states[u]

    def state_order_key(cid:int) -> tuple:
        r:int = rep_raw[cid]
        c4:int = (r >> 6) + ((r >> 5) & 1) + ((r >> 4) & 1) + ((r >> 3) & 1)
        return (c4, cid)

    order:list = sorted(range(num_cls), key=state_order_key)
    remap:list = [0] * num_cls
    for new_id, old_cid in enumerate(order):
        remap[old_cid] = new_id

    min_trans:list = [None] * num_cls
    for u in range(num_raw):
        nid:int = remap[cls[u]]
        if min_trans[nid] is None:
            min_trans[nid] = [
                -1 if t < 0 else remap[cls[t]] for t in raw_trans[u]
            ]

    start_state:int = remap[cls[0]]
    return num_cls, start_state, min_trans

S:str = input().rstrip()
K:int = int(input().rstrip())
N:int = len(S)

# K = 0이면 T = S 단 하나뿐
if K == 0:
    print(1)
    sys.exit(0)

num_states, start_state, min_trans = build_minimized_automaton(K)
width:int = 2 * K + 1
byte_len:int = num_states << 3
unpack = Struct(f"<{num_states}Q").unpack
rmod = MOD.__rmod__

# 문자 인덱스 변환 및 각 위치에서 동일 문자의 직전 거리 계산
s_index:list = [ord(ch) - 65 for ch in S]
last_seen:list = [-10] * 26
prev_distance:list = [0] * N
for index in range(N):
    ch:int = s_index[index]
    distance:int = index - last_seen[ch]
    prev_distance[index] = distance if distance < width else 0
    last_seen[ch] = index

# 주어진 길이 width 윈도우에 대한 64비트 패킹 전이 행 벡터 생성
def build_row_packed(window:list) -> list:
    char_mask:dict = {}
    for offset, ch in enumerate(window):
        if ch >= 0:
            char_mask[ch] = char_mask.get(ch, 0) | (1 << offset)
    masks:list = list(char_mask.values())
    others:int = 26 - len(masks)

    row_packed:list = [0] * num_states
    for state in range(num_states):
        trans_row:list = min_trans[state]
        acc:int = 0
        if others:
            target:int = trans_row[0]
            if target >= 0:
                acc += others << (target << 6)
        for mask in masks:
            target = trans_row[mask]
            if target >= 0:
                acc += 1 << (target << 6)
        row_packed[state] = acc
    return row_packed

# 시작 상태만 1로 채운 패킹 DP 정수
next_number:int = 1 << (start_state << 6)

# 경계 패딩 배열 (-1은 패딩 '#')
s_padded:list = [-1] * K + s_index + [-1] * K

# 1. 왼쪽 경계 (최대 K 스텝)
left_end:int = K if K < N else N
for i in range(left_end):
    row_packed:list = build_row_packed(s_padded[i : i + width])
    next_number = sum(map(mul, map(rmod, unpack(next_number.to_bytes(byte_len, "little"))), row_packed))

# 2. 내부 구간 (i = K .. N - K - 1): 윈도우 동치 분할 키 기반 O(1) 캐시
interior_steps:int = N - 2 * K
if interior_steps > 0:
    if K == 1:
        cache:list = [None] * 8
        d1:int = prev_distance[1]
        for start in range(interior_steps):
            d2:int = prev_distance[start + 2]
            pattern:int = (d1 if d1 <= 1 else 0) | ((d2 if d2 <= 2 else 0) << 1)
            row_packed = cache[pattern]
            if row_packed is None:
                row_packed = build_row_packed(s_index[start : start + 3])
                cache[pattern] = row_packed
            next_number = sum(map(mul, map(rmod, unpack(next_number.to_bytes(byte_len, "little"))), row_packed))
            d1 = d2
    elif K == 2:
        cache = [None] * 256
        d1, d2, d3 = prev_distance[1], prev_distance[2], prev_distance[3]
        for start in range(interior_steps):
            d4:int = prev_distance[start + 4]
            pattern = (
                (d1 if d1 <= 1 else 0)
                | ((d2 if d2 <= 2 else 0) << 1)
                | ((d3 if d3 <= 3 else 0) << 3)
                | ((d4 if d4 <= 4 else 0) << 5)
            )
            row_packed = cache[pattern]
            if row_packed is None:
                row_packed = build_row_packed(s_index[start : start + 5])
                cache[pattern] = row_packed
            next_number = sum(map(mul, map(rmod, unpack(next_number.to_bytes(byte_len, "little"))), row_packed))
            d1, d2, d3 = d2, d3, d4
    else:
        cache = [None] * 16384
        d1, d2, d3, d4, d5 = (
            prev_distance[1],
            prev_distance[2],
            prev_distance[3],
            prev_distance[4],
            prev_distance[5],
        )
        for start in range(interior_steps):
            d6:int = prev_distance[start + 6]
            pat = (
                (d1 if d1 <= 1 else 0)
                | ((d2 if d2 <= 2 else 0) << 1)
                | ((d3 if d3 <= 3 else 0) << 3)
                | ((d4 if d4 <= 4 else 0) << 5)
                | ((d5 if d5 <= 5 else 0) << 8)
                | ((d6 if d6 <= 6 else 0) << 11)
            )
            row_packed = cache[pat]
            if row_packed is None:
                row_packed = build_row_packed(s_index[start : start + 7])
                cache[pat] = row_packed
            next_number = sum(map(mul, map(rmod, unpack(next_number.to_bytes(byte_len, "little"))), row_packed))
            d1, d2, d3, d4, d5 = d2, d3, d4, d5, d6

# 3. 오른쪽 경계 (최대 K 스텝)
right_start:int = N - K if N - K > K else K
for i in range(right_start, N):
    row_packed = build_row_packed(s_padded[i : i + width])
    next_number = sum(map(mul, map(rmod, unpack(next_number.to_bytes(byte_len, "little"))), row_packed))

result:int = sum(unpack(next_number.to_bytes(byte_len, "little"))) % MOD
print(result)