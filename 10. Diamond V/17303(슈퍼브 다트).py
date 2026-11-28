# 링크 : https://acmicpc.net/problem/17303
import sys
import math

read = sys.stdin.read
write = sys.stdout.write

tokens:list = read().split()

N, M = int(tokens[0]), int(tokens[1])
index:int = 2

x:list = [0] * (N + 1)
y:list = [0] * (N + 1)
for i in range(1, N + 1):
    x[i] = int(tokens[index])
    y[i] = int(tokens[index + 1])
    index += 2

# 간선 id -> 반간선 (2*id: u->v, 2*id + 1: v->u), 반대 방향 반간선은 (e ^ 1)
total_half_edges:int = M << 1
graph:list = [[] for _ in range(N + 1)]
to_node:list = [0] * total_half_edges
edge_cross:list = [0] * total_half_edges

for edge_id in range(M):
    u:int = int(tokens[index])
    v:int = int(tokens[index + 1])
    index += 2
    forward_edge:int = edge_id << 1
    reverse_edge:int = forward_edge | 1

    to_node[forward_edge] = v
    to_node[reverse_edge] = u

    # 신발끈 공식 기여분(x_u * y_v - y_u * x_v)을 미리 저장
    cross_value:int = x[u] * y[v] - y[u] * x[v]
    edge_cross[forward_edge] = cross_value
    edge_cross[reverse_edge] = -cross_value

    graph[u].append(forward_edge)
    graph[v].append(reverse_edge)

# 각 정점의 진출 반간선을 반시계(CCW) 정렬 후, 진입 반간선(out_edge ^ 1)의 다음 반간선을 바로 연결
next_edge:list = [0] * total_half_edges
atan2 = math.atan2

for u in range(1, N + 1):
    edges:list = graph[u]
    degree:int = len(edges)
    if degree == 0:
        continue

    # 차수가 1 또는 2인 정점은 순환 순서가 유일하므로 각도 정렬 생략
    if degree > 2:
        edges.sort(
            key=lambda e, ux=x[u], uy=y[u]: atan2(y[to_node[e]] - uy, x[to_node[e]] - ux)
        )

    # CCW 순환에서 out_edge 직전 간선(prev_edge)이 곧 (out_edge ^ 1)로 진입했을 때의 다음 간선
    prev_edge:int = edges[-1]
    for out_edge in edges:
        next_edge[out_edge ^ 1] = prev_edge
        prev_edge = out_edge

# 모든 미방문 반간선에서 면(face) 사이클 추적
visited:bytearray = bytearray(total_half_edges)
valid_areas:list = []
append_area = valid_areas.append

for start_edge in range(total_half_edges):
    if visited[start_edge]:
        continue

    area2:int = 0
    current_edge:int = start_edge
    while not visited[current_edge]:
        visited[current_edge] = 1
        area2 += edge_cross[current_edge]
        current_edge = next_edge[current_edge]

    # 양수 넓이(반시계 내부 면)만 수집, 무한 외부 면(음수) 및 브리지/트리(0)는 제외
    if area2 > 0:
        append_area(area2)

valid_areas.sort()

# 정수 좌표 다각형의 2배 넓이는 정수이므로 실제 넓이는 항상 .0 또는 .5로 정확히 표현됨
result:list = [str(len(valid_areas))]
result.extend(
    f"{area2 >> 1}.5" if area2 & 1 else f"{area2 >> 1}.0"
    for area2 in valid_areas
)
write("\n".join(result))