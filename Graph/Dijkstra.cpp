#include <bits/stdc++.h>
#include <limits.h>
#define fio                           \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL);
#define li int
#define mod 1000000007
using namespace std;

li graph[3001][3001];

li minDistance(li dist[], bool sptSet[], li V)
{

    li min = INT_MAX, min_index;
    for (li v = 0; v < V; v++)
        if (sptSet[v] == false && dist[v] <= min)
            min = dist[v], min_index = v;
    return min_index;
}

void printSolution(li dist[], li V)
{
    // Prints the distance of all the vertices from the given source vertex
    printf("Vertex\tDistance\n");
    for (li i = 0; i < V; ++i)
        if (dist[i] == INT_MAX)
            printf("%d\t=>\tINF\n", i);
        else
            printf("%d\t=>\t%d\n", i, dist[i]);
}

void dijkstra(li graph[][3001], li src, li V)
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

    // n -> Number of vertices
    // v -> Number of edges

    li n, m, x, y, wt, s;
    scanf("%d %d", &n, &m);

    for (li i = 0; i < n; ++i)
        for (li j = 0; j < n; ++j)
            graph[i][j] = 0;

    for (li i = 0; i < m; ++i)
    {
        scanf("%d %d %d", &x, &y, &wt);

        // If more than 2 edges are present between a pair of vertices,
        // then take the edge with less weight.
        if (graph[x - 1][y - 1] == 0 || graph[x - 1][y - 1] > wt)
        {
            graph[x - 1][y - 1] = wt;
            graph[y - 1][x - 1] = wt;
        }
    }

    scanf("%d", &s);
    dijkstra(graph, s - 1, n);

    return 0;
}