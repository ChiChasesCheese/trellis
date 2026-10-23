---
id: hl-heap-kth-largest-code
node: foundations.heap-priority-queue
type: qa
step: 19
---
## Q
写一个函数返回数组中第 k 大的元素（1 ≤ k ≤ n），复杂度 O(n log k)。

## A
```java
static int kthLargest(int[] a, int k) {
    PriorityQueue<Integer> heap = new PriorityQueue<>(k); // 小根堆，保存最大的 k 个
    for (int x : a) {
        if (heap.size() < k) heap.add(x);
        else if (x > heap.peek()) { heap.poll(); heap.add(x); }
    }
    return heap.peek();   // 这 k 个里最小的就是第 k 大
}
```
例：`{3,2,1,5,6,4}`，k = 2 返回 5。时间 O(n log k)，空间 O(k)。`stream().sorted().limit(k)` 是 O(n log n)，n 很大 k 很小时不如手写堆。
