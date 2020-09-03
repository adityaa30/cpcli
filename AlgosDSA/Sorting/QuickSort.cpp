#include <iostream>

void Swap(int *x, int *y) {
    int temp = *y;
    *y = *x;
    *x = temp;
}

int PartitionQ(int *arr, int l, int r) {
    // arr[r] is the pivot here (rightmost)
    int i = l - 1;
    for(int j = l; j <= r - 1; ++j)
        if(arr[j] <= arr[r])
            Swap(&arr[++i], &arr[j]);
    Swap(&arr[++i], &arr[r]);
    return i;
}

void QuickSort(int *arr, int n, int l, int r) {
    if(l < r) {
        int p = PartitionQ(arr, l, r);
        QuickSort(arr, n, l, p - 1);
        QuickSort(arr, n, p + 1, r);
    }
}

int main() {
    int n = 5, arr[n] = {10, 9, 8, 7, 6};
    QuickSort(arr, n, 0, n - 1);
    for(int i = 0; i < n; ++i) printf("%d ", arr[i]);
    return 0;
}