---
id: tlc-partition-array-for-maximum-sum-2-code
node: p4.partition-array-for-maximum-sum
type: qa
step: 2
---
## Q
**LC 1043 分隔数组以得到最大和**｜写出 Python 实现

整数数组 `arr`（长度 `1..500`，`0 <= arr[i] <= 10^9`）和整数 `k`（`1..arr.length`）。把 `arr` 切成若干连续段，每段长度不超过 `k`，每段内的数都改成该段最大值，返回改后数组的最大和。

## A
**思路。** `dp[i]` 表示前 `i` 个元素分隔变换后的最大和，`dp[0] = 0`。对每个 `i`，枚举最后一段的长度 `length`（`1..min(k, i)`），这一段是 `arr[i-length : i]`，它的值是 `length × 段内最大值`；从 `length = 1` 往上走时，段最大值只需和新纳入的 `arr[i - length]` 取一次 `max`。取所有选择中的最大者，答案是 `dp[n]`。

```python
def max_sum_after_partitioning(arr: list[int], k: int) -> int:
    n = len(arr)
    dp = [0] * (n + 1)                  # dp[i]：前 i 个元素分隔后的最大和
    for i in range(1, n + 1):
        seg_max = 0
        for length in range(1, min(k, i) + 1):    # 枚举最后一段的长度
            seg_max = max(seg_max, arr[i - length])   # 滚动维护这一段的最大值
            dp[i] = max(dp[i], dp[i - length] + seg_max * length)
    return dp[n]
```

运行：`arr=[1,15,7,9,2,5,10], k=3` → `84`，`arr=[1,4,1,5,7,3,6,1,9,9,3], k=4` → `83`，`arr=[1], k=1` → `1`，`arr=[0,0,0], k=2` → `0`，`arr=[10**9]*500, k=500` → `500000000000`。

**复杂度。** 时间 `O(n·k)`：`n` 个状态，每个状态枚举最后一段的长度至多 `k` 种，滚动最大值使每次转移 `O(1)`；`n = k = 500` 时约 `1.25·10^5` 次转移。空间 `O(n)`。

**写法要点。** `min(k, i)` 同时处理「前缀不足 `k` 个」的边界；`seg_max = max(seg_max, arr[i - length])` 让段最大值滚动更新，避免对切片反复调用 `max`（后者是 `O(n·k^2)`）；`dp[i] = max(dp[i], ...)` 原地累积比较，`dp` 用 `0` 初始化是因为 `arr[i] >= 0`；`dp = [0] * (n + 1)` 多留一位表示空前缀，免去 `i == 0` 的特判。
