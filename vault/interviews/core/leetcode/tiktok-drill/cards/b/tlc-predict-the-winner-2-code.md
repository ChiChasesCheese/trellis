---
id: tlc-predict-the-winner-2-code
node: b.predict-the-winner
type: qa
step: 2
---
## Q
**LC 486 预测赢家**｜写出 Python 实现

整数数组 `nums`（长度 `1..20`，元素 `0..10^7`）。玩家 1 先手，两人轮流从数组一端取一个数加到自己的得分，双方都使自己的分数最大。玩家 1 的分数大于等于玩家 2 就返回 `True`，否则 `False`。要求 `O(n^2)`，使用完整的二维表。

## A
**思路。** `dp[i][j]` 表示只剩 `nums[i..j]`、轮到你取时，你与对手的最大得分差。区间长度为 `1` 时就是该数本身。长度从 `2` 到 `n` 递增填表：取左端得 `nums[i] - dp[i+1][j]`，取右端得 `nums[j] - dp[i][j-1]`，取较大者。最后看 `dp[0][n-1] >= 0`。

```python
def predict_the_winner(nums: list[int]) -> bool:
    n = len(nums)
    # dp[i][j]：只剩 nums[i..j]、轮到你取时，你的得分 - 对手的得分 的最大值
    dp = [[0] * n for _ in range(n)]
    for i, x in enumerate(nums):
        dp[i][i] = x                            # 只剩一个数：只能取它
    for length in range(2, n + 1):              # 按区间长度从小到大填表
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = max(nums[i] - dp[i + 1][j], nums[j] - dp[i][j - 1])
    return dp[0][n - 1] >= 0                    # 差值 >= 0：先手不输（平局算先手赢）
```

**运行。** `[1,5,2]` → `False`；`[1,5,233,7]` → `True`；`[0]` → `True`；`[7]` → `True`；`[3,3]` → `True`；`[1,2]` → `True`。

**复杂度。** 时间 `O(n^2)`：区间个数 `n(n+1)/2`，每个 `O(1)`；空间 `O(n^2)`。

**写法要点。** `dp = [[0] * n for _ in range(n)]` 用列表推导式建表，每行是独立列表（`[[0] * n] * n` 会让所有行共用同一个列表）；`for i, x in enumerate(nums): dp[i][i] = x` 初始化对角线；外层按区间长度、内层按起点的顺序，保证 `dp[i+1][j]` 与 `dp[i][j-1]`（更短的区间）已经算好；比较用 `>= 0` 体现「平局算先手赢」。
