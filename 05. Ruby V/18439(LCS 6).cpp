// 링크 : https://acmicpc.net/problem/18439
#include <iostream>
#include <vector>
#include <string>
#include <bitset>

using namespace std;

using U64 = unsigned long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string A, B;
    cin >> A >> B;

    // 짧은 문자열을 A로 두어 비트마스크 워드 수와 메모리 최소화
    if (A.size() > B.size()) swap(A, B);

    const int N = static_cast<int>(A.size());
    const int M = static_cast<int>(B.size());
    const int W = (N + 63) >> 6;

    vector<vector<U64>> masks(256, vector<U64>(W, 0ULL));
    for (int i = 0; i < N; i++) {
        unsigned char c = static_cast<unsigned char>(A[i]);
        masks[c][i >> 6] |= (1ULL << (i & 63));
    }

    vector<U64> S(W, 0ULL);

    for (int j = 0; j < M; j++) {
        const vector<U64>& mask_row = masks[static_cast<unsigned char>(B[j])];
        U64 carry = 1ULL;  // i == 0에서 (S[0] << 1) | 1ULL 자동 처리
        U64 borrow = 0ULL;

        for (int i = 0; i < W; i++) {
            U64 x = S[i] | mask_row[i];
            U64 sh = (S[i] << 1) | carry;
            carry = S[i] >> 63;

            U64 t = x - borrow;
            U64 b1 = (x < borrow);
            U64 sub = t - sh;
            U64 b2 = (t < sh);
            borrow = b1 | b2;

            S[i] = x & (~sub);
        }
    }

    int result = 0;
    for (int i = 0; i < W; i++) {
        result += static_cast<int>(bitset<64>(S[i]).count());
    }

    cout << result << '\n';
    return 0;
}