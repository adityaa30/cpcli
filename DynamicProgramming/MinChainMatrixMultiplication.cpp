#include <bits/stdc++.h>
using namespace std;

void PrintBrackets(int *brackets, int i, int j, int n, char &alpha) {
  if (i == j) {
    printf("%c", alpha++);
    return;
  }
  printf("(");
  PrintBrackets(brackets, i, *((brackets + i * n) + j), n, alpha);
  PrintBrackets(brackets, *((brackets + i * n) + j) + 1, j, n, alpha);
  printf(")");
}

int Matrix(int *p, int n) {
  int dp[n][n], j, bracket[n][n], temp;

  for (int i = 1; i < n; ++i)
    dp[i][i] = 0;

  for (int L = 2; L < n; ++L) {
    for (int i = 1; i < n - L + 1; ++i) {
      j = i + L - 1;
      for (int k = i; k < j; ++k) {
        temp = dp[i][k] + dp[k + 1][j] + p[i - 1] * p[k] * p[j];
        if (temp < dp[i][j]) {
          dp[i][j] = temp;
          bracket[i][j] = k;
        }
      }
    }
  }

  return dp[1][n - 1];
}

int FasterMatrix(vector<int> p) {
  int n = p.size();
  vector<vector<int>> dp(n, vector<int>(n, 0));

  for (int L = 0; L < n - 1; ++L) {
    for (int i = 0; i < n - L; ++i) {
      dp[i][i + L] = min(dp[i + 1][i + L] + p[i - 1] * p[i] * p[i + L],
                         dp[i][i + L - 1] + p[i - 1] * p[i + L - 1] * p[i + L]);
    }
  }

  return dp[1][n - 1];
}

int main() { return 0; }