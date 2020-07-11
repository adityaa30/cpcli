// adityaa30
#include <bits/stdc++.h>
#define int long long int
using namespace std;

const int MOD = 1000000007;

int random(int a, int b) { return a + rand() % (b - a + 1); }

int32_t main(int32_t argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);
  cout.tie(NULL);
  cout << fixed << setprecision(20);

  srand(time(0));
  int t = random(1, 10);
  cout << t << "\n";
  while (t--) {
    // Generate test case here

  }

  return 0;
}