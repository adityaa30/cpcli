// adityaa30
#include <bits/stdc++.h>
#define int long long int
#define debug(a) cout << #a << "=" << a << ' ';
#define print(it)                                                              \
  cout << #it << ' -> ';                                                       \
  for (auto __x__ : it)                                                        \
    cout << __x__ << ' ';                                                      \
  cout << '\n';
using namespace std;

const int MOD = 1000000007;

int PosX[] = {0, 1, 0, -1, 1, 1, -1, -1};
int PosY[] = {1, 0, -1, 0, 1, -1, 1, -1};

// pair(Weight, Idx)

struct Pair {
  int weight, idx;

  Pair(int weight, int idx) : weight(weight), idx(idx) {}
};

struct ComparePair {
  bool operator()(Pair &a, Pair &b) { return a.weight < b.weight; }
};

void Dijkstra(vector<vector<Pair>> &adj) {
  int V = adj.size();
  vector<bool> visited(V, false);
  vector<int> distance(V, INT_MAX);
  priority_queue<Pair, vector<Pair>, ComparePair> pq;

  int src = 0;
  distance[src] = 0;
  pq.push(Pair(0, src));

  while (!pq.empty()) {
    Pair top = pq.top(); pq.pop();
    for (Pair child : adj[top.idx]) {
      if (!visited[child.idx] &&
          (distance[top.idx] + child.weight) < distance[child.idx]) {
        distance[child.idx] = distance[top.idx] + child.weight;
        pq.push(Pair(distance[child.idx], child.idx));
      }
    }
  }

  for (int i = 0; i < distance.size(); ++i) {
    cout << "Distance(" << i << ") = " << distance[i] << '\n';
  }
}

int32_t main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);
  cout.tie(NULL);
  cout << fixed << setprecision(20);

  int V = 9;
  vector<vector<Pair>> adj(V);

  function<void(int, int, int)> addEdge = [&](int a, int b, int weight) {
    adj[a].push_back(Pair(weight, b));
    adj[b].push_back(Pair(weight, a));
  };

  addEdge(0, 1, 4);
  addEdge(0, 7, 8);
  addEdge(1, 2, 8);
  addEdge(1, 7, 11);
  addEdge(2, 3, 7);
  addEdge(2, 8, 2);
  addEdge(2, 5, 4);
  addEdge(3, 4, 9);
  addEdge(3, 5, 14);
  addEdge(4, 5, 10);
  addEdge(5, 6, 2);
  addEdge(6, 7, 1);
  addEdge(6, 8, 6);
  addEdge(7, 8, 7);

  Dijkstra(adj);

  return 0;
}