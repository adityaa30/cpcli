// adityaa30
#include <bits/stdc++.h>
#define int long long int
#define print1(a) cout << '(' << #a << '=' << a << ')';
#define print2(a, b)                                                           \
  cout << '(' << #a << '=' << a << ',' << #b << '=' << b << ')';
#define print3(a, b, c)                                                        \
  cout << '(' << #a << '=' << a << ',' << #b << '=' << b << ',' << #c << '='   \
       << c << ')';
#define print(it)                                                              \
  cout << #it << " -> ";                                                       \
  for (auto __x__ : it)                                                        \
    cout << __x__ << ' ';                                                      \
  cout << '\n';
using namespace std;
const int MOD = 1000000007;

int PosX[] = {0, 1, 0, -1, 1, 1, -1, -1};
int PosY[] = {1, 0, -1, 0, 1, -1, 1, -1};

void Solve() {
  // Start here
}

int32_t main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);
  cout.tie(NULL);
  cout << fixed << setprecision(20);

  int t = 1;
  cin >> t;
  for (int test = 1; test <= t; ++test) {
    Solve();
  }

  return 0;
}