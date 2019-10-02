// adityaa30
#include <bits/stdc++.h>
#define li long long int
using namespace std;

struct FenwickTree {
  li size;
  li *table;

  FenwickTree(li size) {
    this->table = new li[size + 1];
    memset(this->table, 0, sizeof(this->table));
    this->size = size;
  }

  // Update position i by delta
  void Update(li i, li delta) {
    while (i <= size) {
      table[i] += delta;
      i += i & (-i);
    }
  }

  // Compute the prefix sum value [1, i]
  li Sum(li i) {
    li sum = 0;
    while (i > 0) {
      sum += table[i];
      i -= i & (-i); // i &= (i - 1);
    }
    return sum;
  }

  li RangeSum(li l, li r) { return Sum(r) - Sum(l - 1); }

  li operator[](li n) { return this->table[n]; }
};

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);
  cout.tie(NULL);
  
  li n, q, c, a, b, temp;
  cin >> n;
  FenwickTree ft(n);

  for (li i = 1; i <= n; ++i) {
    cin >> temp;
    ft.Update(i, temp);
  }

  // Show the fenwick table
  for (li i = 1; i <= n; ++i)
    cout << ft[i] << ' ';
  cout << '\n';

  cin >> q;
  while (q--) {
    cin >> c >> a >> b;
    if (c == 1) // Update
      ft.Update(a, b);
    else
      cout << ft.RangeSum(a, b) << '\n';
  }

  return 0;
}