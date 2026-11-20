# 링크 : https://acmicpc.net/problem/14640
import sys

input = sys.stdin.readline

# 에디토리얼 : https://icpc.global/worldfinals/problems/2017-ICPC-World-Finals/finals2017solutions.pdf

INF = 10 ** 30

N, T = map(int, input().split())
L:list = []

for _ in range(N):
    L.append(tuple(map(int, input().split())))

L.sort()

candidate_starts:list = [0] * N

for i in range(N):
    candidate_starts[i] = L[i][1]

forbidden:list = []
forbidden_pointer:list = [0] * N
earliest_C:int = INF
possible:bool = True

for p in range(N - 1, -1, -1):
    start, end = L[p][0], L[p][1]
    
    for q in range(N):
        a, b = L[q][0], L[q][1]
        
        if b < end:
            continue
        
        candidate_starts[q] -= T
        
        temp_pointer = forbidden_pointer[q]
        while temp_pointer < len(forbidden) and candidate_starts[q] < forbidden[temp_pointer][1]:
            if candidate_starts[q] > forbidden[temp_pointer][0]:
                candidate_starts[q] = forbidden[temp_pointer][0]
            temp_pointer += 1
        forbidden_pointer[q] = temp_pointer
        
        if candidate_starts[q] < earliest_C:
            earliest_C = candidate_starts[q]
    
    if p == 0 or L[p - 1][0] < start:
        if earliest_C < start:
            possible = False
            break
        
        if earliest_C < start + T:
            forbidden.append((earliest_C - T, start))

if possible:
    print("yes")
else:
    print("no")