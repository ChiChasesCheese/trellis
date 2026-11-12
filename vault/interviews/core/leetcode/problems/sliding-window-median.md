---
slug: sliding-window-median
---
## Q
**LC 480 滑动窗口中位数**｜Hard

长度为 `k` 的窗口在数组 `nums` 上每次右移一位，返回每个窗口的中位数（`k` 为偶数取中间两数平均）。

## A
**一句话。** 对顶堆（大顶堆存较小一半、小顶堆存较大一半）加延迟删除：滑出的元素先记账，浮到堆顶再弹。

```python
def median_sliding_window(nums, k):
    small = [-x for x in nums[:k]]    # 大顶堆（存相反数）
    heapify(small)
    large = []                        # 小顶堆
    for _ in range(k // 2):
        heappush(large, -heappop(small))
    delayed = Counter()               # 值 -> 还欠删几次
    def mid():
        if k % 2:
            return float(-small[0])
        return (-small[0] + large[0]) / 2
    res = [mid()]
    for out, new in zip(nums, nums[k:]):
        delayed[out] += 1
        bal = -1 if out <= -small[0] else 1
        if new <= -small[0]:
            heappush(small, -new)
            bal += 1
        else:
            heappush(large, new)
            bal -= 1
        if bal < 0:                   # small 少一个：从 large 补
            heappush(small, -heappop(large))
        elif bal > 0:
            heappush(large, -heappop(small))
        while small and delayed[-small[0]]:
            delayed[-small[0]] -= 1
            heappop(small)
        while large and delayed[large[0]]:
            delayed[large[0]] -= 1
            heappop(large)
        res.append(mid())
    return res
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 只清一个堆的堆顶：两个堆顶都参与中位数，`[2,1,3]`、`k = 2` 会得 `[1.5, 1.5]`，应为 `[1.5, 2.0]`。
- 判断滑出元素在哪个堆写成 `out < -small[0]`：相等时被误判进 `large`，计数失衡。
- 偶数窗口用 `//` 求平均：`[1,4,2,3]`、`k = 4` 得 `2`，应为 `2.5`。

**追问。**
- 为什么不直接从堆里删？：堆删任意元素要 `O(k)`，延迟删除把它摊到 `O(log n)`。
- 更短的写法？：`sortedcontainers.SortedList` 增删后按下标取中位数，`O(n log k)`。

**同模式。** LC 295 数据流的中位数、LC 239 滑动窗口最大值、LC 1825 求出 MK 平均值
