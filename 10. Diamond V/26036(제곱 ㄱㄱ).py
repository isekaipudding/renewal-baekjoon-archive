# 링크 : https://acmicpc.net/problem/26036
import sys

input = sys.stdin.readline

# 펠 방정식으로 증명하는 것은 매우 더럽게 어려운데
# 막상 소스 코드가 이게 끝이라는 것이...ㅋㅋㅋㅋㅋㅋㅋㅋ

N:int = int(input().rstrip())
target:int = 10 ** N

x:int = 3
y:int = 1

while x <= target:
    x, y = 3 * x + 8 * y, x + 3 * y

print(y, 2)
print(x, 1)