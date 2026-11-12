---
slug: two-city-scheduling
---
## Q
**LC 1029 两地调度**｜Medium

`2n` 个人，`costs[i] = [a, b]` 是飞 `a` 市或 `b` 市的费用，两市各要恰好 `n` 人。求最低总费用。

## A
**一句话。** 按 `a - b` 排序，前 `n` 个去 `a` 市，其余去 `b` 市。

```python
def two_city_sched_cost(costs):
    n = len(costs) // 2
    costs.sort(key=lambda c: c[0] - c[1])  # 越小越适合去 a
    return (sum(a for a, _ in costs[:n])
            + sum(b for _, b in costs[n:]))
```

**复杂度。** 时间 `O(n log n)`，空间 `O(1)`。

**易错点。**
- 只按 `a` 排序：忽略 `b` 的代价，`[[5,10],[1,6],[2,2],[5,6]]` 得 `19`，应为 `14`。
- 按 `a - b` 降序：方向反了，得到最大值。

**追问。**
- 为什么看差值？：先假设全去 `b`，改去 `a` 的额外成本是 `a - b`，选最小的 `n` 个。
- 三座城市呢？：没有单一差值，改用费用流或 DP。

**同模式。** LC 455 分发饼干、LC 135 分发糖果、LC 406 根据身高重建队列、LC 1005 K 次取反后最大化的数组和
