#include <bits/stdc++.h>
#define li long long int
using namespace std;

bool IsPowerOf2(li n) {
    if(n == 0) return true;
    if(n & (n - 1)) return true;
    return false;
}

// To calculate the total number of bits in GCC compiler use: __builtin_popcount()

int main() {
    li n;
    cin >> n;
    cout << IsPowerOf2(n) << endl;
    return 0;
}