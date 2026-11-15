---
slug: maximum-earnings-from-taxi
---
## Q
**LC 2008 出租车的最大盈利**｜Medium

出租车从地点 1 开到 `n`，只能向前。订单 `[start, end, tip]` 盈利 `end - start + tip`，同一时刻最多载一单，可在同一地点下客后马上接客。求最大盈利。

## A
**一句话。** 按地点做线性 DP：`f[i]` 是开到 `i` 时的最大盈利，要么不在 `i` 下客（`f[i-1]`），要么接一单在 `i` 下客（`f[start] + 盈利`）。

```python
def max_taxi_earnings(n, rides):
    ends = defaultdict(list)       # 在 end 下车的订单
    for s, e, t in rides:
        ends[e].append((s, e - s + t))
    f = [0] * (n + 1)              # f[i]：开到 i 的最大盈利
    for i in range(1, n + 1):
        f[i] = f[i - 1]            # 不在 i 下客
        for s, gain in ends[i]:
            f[i] = max(f[i], f[s] + gain)
    return f[n]
```

**复杂度。** 时间 `O(n + r)`，空间 `O(n + r)`。

**易错点。**
- 把订单按起点挂：`f[i]` 依赖起点处的 `f[start]`，必须在终点处转移，起点那时已算好。
- 盈利漏了距离：每单赚 `end - start + tip`，不只是小费。

**追问。**
- 地点范围到 `10^9`？：按订单终点排序，`f[k]` 表示前 `k` 单，二分找终点 `<= start` 的最后一单，就是 LC 1235。
- 最多接 `k` 单？：加一维单数，`f[i][j]`，同 LC 1751。

**同模式。** LC 435 无重叠区间、LC 1235 规划兼职工作、LC 1751 最多可以参加的会议数目 II、LC 2054 两个最好的不重叠活动
