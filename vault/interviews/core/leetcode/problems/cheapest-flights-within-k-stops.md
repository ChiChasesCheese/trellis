---
slug: cheapest-flights-within-k-stops
---
## Q
**LC 787 K 站中转内最便宜的航班**｜Medium

`flights[i] = [from, to, price]`。求从 `src` 到 `dst` 最多中转 `k` 站的最低价格，没有则返回 `-1`。

## A
**一句话。** 最多 `k` 站中转即最多 `k+1` 趟航班，做 Bellman-Ford 的分轮 DP：`dp[t][v]` 是最多坐 `t` 趟到 `v` 的最小价格。

```python
def find_cheapest_price(n, flights, src, dst, k):
    INF = float("inf")
    dp = [[INF] * n for _ in range(k + 2)]
    dp[0][src] = 0
    for t in range(1, k + 2):
        dp[t] = dp[t - 1][:]         # 少坐一趟也算
        for u, v, w in flights:
            if dp[t - 1][u] + w < dp[t][v]:  # 只读上一行
                dp[t][v] = dp[t - 1][u] + w
    ans = dp[k + 1][dst]
    return -1 if ans == INF else ans
```

**复杂度。** 时间 `O(kE)`，空间 `O(kn)`。

**易错点。**
- 转移读本行 `dp[t][u]`：一轮可连坐多趟，`[[0,1,100],[1,2,100],[0,2,500]]`、`k=0` 得 `200`，应为 `500`。
- 只开 `k+1` 行：`k` 站中转是 `k+1` 趟，要 `k+2` 行，否则 `k=0` 的直达漏掉。
- 新行不复制上一行：变成「恰好 `t` 趟」，`[[0,1,100],[1,2,100],[0,2,150]]`、`k=1` 得 `200`，应为 `150`。

**追问。**
- 空间压到 `O(n)`？：滚动数组，但每轮必须拷贝上一轮再更新，原地更新会一轮坐多趟。
- 为什么普通 Dijkstra 不行？：最便宜的路线可能用掉太多趟，状态必须带上趟数。

**同模式。** LC 743 网络延迟时间、LC 1631 最小体力消耗路径、LC 1928 规定时间内到达终点的最小花费
