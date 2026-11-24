# 링크 : https://acmicpc.net/problem/10790
import sys
import math

input = sys.stdin.readline

def solve_case(distance_m:int, v_min_mps:int, v_max_mps:int, target_error_mps:int, check_delay_s:int) -> int :
    # 초기에 우리가 좁혀야 할 전체 속력의 불확실성 범위
    current_v_range_mps:int = v_max_mps - v_min_mps
    
    # 분할 가능한 구간의 수 (초기엔 1개의 거대한 구간)
    resolvable_capacity:int = 1
    
    # 코치 민혁이의 확인 횟수
    check_count:int = 0 
    
    # 목표 오차 범위 * 분할 가능 구간 수가 현재 오차 범위보다 작으면 계속 탐색 (결정 트리 확장)
    while target_error_mps * resolvable_capacity < current_v_range_mps :
        # 분할 가능한 구간이 0 이하가 되면 더 이상 측정 불가
        if resolvable_capacity <= 0 :
            break
            
        # 이번 확인을 마쳤을 때 흐른 총 시간 (s)
        elapsed_time_s:int = check_delay_s * (check_count + 1)
        # 측정 불가능한 구간의 개수
        unmeasurable_intervals:int = 0
        
        # [물리적 수식 증명]
        # v_limit = distance_m / elapsed_time_s (이 시간엔 이 속력 이상이면 이미 통과함)
        # 구해야 하는 값 : (v_max_mps - v_limit) / target_error_mps
        # 부동소수점 오차를 막기 위해 분모/분자를 정수로 치환
        # 분자 : (최대 속력으로 달렸을 때의 예상 이동 거리) - (실제 트랙 길이)
        numerator:int = v_max_mps * elapsed_time_s - distance_m
        # 분모 : 오차 구간 1개가 만드는 거리 오차
        denominator:int = elapsed_time_s * target_error_mps
        
        # 분자가 분모보다 커서 1 이상의 구간이 관측 범위를 벗어나는지 확인
        if 1 < math.ceil(numerator / denominator) :
            unmeasurable_intervals = int(math.ceil(numerator / denominator - 1))
            
        # 관측 불가능한 구간만큼 최대 속력 범위를 깎아냄 (최악의 경우를 대비한 상태 축소)
        v_max_mps -= unmeasurable_intervals * target_error_mps
        current_v_range_mps = v_max_mps - v_min_mps
        
        # 다음 단계로 넘어가면 이진 탐색처럼 분기(Branch)가 2배로 늘어남(분할 정복)
        # 단, 이미 결승선을 통과해 측정이 불가능해진 구간은 제외하고 2배를 곱함
        resolvable_capacity = 2 * (resolvable_capacity - unmeasurable_intervals)
        
        # 확인 횟수 증가
        check_count += 1
        
    # 분할 가능한 구간의 수가 0 이하라는 것은 더이상 물리적으로 분할할 수 없는 상태
    # 즉, 주어진 조건에서 절대로 속력을 구할 수 없게 되는 불가능한 경우입니다.
    if resolvable_capacity <= 0 :
        return None
    else :
        return check_count

T:int = int(input().rstrip())
for _ in range(T) :
    l, v1, v2, t, s = map(int, input().split())
    result = solve_case(l, v1, v2, t, s)
    print(result if result is not None else "impossible")


