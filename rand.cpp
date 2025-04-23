#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

const int INF = 1e9;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
    }

    vector<vector<int> > dp(n + 1, vector<int>(3, INF));
    dp[0][0] = 0; 

    for (int i = 1; i <= n; ++i) {
        int today = a[i - 1];

        dp[i][0] = min(dp[i - 1][0], min(dp[i - 1][1], dp[i - 1][2])) + 1;

        if (today == 1 || today == 3) {
            dp[i][1] = min(dp[i - 1][0], dp[i - 1][2]);
        }

        if (today == 2 || today == 3) {
            dp[i][2] = min(dp[i - 1][0], dp[i - 1][1]);
        }
    }

    int result = min(dp[n][0], min(dp[n][1], dp[n][2]));
    cout << result << endl;

    return 0;
}