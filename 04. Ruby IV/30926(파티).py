# 링크 : https://acmicpc.net/problem/30926
import sys

input = sys.stdin.readline

# 문제 출처 : https://atcoder.jp/contests/wtf22-day2/tasks/wtf22_day2_c
# 에디토리얼 : https://atcoder.jp/contests/wtf22-day2/editorial/7033

def new_state(personalities:int) -> list:
    return [0, 0, 0, [0] * personalities]

def process_small(state:list, personality:int) -> None:
    small_count, big_count, _, per_personality_capacity = state
    if per_personality_capacity[personality] < big_count:
        per_personality_capacity[personality] = big_count
    per_personality_capacity[personality] += 1
    
    state[0] = small_count + 1

def process_big(state:list, personality:int) -> bool:
    small_count, big_count, mincut_f, per_personality_capacity = state
    if per_personality_capacity[personality] < big_count:
        per_personality_capacity[personality] = big_count
    per_personality_capacity[personality] += 1
    
    big_count += 1
    mincut_f += 1
    threshold = small_count + big_count - per_personality_capacity[personality]
    if mincut_f > threshold:
        mincut_f = threshold
        state[0], state[1], state[2] = small_count, big_count, mincut_f
        return False

    state[0], state[1], state[2] = small_count, big_count, mincut_f
    return True

blossom_girls, limit_k = map(int, input().split())

# (value, personality_tag) 구성
# small 항목: (b, a)             (b*2 <= k)
# big   항목: (k-b, a+num_girls) (b*2 >  k)
# 참고로 big은 W = k - b로 저장
items:list = []
for _ in range(blossom_girls):
    personality, happiness = map(int, input().split())
    personality -= 1
    if happiness * 2 <= limit_k:
        items.append((happiness, personality)) # small
    else:
        items.append((limit_k - happiness, personality + blossom_girls)) # big
items.sort() # value 오름차순(여기서 그리디 알고리즘 적용)

# 1단계: 모든 small은 유지, big은 타당성(매칭 가능)인 것만 유지
write_index:int = 0
state:list = new_state(blossom_girls)
for value, tag in items:
    if tag < blossom_girls:
        process_small(state, tag)
        items[write_index] = (value, tag)
        write_index += 1
    else:
        if process_big(state, tag - blossom_girls):
            items[write_index] = (value, tag)
            write_index += 1
items = items[:write_index]

# 2단계: 걸러진 시퀀스를 다시 스캔해 상태(state) 재구성
state = new_state(blossom_girls)
for value, tag in items:
    if tag < blossom_girls:
        process_small(state, tag)
    else:
        process_big(state, tag - blossom_girls)

small_total, big_total, _, per_personality_capacity = state

# 남아 있는 small들 중 다수 성격(과반 존재 여부) 찾기
majority_personality:int = -1
for c in range(blossom_girls) :
    # 성격의 잔여 small 개수 = per_personality_capacity[c] - big_total
    remain_c = per_personality_capacity[c] - big_total
    if remain_c * 2 > (small_total - big_total) :
        majority_personality = c
        break

# 제거해야 할 small의 개수(= parity 혹은 과반 보정)
if majority_personality == -1 :
    need_to_remove:int = (small_total + big_total) & 1
else :
    need_to_remove = (per_personality_capacity[majority_personality] - big_total) * 2 - (small_total - big_total)

# suffix에서 타당성을 유지하며 제거 가능한 후보 small들의 값 모으기
removable_values:list = []
scan_state:list = new_state(blossom_girls)

for value, tag in reversed(items) :
    if tag < blossom_girls :
        if majority_personality == -1 or majority_personality == tag :
            # 지금 이 small을 선택하면 타당성 깨짐 -> 제거 후보
            if not process_big(scan_state, tag):
                removable_values.append(value)
    else :
        process_small(scan_state, tag - blossom_girls)

removable_values.reverse()
if need_to_remove > len(removable_values) : # 이론상 발생하지 않지만 안전장치
    need_to_remove = len(removable_values)
remove_sum:int = sum(removable_values[:need_to_remove])

# 최종 합계 계산
# small 항목은 value(= b)
# big   항목은 (k - value)(= b)
result:int = 0
for value, tag in items :
    if tag < blossom_girls :
        result += value
    else :
        result += (limit_k - value)
result -= remove_sum

print(result)