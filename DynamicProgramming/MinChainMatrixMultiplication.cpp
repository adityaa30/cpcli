#include <iostream>

void PrintBrackets(int *brackets, int i, int j, int n, char& alpha) {
    if(i == j) {
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

    for(int i = 1; i < n; ++i) dp[i][i] = 0;

    for(int L = 2; L < n; ++L) {
        for(int i = 1; i < n - L + 1; ++i) {
            j = i + L - 1;
            for(int k = i; k < j; ++k) {
                temp = dp[i][k] + dp[k+1][j] + p[i-1]*p[k]*p[j];
                if(temp < dp[i][j]) {
                    dp[i][j] = temp;
                    bracket[i][j] = k;
                }
            }
        }
    }

    return dp[1][n - 1];
}

int main() {
    return 0;
}