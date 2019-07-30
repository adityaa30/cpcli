#include <iostream>

template <typename T>
void Swap(T x, T y) {
    T temp = x;
    x = y;
    y = temp;
}

void Merge(int *arr, int n, int l, int m, int r) {
    int Size1 = m - l + 1, Size2 = r - m;

    int Arr1[Size1], Arr2[Size2];
    for(int i = 0; i < Size1; ++i) Arr1[i] = arr[i + l];
    for(int i = 0; i < Size2; ++i) Arr2[i] = arr[i + m + 1];

    int i = 0, j = 0, k = l;
    while(i < Size1 && j < Size2) {
        if(Arr1[i] > Arr2[j]) arr[k++] = Arr2[j++];
        else arr[k++] = Arr1[i++];
    }

    while(i < Size1) arr[k++] = Arr1[i++];
    while(j < Size2) arr[k++] = Arr2[i++];
}

void MergeSort(int *arr, int n, int l, int r) {
    if(l < r) {
        int m = l + (r - l) / 2;
        MergeSort(arr, n, l, m);
        MergeSort(arr, n, m + 1, r);
        Merge(arr, n, l, m, r);
    }
}

int main() {
    int arr[4] = {10, 5, 6, 5}, n = 4;
    MergeSort(arr, 4, 0, 4 - 1);
    for(int i = 0; i < n; ++i) printf("%d ", *(arr + i));
    printf("\n");
    return 0;
}