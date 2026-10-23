---
id: hl-heap-siftup-code
node: foundations.heap-priority-queue
type: qa
step: 8
---
## Q
写出 `int[]` 小根堆的 `siftUp(int[] a, int i)`。随机顺序插入 10⁶ 个数平均交换多少次，什么顺序才是最坏？

## A
```java
static void siftUp(int[] a, int i) {
    while (i > 0) {
        int parent = (i - 1) / 2;
        if (a[parent] <= a[i]) break;
        int t = a[parent]; a[parent] = a[i]; a[i] = t;
        i = parent;
    }
}
```
最坏插入 O(log n)：新元素是全局最小，一路换到根；**递减序列**每次都换到根。随机顺序插入时新元素大概率偏大，很快停下：n = 10⁶ 次插入总共只交换 1,280,829 次，平均 **1.28 次**，随机数据下插入平均 O(1)。
