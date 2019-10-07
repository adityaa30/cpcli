// adityaa30
#include <bits/stdc++.h>
#define li long long int
#define Debug(a) cout << "|>" #a << "=" << a << "<| ";
#define EmptyArr(ar) memset(ar, 0, sizeof(ar));
using namespace std;

template <typename T> struct SegmentTree {
  T n, *low, *high, *xorVal, *delta;
  SegmentTree(T n, T *arr) {
    this->n = n;
    this->low = new T[4 * n + 1];
    this->high = new T[4 * n + 1];
    this->xorVal = new T[4 * n + 1];
    this->delta = new T[4 * n + 1];

    EmptyArr(this->low);
    EmptyArr(this->high);
    EmptyArr(this->xorVal);
    EmptyArr(this->delta);

    Build(1, 0, n - 1, arr);
  }

  void Build(T i, T a, T b, T *arr) {
    /* Range to initialize [a, b]
     * Current node index = i */
    low[i] = a;
    high[i] = b;
    if (a == b) {
      // Leaf node
      xorVal[i] = arr[a];
      return;
    }

    LazyPropogate(i);

    T m = a + (b - a) / 2;
    Build(i << 1, a, m, arr);
    Build(i << 1 | 1, m + 1, b, arr);

    Update(i);
  }

  void Increment(T a, T b, T val) {
    /* Increase values in range [a, b] by val */
    Increment(1, a, b, val);
  }

  T XOR(T a, T b) {
    /* XOR val in range [a, b] */
    return XOR(1, a, b);
  }

private:
  void LazyPropogate(T i) {
    delta[i << 1] += delta[i];
    delta[i << 1 | 1] += delta[i];
    delta[i] = 0;
  }

  void Update(T i) {
    xorVal[i] = (xorVal[i << 1] + delta[i << 1]) ^
                (xorVal[i << 1 | 1] + delta[i << 1 | 1]);
  }

  void Increment(T i, T a, T b, T val) {
    if (b < low[i] || high[i] < a)
      return;

    if (a <= low[i] && high[i] <= b) {
      delta[i] += val;
      return;
    }

    LazyPropogate(i);
    Increment(i << 1, a, b, val);
    Increment(i << 1 | 1, a, b, val);
    Update(i);
  }
  T XOR(T i, T a, T b) {
    if (b < low[i] || high[i] < a)
      return 0;

    if (a <= low[i] && high[i] <= b) {
      return xorVal[i] + delta[i];
    }

    LazyPropogate(i);
    T xorLeft = XOR(i << 1, a, b);
    T xorRight = XOR(i << 1 | 1, a, b);
    Update(i);

    return xorLeft ^ xorRight;
  }
};

int main() {
  int arr[] = {1, 2, 3, 4};
  int n = sizeof(arr) / sizeof(int);
  SegmentTree<int> st(n, arr);
  cout << st.XOR(0, n - 1) << '\n';
  cout << st.XOR(1, 2) << '\n';
  cout << st.XOR(1, 3) << '\n';
  cout << st.XOR(2, 3) << '\n';
  cout << st.XOR(2, 2) << '\n';
  return 0;
}