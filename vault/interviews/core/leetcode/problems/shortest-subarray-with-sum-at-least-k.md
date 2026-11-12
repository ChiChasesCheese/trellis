---
slug: shortest-subarray-with-sum-at-least-k
---
## Q
**LC 862 和至少为 K 的最短子数组**｜Hard

整数数组 `nums`（含负数）和整数 `k`，求和至少为 `k` 的最短非空子数组的长度，不存在返回 `-1`。

## A
**一句话。** 前缀和加单调递增双端队列：队首满足 `>= k` 就弹出并更新答案，队尾不小于当前值的起点作废。

```python
def shortest_subarray(nums, k):
    n = len(nums)
    pre = [0, *accumulate(nums)]   # 区间和 = pre[j]-pre[i]
    dq = deque()                   # 下标，前缀和严格递增
    best = n + 1
    for j, cur in enumerate(pre):
        while dq and cur - pre[dq[0]] >= k:
            best = min(best, j - dq.popleft())  # 再往后只会更长
        while dq and pre[dq[-1]] >= cur:
            dq.pop()               # 起点更晚且前缀和更小，更优
        dq.append(j)
    return best if best <= n else -1
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 前缀数组不从 `0` 开始：漏掉以首元素开头的子数组，`[5]`、`k=5` 得 `-1`。
- 队首弹出写成 `if`：`[4,8]`、`k=6` 在 `j=2` 要连弹两个才得 `1`。
- 漏掉队尾弹出：`[-4,6]`、`k=6` 因被较小下标挡住而得 `-1`。

**追问。**
- 全是正数呢？：窗口和单调，退化成双指针（LC 209）；有负数才需要单调队列。
- 为什么出队后不再用？：之后的 `j` 只会让这个起点的子数组更长，不可能更短。

**同模式。** LC 209 长度最小的子数组、LC 239 滑动窗口最大值、LC 1425 带限制的子序列和、LC 1438 绝对差不超过限制的最长连续子数组
