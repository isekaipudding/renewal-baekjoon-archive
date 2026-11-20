# 링크 : https://acmicpc.net/problem/18738
import sys

input = sys.stdin.readline

INF = 10 ** 9

N:int = int(input().rstrip())
L1:list = list(map(int, input().split())) # 드미트릭의 카드 목록
L2:list = list(map(int, input().split())) # 페트로의 카드 목록

L1.sort()
L2.sort()

turn:int = 0
result:int = 0

while True:
    if turn == 0:
        if not L1 or L1[-1] < L2[0]:
            break

        if L1[0] > L2[-1]:
            result += len(L1)
            break

        number:int = len(L1)

        best_diff = -INF
        best_dmytryk = 0
        best_petro = 0
        j = 0
        for i in range(number):
            while j < number and L2[j] <= L1[i]:
                j += 1
            if j < number:
                diff = i - j
                if diff > best_diff:
                    best_diff = diff
                    best_dmytryk = i
                    best_petro = j
            else:
                break
            
        L1.pop(best_dmytryk)
        L2.pop(best_petro)

        result += number - 1

        turn = 1

    else :
        if not L2 or L2[-1] < L1[0]:
            break

        if L2[0] > L1[-1] :
            result -= len(L2)
            break

        number:int = len(L2)

        best_diff = -INF
        best_petro = 0
        best_dmytryk = 0
        j = 0
        for i in range(number):
            while j < number and L1[j] <= L2[i]:
                j += 1
            if j < number:
                diff = i - j
                if diff > best_diff:
                    best_diff = diff
                    best_petro = i
                    best_dmytryk = j
            else:
                break

        L1.pop(best_dmytryk)
        L2.pop(best_petro)

        result -= number - 1

        turn = 0

print(result)

