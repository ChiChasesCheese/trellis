---
id: hl-hc11-two-arrays
node: problems.hc11-order-interval-overlap
type: qa
step: 4
---
## Q
Part 1 的两个已排序数组扫描线怎么写？如何得到最早时刻、处理空区间和非法输入？它和用堆的 Meeting Rooms II 做法比呢？

## A
开始事件只有 +1，结束事件只有 −1。所有 `start` 放一个 `long[]` 排序，所有 `end` 放另一个排序，像归并一样一起扫：

```java
static Peak peakOf(long[] starts, long[] ends, int n, boolean inclusive) {
    if (n == 0) return new Peak(0, 0);
    Arrays.sort(starts, 0, n); Arrays.sort(ends, 0, n);
    int best = 0; long bestTime = 0; int j = 0;
    for (int i = 0; i < n; i++) {
        long s = starts[i];
        while (j < n && (inclusive ? ends[j] < s : ends[j] <= s)) j++;   // 同一时刻先结束
        int live = (i + 1) - j;                                          // 已开始 − 已结束
        if (live > best) { best = live; bestTime = s; }                  // 严格 > 保留最早
    }
    return new Peak(best, bestTime);
}
```
- 「同一时刻先结束后开始」就是 `ends[j] <= s`（闭区间 `<`）；最大值只可能出现在某个 `start` 上；
- 同一个 `s` 重复时 `live` 逐个增大，严格 `>` 更新最优；
- `Arrays.sort(long[])` 是原始类型双轴快排，无装箱无比较器，100 万个区间约 80 ms；
- `Arrays.sort(a, 0, n)` 只排前 n 个；排序原地，所以 `sweep` 里用**拷贝**，不动调用者的 `long[][]`（对输入数组原地排序是误区）；
- 只比较不做减法，坐标接近 `Long.MAX_VALUE` 也安全；
- `start == end` 的空区间从没活过，直接跳过；`end < start`、`start < 0`、行长度不是 2 → `IllegalArgumentException`；`Peak(0, 0)` 表示从没有订单活着，时间域 t≥0、最大值 0 在 t=0 就达到，是自洽的真话而非哨兵。

**每个事件一个 `long[]{time, delta}`** 的版本也对（`Comparator.comparingLong(x->x[0]).thenComparingLong(x->x[1])`，−1 < +1 即 tie 规则），但 2n 个小数组缓存不友好。

**堆做法**（Meeting Rooms II）：按 start 排序，最小堆存活着订单的结束时间；新订单先 `while (heap.peek() <= s) heap.poll()` 再 `heap.add(e)`，堆大小最大值是答案，O(n log n) 同样对。选两数组因为：无堆对象开销、tie 规则一眼可见、易扩展到按方向和撤单。
