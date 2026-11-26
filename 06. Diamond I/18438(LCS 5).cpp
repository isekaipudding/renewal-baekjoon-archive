// https://acmicpc.net/problem/18438
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

static string A, B;
static vector<int> Lrow, Rrow, current_row;

// L[j] = LCS(A[xl..xr], B[yl..yl+j-1]) (j = 0..m)
static void lcs_prefix_dp(int xl, int xr, int yl, int yr, vector<int>& out) {
    const int m = yr - yl + 1;
    fill(out.begin(), out.begin() + m + 1, 0);

    for (int i = xl; i <= xr; i++) {
        const char c = A[i];
        current_row[0] = 0;
        for (int j = 1; j <= m; j++) {
            if (c == B[yl + j - 1]) {
                current_row[j] = out[j - 1] + 1;
            } else {
                current_row[j] = (out[j] > current_row[j - 1]) ? out[j] : current_row[j - 1];
            }
        }
        out.swap(current_row);
    }
}

// R[j] = LCS(A[xl..xr], B[yl+j..yr]) (j = 0..m)
static void lcs_suffix_dp(int xl, int xr, int yl, int yr, vector<int>& out) {
    const int m = yr - yl + 1;
    fill(out.begin(), out.begin() + m + 1, 0);

    for (int i = xr; i >= xl; i--) {
        const char c = A[i];
        current_row[m] = 0;
        for (int j = m - 1; j >= 0; j--) {
            if (c == B[yl + j]) {
                current_row[j] = out[j + 1] + 1;
            } else {
                current_row[j] = (out[j] > current_row[j + 1]) ? out[j] : current_row[j + 1];
            }
        }
        out.swap(current_row);
    }
}

// 히르쉬버그 분할 정복
static void hirschberg(int xl, int xr, int yl, int yr, string& lcs) {
    if (xl > xr || yl > yr) return;

    if (xl == xr) {
        const char c = A[xl];
        for (int j = yl; j <= yr; j++) {
            if (B[j] == c) {
                lcs.push_back(c);
                return;
            }
        }
        return;
    }

    const int mid = (xl + xr) >> 1;
    const int m = yr - yl + 1;

    lcs_prefix_dp(xl, mid, yl, yr, Lrow);
    lcs_suffix_dp(mid + 1, xr, yl, yr, Rrow);

    int k = 0;
    int best = Lrow[0] + Rrow[0];
    for (int j = 1; j <= m; j++) {
        const int v = Lrow[j] + Rrow[j];
        if (v > best) {
            best = v;
            k = j;
        }
    }

    hirschberg(xl, mid, yl, yl + k - 1, lcs);
    hirschberg(mid + 1, xr, yl + k, yr, lcs);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> A >> B;
    const int NA = static_cast<int>(A.size());
    const int NB = static_cast<int>(B.size());

    Lrow.assign(NB + 1, 0);
    Rrow.assign(NB + 1, 0);
    current_row.assign(NB + 1, 0);

    string lcs;
    lcs.reserve(min(NA, NB));
    hirschberg(0, NA - 1, 0, NB - 1, lcs);

    cout << lcs.size() << '\n';
    if (!lcs.empty()) {
        cout << lcs << '\n';
    }
    return 0;
}