"""
[문제 개요]
두 플레이어 드미트릭(L1)과 페트로(L2)가 각각 N장의 카드를 들고 진행하는 완전 정보 2인 제로섬 게임입니다.
- 첫 라운드는 드미트릭이 선공이며, 이후에는 직전 라운드의 승자가 다음 라운드의 선공이 됩니다.
- 선공이 카드 한 장을 내면, 후공은 이를 보고 카드를 냅니다.
- 단, 후공은 선공의 카드보다 큰 카드를 하나라도 가지고 있다면 반드시 그중 하나를 내어 승리해야 합니다.
- 두 플레이어 모두 자신의 승리 라운드 수를 최대화하는 최적 전략(미니맥스)을 쓸 때, 드미트릭의 최종 승리 횟수를 구합니다.

[핵심 수학적 구조]
1. 교대합 점화식 (result += number - 1, result -= number - 1의 이유)
   현재 남은 카드가 k장일 때,
   - f(L1, L2): 드미트릭 선공 시 드미트릭이 얻는 최대 승수
   - g(L1, L2): 페트로 선공 시 페트로가 얻는 최대 승수
   라고 정의합니다. (제로섬 게임이므로 페트로 선공 시 드미트릭의 승수는 k - g(L1, L2)입니다.)

   선공이 이번 라운드에서 상대가 이길 수 있는 카드를 내어 1패를 감수하고 선공권을 넘기면,
   남은 (k - 1)라운드에서 상대가 선공을 잡게 됩니다. 따라서 다음 점화식이 성립합니다.
   - 드미트릭 선공: f(L1, L2) = 0 + ((k - 1) - g(L1', L2')) = (k - 1) - g(L1', L2')
   - 페트로 선공:   g(L1', L2') = 0 + ((k - 2) - f(L1'', L2'')) = (k - 2) - f(L1'', L2'')

   이를 반복 대입하면 최종 답은 다음과 같은 교대합(alternating sum)으로 전개됩니다.
   f(L1, L2) = +(k - 1) - (k - 2) + (k - 3) - ... ± (기저 상태의 승수)
   코드에서 turn == 0일 때 result += number - 1, turn == 1일 때 result -= number - 1을
   수행하는 것은 바로 이 점화식의 부호 반전을 재귀 없이 반복문으로 풀어낸 것입니다.

2. 기저 조건 (종료 조건)
   - turn == 0:
     * L1[-1] < L2[0]: 드미트릭의 모든 카드가 페트로보다 작으므로 f = 0 (+0 후 종료)
     * L1[0] > L2[-1]: 드미트릭의 모든 카드가 페트로보다 크므로 f = len(L1) (+len(L1) 후 종료)
   - turn == 1 (앞선 점화식에 의해 -g(L1, L2)로 반영):
     * L2[-1] < L1[0]: 페트로의 모든 카드가 드미트릭보다 작으므로 g = 0 (-0 후 종료)
     * L2[0] > L1[-1]: 페트로의 모든 카드가 드미트릭보다 크므로 g = len(L2) (-len(L2) 후 종료)

3. 왜 (i - j)를 최대화하는 쌍을 선택하는가? (높이 함수 해석)
   정렬된 L1(D)과 L2(P)를 오름차순으로 하나의 수열로 합친 뒤,
   D를 만나면 +1, P를 만나면 -1을 더하는 누적합(높이 h = #D - #P)을 생각해 봅니다.
   - 드미트릭의 최악의 상태(전패, DDD...PPP)는 높이가 전부 양수인 산 모양입니다.
   - 드미트릭의 최선의 상태(전승, PPP...DDD)는 높이가 전부 음수인 골짜기 모양입니다.

   드미트릭 선공(turn == 0)에서 카드 L1[i]를 내면, 후공 페트로는 최적 대응으로
   L1[i]보다 큰 가장 작은 카드 L2[j]를 냅니다.
   이때 L1[i]보다 작은 드미트릭 카드는 i장, 페트로 카드는 j장이므로
   i - j는 정확히 L1[i] 직전의 누적 높이(#D - #P)가 됩니다.

   - 같은 L2[j]를 가리키는 여러 L1[i] 중에는 가장 큰 i(즉, 합친 수열에서 L2[j] 바로 앞에 인접한 D)가
     i - j를 최대화합니다.
   - 따라서 i - j가 최대인 (i, j)를 제거하는 것은 합친 수열에서 인접한 DP 쌍(+1 후 -1로 꺾이는 봉우리) 중
     가장 높은 봉우리를 깎아내는 작업과 같습니다. 이는 나머지 구간의 상대 높이를 건드리지 않고
     드미트릭에게 가장 불리한 최대 높이를 낮추는 최적의 선택입니다.
   - 대칭적으로 페트로 선공(turn == 1)에서 i - j 최대화는 (#P - #D) 최대화,
     즉 (#D - #P)가 최소인 가장 깊은 PD 골짜기를 메워 드미트릭의 우위를 깎아내는 최적 대응입니다.

[시뮬레이션 예시]
L1 = [1, 4, 6], L2 = [2, 3, 5] (합친 수열: 1D 2P 3P 4D 5P 6D)
1. turn = 0 (number = 3):
   - (i=0, j=0) -> 1 vs 2, i - j = 0 (최대)
   - (i=1, j=2) -> 4 vs 5, i - j = -1
   -> (1, 2) 제거, 남은 카드 L1 = [4, 6], L2 = [3, 5]
   -> result = 0 + (3 - 1) = 2, turn = 1
2. turn = 1 (number = 2):
   - (i=0, j=0) -> 3 vs 4, i - j = 0 (최대)
   - (i=1, j=1) -> 5 vs 6, i - j = 0
   -> (3, 4) 제거, 남은 카드 L1 = [6], L2 = [5]
   -> result = 2 - (2 - 1) = 1, turn = 0
3. turn = 0 (number = 1):
   - L1[0](6) > L2[-1](5) 종료 조건 충족
   -> result = 1 + 1 = 2, 종료 (최종 출력: 2)

[시간 복잡도 최적화]
L1과 L2가 오름차순으로 정렬되어 있으므로 i가 증가함에 따라 조건을 만족하는 최소 인덱스 j도 단조 증가합니다.
따라서 j를 매 i마다 0으로 초기화하지 않고 투 포인터(Two Pointers)로 유지하여
라운드당 탐색을 O(N^2)에서 O(N)으로 단축했으며, 전체 시간 복잡도는 O(N^2)입니다.
"""