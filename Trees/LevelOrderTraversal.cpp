#include <bits/stdc++.h>
#define li long long int
using namespace std;

struct Node {
    li data;
    Node *right, *left, *next;

    Node(li _data) {
        data = _data;
        right = NULL;
        left = NULL;
        next = NULL;
    }

    static void LevelOrderTraversalWithSpace(Node *node, bool printNext);
    static void ConnectSameLevelNodesWithSpace(Node *node);
};

void Node::LevelOrderTraversalWithSpace(Node *node, bool printNext=false) {
    if(node == NULL) return;
    queue<Node*> q;
    
    q.push(node);
    while(!q.empty()) {
        Node *currNode = q.front();
        if(printNext) {
            cout << (currNode->next ? currNode->next->data : -1) << " ";
        } else {
            cout << currNode->data << " ";
        }
        q.pop();

        if(currNode->left != NULL) q.push(currNode->left);
        if(currNode->right != NULL) q.push(currNode->right);
    }
    cout << endl;
}


void Node::ConnectSameLevelNodesWithSpace(Node *node) {
    queue<Node*> q;
    q.push(node);
    q.push(NULL);
    Node *temp = NULL;

    while(!q.empty()) {
        temp = q.front();
        q.pop();

        if(temp != NULL) {
            temp->next = q.front();
            if(temp->left != NULL) q.push(temp->left);
            if(temp->right != NULL) q.push(temp->right);
        } else if(!q.empty()) {
            q.push(NULL);
        }
    }
}

int main() {
    Node *root = new Node(5);
    root->left = new Node(4);
    root->right = new Node(6);
    root->right->left = new Node(3);
    root->right->right = new Node(8);

    Node::ConnectSameLevelNodesWithSpace(root);
    Node::LevelOrderTraversalWithSpace(root);
    Node::LevelOrderTraversalWithSpace(root, true);
    return 0;
}