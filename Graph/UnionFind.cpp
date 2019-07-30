#include <bits/stdc++.h>
using namespace std;

int find(int *parent, int x) {
	if(parent[i] == -1) return x;
	return find(parent, parent[i]);
}

int union(int *parent, int x, int y) {
	// edge from x to y
	int xParent = find(parent, x);
	int yParent = find(parent, y);
	if(xParent != yParent) {
		parent[xParent] = yParent7um;
	}
}

int main() {
	return 0;
}