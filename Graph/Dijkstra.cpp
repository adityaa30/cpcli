#include <bits/stdc++.h>
#include <limits.h>
#define fio ios_base::sync_with_stdio(false); cin.tie(NULL); cout.tie(NULL);
#define li long long int
#define mod 1000000007
using namespace std;

li minDistance(li dist[], bool sptSet[], li V)
{

    li min = INT_MAX, min_index;
    for (li v = 0; v < V; v++)
        if (sptSet[v] == false && dist[v] <= min)
            min = dist[v], min_index = v;
    return min_index;
}

li printSolution(li dist[], li V)
{

    cout << "Vertex\tDistance from Source" << endl;
    for (li i = 0; i < V; i++)
        cout << i << '\t' << dist[i] << endl;
}

void dijkstra(li graph[][100000], li src, li V)
{

    li dist[V];
    bool sptSet[V];

    for (li i = 0; i < V; i++)
        dist[i] = INT_MAX, sptSet[i] = false;

    dist[src] = 0;

    for (li count = 0; count < V - 1; count++)
    {
        // *(graph + v + V *)
        li u = minDistance(dist, sptSet, V);
        sptSet[u] = true;
        for (li v = 0; v < V; v++)
            if (!sptSet[v] && graph[u][v] && dist[u] != INT_MAX && dist[u] + graph[u][v] < dist[v])
                dist[v] = dist[u] + graph[u][v];
    }

    printSolution(dist, V);
}

int main()
{
    fio;

    li n, m, x, y, wt, s;
    cin >> n >> m;
    li graph[n][100000];

    for (li i = 0; i < n; ++i)
    {
        for (li j = 0; j < n; ++j)
        {
            graph[i][j] = 0;
        }
    }

    for (li i = 0; i < m; ++i)
    {
        cin >> x >> y >> wt;
        graph[x - 1][y - 1] = wt;
        graph[y - 1][x - 1] = wt;
    }
    cin >> s;
    dijkstra(graph, s - 1, n);

    return 0;
}