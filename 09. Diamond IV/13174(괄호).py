# 링크 : https://acmicpc.net/problem/13174
import sys

input = sys.stdin.readline

MOD = 1_000_000_007

# 에디토리얼 : https://higstudev.github.io/BOJ13174/
# 증명이 너무 까다로워서 결론부터 말하자면
# 답은 sigma(from k = ceil(N/2) to N) K^k * (N_C_k - N_C_(k+1)) % MOD

# 이항 계수 구하는 함수
def nCr(n, r) :
    if r < 0 or r > n :
        return 0
    return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD

N, K = map(int, input().split())

fact:list = [1 for _ in range(N+1)]
invfact = [1 for _ in range(N + 1)]

for i in range(1, N + 1):
    fact[i] = fact[i - 1] * i % MOD

invfact[N] = pow(fact[N], MOD - 2, MOD)
for i in range(N, 0, -1) :
    invfact[i - 1] = invfact[i] * i % MOD

start:int = (N + 1) // 2 # ceil(N/2)
powK:int = pow(K, start, MOD)

result:int = 0
for k in range(start, N + 1) :
    count:int = (nCr(N, k) - nCr(N, k + 1)) % MOD
    result = (result + count * powK) % MOD
    powK = powK * K % MOD

print(result)