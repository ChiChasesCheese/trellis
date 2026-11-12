---
slug: maximum-performance-of-a-team
---
## Q
**LC 1383 最大的团队表现值**｜Hard

`n` 名工程师有速度 `speed[i]` 和效率 `efficiency[i]`，最多选 `k` 人，表现值 = 速度之和 × 最小效率。求最大表现值，对 `10^9+7` 取余。

## A
**一句话。** 按效率从高到低枚举「最低效率的人」，用大小为 `k` 的最小堆维护已选人的最大速度和。

```python
def max_performance(n, speed, efficiency, k):
    heap, total, best = [], 0, 0
    for e, s in sorted(zip(efficiency, speed))[::-1]:
        heappush(heap, s)
        total += s
        if len(heap) > k:
            total -= heappop(heap)    # 踢掉速度最小的
        best = max(best, total * e)   # 当前 e 是团队最低效率
    return best % (10**9 + 7)
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 按效率升序遍历：最小效率不再是当前这个人，`k=2` 的示例得 `162`，应为 `60`。
- 弹出最小速度后忘了从 `total` 里减掉：速度和只增不减，同例得 `72`，应为 `60`。
- 比较时就取模：取模后的值不能比大小，最后才取模。

**追问。**
- 要恰好选 `k` 个怎么改？：堆满 `k` 个之后才更新答案。
- 怎么还原选了哪些人？：记下取得最大值时的效率阈值，再选速度最大的 `k` 个。

**同模式。** LC 2542 最大子序列的分数、LC 857 雇佣 K 名工人的最低成本、LC 502 IPO、LC 215 数组中的第K个最大元素
