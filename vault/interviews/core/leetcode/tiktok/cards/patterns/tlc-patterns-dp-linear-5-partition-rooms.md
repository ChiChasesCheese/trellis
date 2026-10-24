---
id: tlc-patterns-dp-linear-5-partition-rooms
node: patterns.dp-linear
type: qa
step: 5
---
## Q
**动态规划：线性与状态机｜分段与递推：分隔数组得到最大和（LC 1043）、访问完所有房间的第一天（LC 1997）**

"把数组切成长度不超过 `k` 的段"的 DP 状态怎么设？房间那题为什么 `dp[i] = 2·dp[i-1] − dp[next[i-1]] + 2`？

## A
**LC 1043**：`dp[i]` = 前 `i` 个元素分段后的最大和。枚举**最后一段**的长度 `j`（`1..k`），这一段的值全变成段内最大值：

```python
def max_sum_after_partitioning(arr: list[int], k: int) -> int:
    n = len(arr)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        mx = 0
        for j in range(1, min(k, i) + 1):  # 最后一段是 arr[i-j : i]
            mx = max(mx, arr[i - j])       # 向左延长一格，顺便维护段内最大值
            dp[i] = max(dp[i], dp[i - j] + mx * j)
    return dp[n]
```

运行：`([1,15,7,9,2,5,10], 3)` → `84`；`([1,4,1,5,7,3,6,1,9,9,3], 4)` → `83`；`([1], 1)` → `1`。时间 `O(nk)`，`n <= 500` 轻松通过。

**LC 1997**：`dp[i]` = 第一次到达房间 `i` 的日期。第一次到 `i-1` 时它被访问了 1 次（奇数），第二天回到 `next[i-1]`；要再次走到 `i-1`（偶数次访问）需要把 `next[i-1]` 到 `i-1` 之间的房间重新走一遍，相当于 `dp[i-1] − dp[next[i-1]]` 天；再加 2 天（回退一天、前进一天）。所以

```python
def first_day_been_in_all_rooms(next_visit: list[int]) -> int:
    mod = 10**9 + 7
    dp = [0] * len(next_visit)
    for i in range(1, len(next_visit)):
        dp[i] = (2 * dp[i - 1] - dp[next_visit[i - 1]] + 2) % mod
    return dp[-1]
print(first_day_been_in_all_rooms([0, 0]), first_day_been_in_all_rooms([0, 0, 2]), first_day_been_in_all_rooms([0, 1, 2, 0]))   # 2 6 6
```

- 取模后 `2·dp[i-1] − dp[...]` 可能为负，Python 的 `%` 自动得到非负结果，不用补 `+ mod`。
- `n = 10^5`、`nextVisit` 全 `0` 时，线性递推瞬间完成；直接模拟则需要指数级天数。
- 推递推式的方法：先画出前三四个房间的时间线，找出"第一次到 `i`"之前发生的固定模式。
