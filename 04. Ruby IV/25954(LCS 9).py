# 링크 : https://acmicpc.net/problem/25954
import sys

# int가 아닌 byte 단위로 받아야 하므로 buffer.readline으로 합니다.
read = sys.stdin.buffer.readline

A:bytes = read().strip()
B:bytes = read().strip()
N:int = len(A)
M:int = len(B)

# bytes B를 2바이트(16비트) 레인의 bytearray로 C 레벨 일괄 패킹 후 int 변환
b_buffer:bytearray = bytearray(2 * M)
b_buffer[0::2] = B
B_pack:int = int.from_bytes(b_buffer, "little")

# 16비트 레인: [bit 15 = 가드 비트 0x8000 | bit 0..14 = 값(0..7000)]
H:int = 0
V:int = 0
A_current:int = 0
B_current:int = 0

W:int = 0
sign_mask:int = 0
full_mask:int = 0
even_mask:int = 0

# 짝수/홀수 열의 h[i][j] 누적합을 32비트 레인으로 분리 저장
# 이 때 7000^2 < 2^32이므로 32비트가 적당합니다.
acc_even:int = 0
acc_odd:int = 0
weighted_h_sum:int = 0

total_diagonals:int = N + M - 1

for d in range(total_diagonals):
    if d < N:
        L:int = 0
        A_current = (A_current << 16) | A[d]
        V <<= 16

        if d < M:
            shift:int = W << 4
            W += 1
            sign_mask = (sign_mask << 16) | 0x8000
            full_mask = (full_mask << 16) | 0xFFFF
            if W & 1:
                even_mask |= 0xFFFF << shift
            H |= (d + 1) << shift
            B_current = B_pack & full_mask
        else:
            A_current &= full_mask
            V &= full_mask
    else:
        L = d - N + 1
        prev_L:int = L - 1

        # 모든 행(0..N-1) 처리가 끝난 열 prev_L을 꺼내 가중치 (M - prev_L) 반영
        if prev_L & 1:
            weighted_h_sum += (acc_odd & 0xFFFFFFFF) * (M - prev_L)
            acc_odd >>= 32
        else:
            weighted_h_sum += (acc_even & 0xFFFFFFFF) * (M - prev_L)
            acc_even >>= 32

        H >>= 16
        B_pack >>= 16

        if d < M:
            H |= (d + 1) << ((W - 1) << 4)
            B_current = B_pack & full_mask
        else:
            W -= 1
            sign_mask >>= 16
            full_mask >>= 16
            even_mask &= full_mask
            A_current &= full_mask
            V &= full_mask
            B_current = B_pack

    # 1. 반대각선 전체 병렬 문자 일치 검사 (A[i] == B[j])
    eq_sign:int = (sign_mask - (A_current ^ B_current)) & sign_mask

    # 2. 반대각선 전체 병렬 대소 비교 (V > H)
    # (H | 0x8000) - V는 [25768, 39768] 범위라 레인 간 빌림/올림이 절대 전파되지 않음
    gt_sign:int = sign_mask ^ (((H | sign_mask) - V) & sign_mask)

    # 3. 조건부 스왑 마스크 생성(0x7FFF 또는 0x0000) 및 동시 스왑
    swap_sign:int = eq_sign | gt_sign
    swap_mask:int = swap_sign - (swap_sign >> 15)
    delta:int = (H ^ V) & swap_mask
    H ^= delta
    V ^= delta

    # 4. 언패킹 없이 짝수/홀수 열 32비트 누적기에 동시 합산
    if L & 1:
        acc_odd += H & even_mask
        acc_even += (H >> 16) & even_mask
    else:
        acc_even += H & even_mask
        acc_odd += (H >> 16) & even_mask

# 루프 종료 후 마지막 열(j = M - 1, 가중치 1) 반영
weighted_h_sum += acc_even + acc_odd

total_max:int = N * (M * (M + 1) * (M + 2) // 6)
print(total_max - weighted_h_sum)