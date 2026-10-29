---
id: tlc-sliding-window-median-2-code
node: b.sliding-window-median
type: qa
step: 2
---
## Q
**LC 480 滑动窗口中位数**｜写出 Python 实现

长度为 `k` 的窗口在 `nums`（`1 <= k <= nums.length <= 10^5`，32 位整数）上逐位右移，返回每个窗口的中位数（偶数个时取中间两数平均），要求 `O(n log n)`。

## A
**思路。** `small` 是大顶堆（存相反数）放较小的一半，`large` 是小顶堆放较大的一半，有效元素个数 `small` 比 `large` 多 0 或 1 个。每步滑出 `out`、滑入 `new`：`out` 记进 `delayed`，并按它属于哪个堆记一笔 `balance`；`new` 按与 `small` 堆顶的大小入堆。`balance` 非 0 就从多的一侧挪一个堆顶过去。最后把两个堆顶上的过期元素弹掉，读中位数。

```python
from collections import Counter
from heapq import heapify, heappop, heappush


def median_sliding_window(nums: list[int], k: int) -> list[float]:
    small = [-x for x in nums[:k]]          # 大顶堆（存相反数）：窗口里较小的一半
    heapify(small)
    large: list[int] = []                   # 小顶堆：窗口里较大的一半
    for _ in range(k // 2):                 # 有效元素个数：small 比 large 多 0 或 1 个
        heappush(large, -heappop(small))
    delayed: Counter[int] = Counter()       # 延迟删除：值 -> 还欠删几次

    def mid() -> float:
        return float(-small[0]) if k % 2 else (-small[0] + large[0]) / 2

    res = [mid()]
    for out, new in zip(nums, nums[k:]):    # out 滑出窗口，new 滑入窗口
        delayed[out] += 1
        balance = -1 if out <= -small[0] else 1     # 「small 有效数 − large 有效数」的变化
        if new <= -small[0]:
            heappush(small, -new)
            balance += 1
        else:
            heappush(large, new)
            balance -= 1
        if balance < 0:                     # small 少了一个：从 large 补
            heappush(small, -heappop(large))
        elif balance > 0:                   # large 少了一个：从 small 补
            heappush(large, -heappop(small))
        while small and delayed[-small[0]]:  # 堆顶若是待删元素，现在真正弹掉
            delayed[-small[0]] -= 1
            heappop(small)
        while large and delayed[large[0]]:
            delayed[large[0]] -= 1
            heappop(large)
        res.append(mid())
    return res
```

运行：`[1,3,-1,-3,5,3,6,7], k=3` → `[1.0, -1.0, -1.0, 3.0, 5.0, 6.0]`，同一数组 `k=2` → `[2.0, 1.0, -2.0, 1.0, 4.0, 4.5, 6.5]`，`[1,2,3,4,2,3,1,4,2], k=3` → `[2.0, 3.0, 3.0, 3.0, 2.0, 3.0, 2.0]`，`[1,4,2,3], k=4` → `[2.5]`，`[5], k=1` → `[5.0]`。

**复杂度。** 时间 `O(n log n)`，每个元素入堆出堆常数次；空间 `O(n)`，过期元素最坏会一直埋在堆里。

**写法要点。** `heapq` 只有小顶堆，大顶堆存相反数；`zip(nums, nums[k:])` 一次拿到「滑出、滑入」两个值，不用算下标；`Counter` 的缺失键读出 `0`，`while delayed[top]` 不必先判断键是否存在；`balance` 只可能是 `-2、0、2`，挪一次就平衡。
