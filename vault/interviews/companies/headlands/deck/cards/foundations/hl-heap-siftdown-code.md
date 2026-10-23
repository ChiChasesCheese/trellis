---
id: hl-heap-siftdown-code
node: foundations.heap-priority-queue
type: qa
step: 11
---
## Q
写出 `int[]` 小根堆的 `siftDown(int[] a, int size, int i)`。

## A
```java
static void siftDown(int[] a, int size, int i) {
    while (true) {
        int l = 2 * i + 1, r = l + 1, smallest = i;
        if (l < size && a[l] < a[smallest]) smallest = l;
        if (r < size && a[r] < a[smallest]) smallest = r;
        if (smallest == i) break;
        int t = a[i]; a[i] = a[smallest]; a[smallest] = t;
        i = smallest;
    }
}
```
要点：先检查 `l < size`、`r < size` 再读元素，避免越界；`smallest` 先从自己出发，依次与两个孩子比，取三者最小；`smallest == i` 说明堆序成立，停。最多下沉到叶子，O(log n)。
