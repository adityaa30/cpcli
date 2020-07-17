// adityaa30
#include "Node.hpp"
#include <bits/stdc++.h>
using namespace std;

const int MOD = 1000000007;

int PosX[] = {0, 1, 0, -1};
int PosY[] = {1, 0, -1, 0};

Node *clone(Node *root) {
  Node *rootBackup = root;
  while (root != NULL) {
    Node *newNode = new Node(root->data);
    newNode->next = root->next;
    root->next = newNode;
    root = root->next->next;
  }

  root = rootBackup;
  while (root != NULL) {
    root->next->random = root->random->next;
    root = root->next->next;
  }

  Node *clonedHead = NULL, *clonedCurr = NULL;
  root = rootBackup;
  while (root != NULL) {
    if (clonedCurr == NULL) {
      clonedHead = root->next;
      clonedCurr = root->next;
    } else {
      clonedCurr->next = root->next;
      clonedCurr = clonedCurr->next;
    }
    root->next = root->next->next;
    root = root->next;
  }

  return clonedHead;
}

int32_t main() { return 0; }