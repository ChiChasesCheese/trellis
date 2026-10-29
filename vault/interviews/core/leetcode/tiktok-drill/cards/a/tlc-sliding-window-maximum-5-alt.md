---
id: tlc-sliding-window-maximum-5-alt
node: a.sliding-window-maximum
type: qa
step: 5
---
## Q
**LC 239 滑动窗口最大值**｜另一种解法

单调队列之外，滑动窗口最大值还有哪些做法？各自的复杂度和适用场景是什么？

## A
**解法二：分块 + 前后缀最大值（不需要队列）。** 把数组按每 `k` 个切成一块。任何长度为 `k` 的窗口 `[i, i + k - 1]` 要么恰好是一整块，要么由「某块的后缀」和「下一块的前缀」拼成。所以预处理每块内的前缀最大值 `left` 和后缀最大值 `right`，窗口最大值就是 `max(right[i], left[i + k - 1])`。

```python
def max_sliding_window_blocks(nums: list[int], k: int) -> list[int]:
    n = len(nums)
    left, right = nums[:], nums[:]     # 把数组按 k 个一块切开
    for i in range(1, n):
        if i % k:                      # 块内前缀最大值
            left[i] = max(left[i - 1], nums[i])
    for i in range(n - 2, -1, -1):
        if (i + 1) % k:                # 块内后缀最大值
            right[i] = max(right[i + 1], nums[i])
    # 任何长为 k 的窗口 [i, i+k-1] 恰好由一个块的后缀和下一个块的前缀拼成
    return [max(right[i], left[i + k - 1]) for i in range(n - k + 1)]
```

时间 `O(n)`，空间 `O(n)`，全是顺序数组扫描，常数小，也容易并行；缺点是窗口大小必须固定，且不能增量处理流数据。

**解法三：最大堆 + 惰性删除。** 堆里放 `(-值, 下标)`，每步堆顶若已滑出窗口就弹出，直到堆顶在窗口内。

```python
def max_sliding_window_heap(nums: list[int], k: int) -> list[int]:
    heap: list[tuple[int, int]] = []   # (-值, 下标) 的最大堆
    ans: list[int] = []
    for i, x in enumerate(nums):
        heapq.heappush(heap, (-x, i))
        while heap[0][1] <= i - k:     # 惰性删除：堆顶已滑出窗口才弹出
            heapq.heappop(heap)
        if i >= k - 1:
            ans.append(-heap[0][0])
    return ans
```

时间 `O(n log n)`（堆里最多 `n` 个元素，弹出的总数 `≤ n`），空间 `O(n)`。写法最直观，不需要想单调性。

**怎么选。** 面试里先说暴力 `O(nk)`，再说堆 `O(n log n)`，最后给单调队列 `O(n)`——这是最标准的答案；追问「不用队列怎么做」时给分块前后缀；窗口大小可变或需要处理流时，只有单调队列和堆适用。
