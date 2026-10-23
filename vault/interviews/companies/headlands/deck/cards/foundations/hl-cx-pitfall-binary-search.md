---
id: hl-cx-pitfall-binary-search
node: foundations.complexity
type: qa
step: 38
---
## Q
补全并写出整数数组上的二分查找 `binarySearch(int[] sorted, int target)`，找不到返回 -1。

## A
```java
static int binarySearch(int[] sorted, int target) {
    int lo = 0, hi = sorted.length - 1;
    while (lo <= hi) {
        int mid = (lo + hi) >>> 1;
        if (sorted[mid] == target) return mid;
        if (sorted[mid] < target) lo = mid + 1; else hi = mid - 1;
    }
    return -1;
}
```
要点：区间是闭区间 `[lo, hi]`，循环条件 `lo <= hi`；每次丢一半，O(log n)；中点用 `>>> 1` 避免加法溢出；移动边界时必须 `mid ± 1`，否则可能死循环。
