#include <bits/stdc++.h>
#define ll long long int
using namespace std;

void merge(int arr[], int l, int m, int r) {
    int size1 = (m + 1) - l;
    int size2 = (r + 1) - (m + 1);

    int L[size1];
    int R[size2];

    for (int i = 0; i < size1; ++i)
        L[i] = arr[l + i];

    for (int j = 0; j < size2; ++j)
        R[j] = arr[m + 1 + j];

    int i = 0, j = 0, k = l;
    while (i < size1 && j < size2)
        if (L[i] < R[j])
            arr[k++] = L[i++];
        else
            arr[k++] = R[j++];

    while (i < size1)
        arr[k++] = L[i++];

    while (j < size2)
        arr[k++] = L[j++];

}

void mergeSort(int arr[], int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}

void printArray(int arr[], int n) {
    for (int i = 0; i < n; ++i)
        cout << arr[i] << ' ';
    cout << endl;
}

int main() {
    int n;
    cin >> n;
    int arr[n];
    for (int i = 0; i < n; ++i)
        cin >> arr[i];
    mergeSort(arr, 0, n - 1);
    printArray(arr, n);
    return 0;
}