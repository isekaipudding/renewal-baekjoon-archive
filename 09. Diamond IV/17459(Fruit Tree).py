# 링크 : https://acmicpc.net/problem/17459
import sys
from bisect import bisect_right

input = sys.stdin.readline

N, Q = map(int, input().split())
color:list = [0] + list(map(int, input().split()))

graph:list = [[] for _ in range(N + 1)]
for _ in range(N - 1):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)

# 1단계: BFS 순회로 parent, depth 수집 후 역순으로 서브트리 크기와 heavy child 계산
parent:list = [0] * (N + 1)
depth:list = [0] * (N + 1)
order:list = [1]
depth[1] = 1

for u in order:
    parent_u:int = parent[u]
    next_depth:int = depth[u] + 1
    for v in graph[u]:
        if v != parent_u:
            parent[v] = u
            depth[v] = next_depth
            order.append(v)

subtree_size:list = [1] * (N + 1)
subtree_size[0] = 0
heavy_child:list = [0] * (N + 1)

for u in reversed(order):
    parent_u = parent[u]
    if parent_u:
        size_u:int = subtree_size[u]
        subtree_size[parent_u] += size_u
        if size_u > subtree_size[heavy_child[parent_u]]:
            heavy_child[parent_u] = u

# 2단계: 비재귀 DFS로 HLD(chain_head, segment_position)와 오일러 투어(in_time, 색상별 누적합) 동시 구축
chain_head:list = [0] * (N + 1)
segment_position:list = [0] * (N + 1)
in_time:list = [0] * (N + 1)
event_time:list = [[] for _ in range(N + 1)]
event_sum:list = [[] for _ in range(N + 1)]

position_timer:int = 0
euler_timer:int = 0

chain_head[1] = 1
stack:list = [1] # 양수: 진입, 음수(~u): 진출
while stack:
    u = stack.pop()
    if u > 0:
        segment_position[u] = position_timer
        position_timer += 1

        euler_timer += 1
        in_time[u] = euler_timer
        c:int = color[u]
        event_time[c].append(euler_timer)
        sums:list = event_sum[c]
        sums.append((sums[-1] if sums else 0) + 1)

        stack.append(~u)

        parent_u = parent[u]
        heavy_u:int = heavy_child[u]
        for v in graph[u]:
            if v != parent_u and v != heavy_u:
                chain_head[v] = v
                stack.append(v)
        if heavy_u:
            chain_head[heavy_u] = chain_head[u]
            stack.append(heavy_u)
    else:
        u = ~u
        euler_timer += 1
        c = color[u]
        event_time[c].append(euler_timer)
        sums = event_sum[c]
        sums.append(sums[-1] - 1)

del graph, order, subtree_size, heavy_child

# 3단계: 비거듭제곱 바텀업 세그먼트 트리 구축 (크기 N, 보이어-무어 상태 저장)
segment_value:list = [0] * (2 * N)
segment_count:list = [0] * (2 * N)

for node in range(1, N + 1):
    leaf:int = segment_position[node] + N
    segment_value[leaf] = color[node]
    segment_count[leaf] = 1

for index in range(N - 1, 0, -1):
    left_child:int = index << 1
    right_child:int = left_child | 1
    lv:int = segment_value[left_child]
    lc:int = segment_count[left_child]
    rv:int = segment_value[right_child]
    rc:int = segment_count[right_child]
    if lv == rv:
        segment_value[index] = lv
        segment_count[index] = lc + rc
    elif lc > rc:
        segment_value[index] = lv
        segment_count[index] = lc - rc
    else:
        segment_value[index] = rv
        segment_count[index] = rc - lc

# 4단계: 쿼리 처리 (HLD 경로 병합으로 과반수 후보 + LCA 동시 계산 후 오일러 투어 검증)
for _ in range(Q):
    u, v = map(int, input().split())

    if u == v:
        print(color[u])
        continue

    candidate_value:int = 0
    candidate_count:int = 0
    current_u:int = u
    current_v:int = v

    while chain_head[current_u] != chain_head[current_v]:
        if depth[chain_head[current_u]] < depth[chain_head[current_v]]:
            current_u, current_v = current_v, current_u

        left:int = segment_position[chain_head[current_u]] + N
        right:int = segment_position[current_u] + N
        while left <= right:
            if left & 1:
                nv:int = segment_value[left]
                nc:int = segment_count[left]
                if candidate_value == nv:
                    candidate_count += nc
                elif candidate_count > nc:
                    candidate_count -= nc
                else:
                    candidate_value = nv
                    candidate_count = nc - candidate_count
                left += 1
            if not (right & 1):
                nv = segment_value[right]
                nc = segment_count[right]
                if candidate_value == nv:
                    candidate_count += nc
                elif candidate_count > nc:
                    candidate_count -= nc
                else:
                    candidate_value = nv
                    candidate_count = nc - candidate_count
                right -= 1
            left >>= 1
            right >>= 1

        current_u = parent[chain_head[current_u]]

    if depth[current_u] > depth[current_v]:
        current_u, current_v = current_v, current_u
    lca:int = current_u

    left = segment_position[current_u] + N
    right = segment_position[current_v] + N
    while left <= right:
        if left & 1:
            nv = segment_value[left]
            nc = segment_count[left]
            if candidate_value == nv:
                candidate_count += nc
            elif candidate_count > nc:
                candidate_count -= nc
            else:
                candidate_value = nv
                candidate_count = nc - candidate_count
            left += 1
        if not (right & 1):
            nv = segment_value[right]
            nc = segment_count[right]
            if candidate_value == nv:
                candidate_count += nc
            elif candidate_count > nc:
                candidate_count -= nc
            else:
                candidate_value = nv
                candidate_count = nc - candidate_count
            right -= 1
        left >>= 1
        right >>= 1

    # 생존 카운트가 0이면 과반수 원소 존재 불가
    if candidate_count == 0:
        print(-1)
        continue

    path_len:int = depth[u] + depth[v] - 2 * depth[lca] + 1

    # 생존 카운트 <= 실제 출현 횟수이므로 이미 과반수 초과 시 검증 생략
    if candidate_count * 2 > path_len:
        print(candidate_value)
        continue

    # 오일러 투어 누적합 이분 탐색으로 경로 내 candidate_value 출현 횟수 검증
    times:list = event_time[candidate_value]
    sums = event_sum[candidate_value]

    index_u:int = bisect_right(times, in_time[u])
    total_candidate:int = sums[index_u - 1] if index_u else 0

    index_v:int = bisect_right(times, in_time[v])
    if index_v:
        total_candidate += sums[index_v - 1]

    index_lca:int = bisect_right(times, in_time[lca])
    if index_lca:
        total_candidate -= sums[index_lca - 1]

    parent_lca:int = parent[lca]
    if parent_lca:
        index_p:int = bisect_right(times, in_time[parent_lca])
        if index_p:
            total_candidate -= sums[index_p - 1]

    if total_candidate * 2 > path_len:
        print(candidate_value)
    else:
        print(-1)