# 가능한 경우
"""
l v1 v2 t s = 60 2 10 2 5인 경우
총 달리기 거리(distance_m)는 60m이고 유라의 속도가 2m/s ~ 10m/s 사이라는 것만 알고 있어요.
목표 오차(target_error_mps)는 2m/s이고 확인하러 가는 지연 시간은 5초입니다.
이 때 속도 범위의 크기(current_v_range_mps)는 10-2 = 8m/s이며 이것은 좁혀야 할 불확실성 범위입니다.
이 때 분할 가능한 구간의 수(resolvable_capacity)는 초기에 1개로 지정합니다.
우리가 구해야 하는 것은 오차 범위 내에 속도가 측정되도록 유라가 뛰어야 하는 횟수입니다.


[1차 측정 사이클]
target_error_mps * resolvable_capacity < current_v_range_mps
이 조건문의 의미는 오차 범위 * 측정 가능한 구간 개수가 속도 범위보다 크거나 같으면
민혁이가 "드디어 오차 범위 내에 속도를 측정이 되었구나!"라는 의미이므로 멈추면 됩니다.
그러면 2 * 1 < 8이면? 민혁이가 "아! 아직 오차 범위가 아니네! 달려가서 측정해야 해!"라는 뜻입니다.
 
민혁이가 처음으로 헐레벌떡 트랙으로 뛰어나갑니다.
(이 때 s = 5이므로 민혁이가 5초 동안 엄청 열심히 달립니다.)
유라가 아무리 빨라도 5초 동안 50m 밖에 못 갔습니다.
트랙 길이가 60m이니 유라는 무조건 트랙 위에 있어요.
이 때 경과시간(elapsed_time_s)은 5초이고요.

그리고 분자는 (최대 속력으로 달렸을 때의 예상 이동 거리) - (실제 트랙 길이)이고
분모는 (오차 구간 1개가 만드는 거리 오차)입니다.
그리고 1과 분자/분모를 비교합니다.

만약 1 >= 분자/분모이면 최대 속력으로 아무리 열심히 달려도 트랙 전체를 벗어나지 못 했다는 뜻입니다.
왜 어째서 0이 아닌 1이냐면 오차범위 t에 의해 (70 / 60) / 10 = 1이라고 해도 
오차범위(5[s] * 2[m/s] = 10[m]) 내에 있으므로 최대 70[m]로 해도 트랙 전체를 벗어나지 않는다고 취급합니다.

이 때 분자/분모가 만약 1.xxx이면 이것은 트랙 전체를 조금이라도 벗어났다는 뜻입니다.
그러므로 math.ceil(분자/분모)로 하는 것이 합리적이며
1 < math.ceil(분자/분모)이면 측정 불가능한 구간은 다음과 같습니다.
unmeasurable_intervals = int(math.ceil(numerator / denominator - 1))
이것의 의미는 분자/분모에서 -1은 (측정 불가능한 구간을 계산할 때는 오차 범위를 무시해야 한다)이며
예시로 (70 / 60) / 10이라고 가정하면 측정 불가능한 구간을 계산하기 위해 -1을 해서 완전히 오차 범위를 제거합니다.
이건 나중에 [2차 측정 사이클]에서 자세히 다루도록 할게요.

[1차 측정 사이클]에서는 분자 / 분모 = (10 * 5 - 60) / (5 * 2) = -1이므로 1 >= -1입니다.
따라서 트랙 전체를 벗어나지 않았으므로 측정 불가능한 구간은 0개입니다.

분할 정복 알고리즘(이진 탐색 알고리즘으로 불러도 되겠네요.)
에 의해 측정 가능한 구간은 정확히 반으로 쪼개집니다.
즉, resolvable_capacity = 2 * (resolvable_capacity - unmeasurable_intervals)에서
unmeasurable_intervals = 0이므로 측정 가능한 구간은 1개 -> 2개가 됩니다.

이렇게 해서 첫번째 측정이 마쳤습니다.(check_count = 1)


[2차 측정 사이클]
2 * 2 < 8이므로 민혁이는 달려나가서 측정해야 합니다.

우와! 민혁이가 5초 정도 더 늦게 나와서 경과 시간이 5초에서 10초가 되었어요.
그런데 이럴 수가! 만약 유라가 최대 속력으로 달린다면 10[s] * 10[m/s] = 100[m]로
전체 트랙 길이인 60[m]를 뛰어넘었어요!
그러면 측정 불가능한 구간이 생겼어요!
왜냐면 최대 속력으로 달렸다면 현실적으로 볼 때 유라는 이미 결승선을 통과하고도 남아서
"아, 코치가 없을 때 튀어야겠다!"라고 하면서 그 자리에 없거든요.
자, 우리 측정 불가능한 구간을 구해봅시다.

우선 분자/분모를 해줘야 해요.
분자/분모 = (10[m/s] * 10[s] - 60[m]) / (10[s] * 2[m/s]) = 2
math.ceil 연산하면 2가 되니 1 < 2가 됩니다.
1 < 분자/분모이니 측정 불가능한 구간이 생겼어요.
이 때 측정 불가능한 구간은 다음과 같습니다.
unmeasurable_intervals = math.ceil(numerator / denominator - 1) = math.ceil(2 - 1) = 1개
전체 구간 2개 중에서 1개가 측정이 안 됩니다!

최대 속력으로 했다면 이미 유라가 튀었나갔으니 튀어나가지 말라는 의미로 최대 속력 v2를 깎아내리겠습니다.
어딜 도망갈려고!
v2 = v2 - unmeasurable_intervals * target_error_mps = 10 - 1 * 2 = 8[m/s]
이렇게 해서 유라의 속도 범위는 2[m/s] ~ 8[m/s]로 좁혀졌고
측정 가능한 구간의 개수는 아까 측정 불가능한 구간 1개 빼고 다시 반으로 쪼개주세요.
resolvable_capacity = 2 * (2 - 1) = 2개

그렇게 해서 2번째 측정이 끝났습니다.(check_count = 2)


[3차 측정 사이클]
2 * 2 < 6이므로 민혁이는 또 달려나가야 합니다.

민혁이 이 놈의 자식이 또 늦어서 15초가 되었어요!
분자/분모 = (8[m/s] * 15[s] - 60[m]) / (15[s] * 2[m/s]) = 2이고 math.ceil(2) = 2입니다.
따라서 1 < 2이므로 측정 불가능한 구간이 생깁니다.
이 때 측정 불가능한 구간은 math.ceil(2 - 1) = 1개입니다.

또 1개의 오차 구간을 버립니다.
그러면 v2 = 8 - 1 * 2 = 6[m/s]가 되고
v2 - v1 = 6 - 2 = 4가 됩니다.

이 때 측정 가능한 구간의 개수는 2 * (2 - 1) = 2개가 됩니다.
이렇게 해서 원만하게 3번째 측정을 성공했습니다.(check_count = 3)


그 뒤 다음 루프에서 t * (측정 가능 구간 개수) < v2 - v1에서
4 < 4이므로 여기서 측정을 멈춥니다.
왜냐면 열심히 달려서 어느 구간에 들어가도 무조건 오차 범위 안에 들어갑니다.

따라서 민혁이는 3번만에 오차 범위 내의 속도를 측정할 수 있게 됩니다.
"""

# 불가능한 경우
"""
같은 테스트 케이스에서 l = 60[m]가 아닌 l = 45[m]이면 어떻게 될까요?
2차 측정 사이클 끝난 후 측정 가능한 구간은 2 * (2 - 2) = 0개가 됩니다.
그러므로 t * (측정 가능 구간 개수) = 2 * 0 = 0으로 while 루프 안에 들어가도
3차 측정 사이클에서 더이상 측정 가능한 구간 자체가 없으므로
민혁이는 멘붕에 빠지면서 "아니! 오차 범위 내에 측정할 수 없다고???"라고 절망합니다.
따라서 l v1 v2 t s = 45 2 10 2 5일 때 "impossible"이 출력됩니다.
"""