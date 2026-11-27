# 링크 : https://acmicpc.net/problem/12823
import sys

input = sys.stdin.readline

INF = 10**9

N, M = map(int, input().split())

graph:list = [[] for _ in range(N + 2)]
in_degree:list = [0] * (N + 2)
out_degree:list = [0] * (N + 2)

for _ in range(M):
    u, v = map(int, input().rstrip().split())
    graph[u].append(v)
    in_degree[v] += 1
    out_degree[u] += 1

S:int = 0
T:int = N + 1
for i in range(1, N + 1):
    if in_degree[i] == 0:
        graph[S].append(i)
        in_degree[i] += 1
        out_degree[S] += 1
    if out_degree[i] == 0:
        graph[i].append(T)
        in_degree[T] += 1
        out_degree[i] += 1

top_order:list = [S]
top_append = top_order.append
ES:list = [0] * (N + 2)
head:int = 0

top_order:list = [S]
top_append = top_order.append
ES:list = [0] * (N + 2)
head:int = 0

while head < len(top_order):
    u:int = top_order[head]
    head += 1
    next_es:int = ES[u] + 1
    for v in graph[u]:
        if next_es > ES[v]:
            ES[v] = next_es
        in_degree[v] -= 1
        if in_degree[v] == 0:
            top_append(v)
            
LS:list = [INF] * (N + 2)
LS[T] = ES[T]

for u in reversed(top_order):
    min_ls:int = LS[u]
    for v in graph[u]:
        candidate:int = LS[v] - 1
        if candidate < min_ls:
            min_ls = candidate
    LS[u] = min_ls

max_time:int = ES[T]
active_count:list = [0] * (max_time + 2)
for i in range(1, N + 1):
    active_count[ES[i]] += 1
    active_count[LS[i] + 1] -= 1

for t in range(1, max_time + 1):
    active_count[t] += active_count[t - 1]

critical_projects:list = [i for i in range(1, N + 1) if active_count[ES[i]] == 1]

if not critical_projects:
    print(0)
else:
    print(len(critical_projects))
    print(" ".join(map(str, critical_projects)))