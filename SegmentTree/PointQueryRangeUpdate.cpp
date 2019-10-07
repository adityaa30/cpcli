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
    /* Initally all nodes of the tree should be 0
     * except the array values */
  }

  void Modify(li l, li r, li val) {
    /* l & r both are 0 - indexed
     * Add val to elements in [l, r]
     * Increment r by 1 s.t range change from [l, r) */
    r += 1;
    for (l += arrSize, r += arrSize; l < r; l >>= 1, r >>= 1) {
      if (l & 1)
        table[l++] += val;
      if (r & 1)
        table[--r] += val;
    }
  }

  li Query(li idx, li val) { // idx is 0 - indexed
    li res = 0;
    for (idx += arrSize; idx > 1; idx >>= 1) {
      res += table[idx];
    }

    return res;
  }

  void PushSum() {
    // Push all modifications to the leaf
    for (li i = 1; i < arrSize; ++i) {
      table[i << 1] += table[i];
      table[i << 1 | 1] += table[i];
      table[i] = 0;
    }
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

  cout << st.Query(0, n) << '\n';
  st.Modify(1, 15);
  cout << st.Query(0, n) << '\n';

  return 0;
}