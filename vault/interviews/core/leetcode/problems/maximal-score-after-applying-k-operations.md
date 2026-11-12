---
slug: maximal-score-after-applying-k-operations
---
## Q
**LC 2530 执行 K 次操作后的最大分数**｜Medium

每次操作选下标 `i`，分数加 `nums[i]`，再把 `nums[i]` 换成 `ceil(nums[i]/3)`。求恰好 `k` 次操作后的最大分数。

## A
**一句话。** 贪心加最大堆：每次取当前最大值，再把 `ceil(x/3)` 放回。

```python
def max_kelements(nums, k):
    heap = [-x for x in nums]         # 负数小根堆当最大堆
    heapify(heap)
    score = 0
    for _ in range(k):
        x = -heap[0]
        score += x
        heapreplace(heap, -((x + 2) // 3))   # 弹出再压入
    return score
```

**复杂度。** 时间 `O(n + k log n)`，空间 `O(n)`。

**易错点。**
- 先 `heappush` 再 `heappop`：弹出的可能是刚压入的值，要先弹后压或用 `heapreplace`。
- 压回时忘了取负：把最小值当成最大值。

**追问。**
- 替换规则换成 `x // 2` 呢？：只要替换后不增且单调，贪心仍成立。
- 每个下标最多操作 `m` 次？：堆元素带上操作计数，满了就不再放回。

**同模式。** LC 1962 移除石子使总数最小、LC 1046 最后一块石头的重量、LC 2208 将数组和减半的最少操作次数、LC 1167 连接棒材的最低费用
