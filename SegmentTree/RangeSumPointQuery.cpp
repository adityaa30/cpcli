#include <bits/stdc++.h>
#define li long long int
using namespace std;

struct SegmentTree {
  li arrSize, tableSize;
  li *table;

  SegmentTree(li n) {
    this->arrSize = n;
    this->tableSize = 2 * n + 1;
    this->table = new li[this->tableSize];
    memset(this->table, 0, sizeof(this->table));
  }

  SegmentTree(li n, li *arr) : SegmentTree(n) {
    for (li i = 0; i < n; ++i) {
      this->table[n + i] = arr[i];
    }
  }

  void Build() {
    for (li i = arrSize - 1; i > 0; --i) {
      // table[i] = table[i * 2] + table[i * 2 + 1];
      table[i] = table[i << 1] + table[i << 1 | 1];
    }
  }

  void Modify(li idx, li val) { // idx is 0 - indexed
    idx += arrSize;
    for (table[idx] = val; idx > 1; idx >>= 1) {
      // (idx ^ i) turns 2 * i into 2 * i + 1 and vice versa
      table[idx >> 1] = table[idx] + table[idx ^ 1];
    }
  }

  li Query(li l, li r) {
    /* l & r both are 0 - indexed
     * Returns sum in [l, r]
     * Increment r by 1 s.t range change from [l, r) */
    r += 1;
    li sum = 0;
    for (l += arrSize, r += arrSize; l < r; l >>= 1, r >>= 1) {
      cout << "Query " << l << ' ' << r << '\n';
      if (l & 1)
        sum += table[l++];
      if (r & 1)
        sum += table[--r];
    }
    return sum;
  }

  li operator[](li idx) { return table[idx]; }
};

int main() {
  li n;
  cin >> n;
  li arr[n];
  for (li i = 0; i < n; ++i) {
    cin >> arr[i];
  }

  SegmentTree st(n, arr);
  st.Build();

  cout << st.Query(1, 6) << '\n';
  st.Modify(1, 15);
  cout << st.Query(1, 6) << '\n';

  return 0;
}