---
slug: plates-between-candles
---
## Q
**LC 2055 蜡烛之间的盘子**｜Medium

只含 `*`（盘子）和 `|`（蜡烛）的串，每个查询 `[l, r]` 问子串里两侧都有蜡烛的盘子数。`n`、查询数到 `10^5`。

## A
**一句话。** 答案只看区间内最左和最右的蜡烛：预处理每个位置右侧最近蜡烛、左侧最近蜡烛和盘子前缀和，查询 `O(1)`。

```python
def plates_between_candles(s, queries):
    n = len(s)
    pre = [0] * (n + 1)          # 盘子前缀和
    left = [-1] * n              # i 及左边最近的蜡烛
    right = [n] * n              # i 及右边最近的蜡烛
    for i, ch in enumerate(s):
        pre[i + 1] = pre[i] + (ch == '*')
        if ch == '|':
            left[i] = i
        elif i:
            left[i] = left[i - 1]
    for i in range(n - 1, -1, -1):
        if s[i] == '|':
            right[i] = i
        elif i + 1 < n:
            right[i] = right[i + 1]
    ans = []
    for l, r in queries:
        a, b = right[l], left[r]     # 区间内最外两根蜡烛
        ans.append(pre[b] - pre[a] if a < b else 0)
    return ans
```

**复杂度。** 时间 `O(n + q)`，空间 `O(n)`。

**易错点。**
- 用 `left[l]`、`right[r]`：那是区间外的蜡烛，要反过来取 `right[l]`、`left[r]`。
- 区间内少于两根蜡烛没处理：`a >= b` 时答案是 `0`。

**追问。**
- 只用一个数组？：记录所有蜡烛下标，查询时二分找区间内第一根和最后一根，`O(log n)`。
- 为什么 `pre[b] - pre[a]`？：`a`、`b` 都是蜡烛，前缀和之差正好是两者之间的盘子数。

**同模式。** LC 303 区域和检索 - 数组不可变、LC 238 除了自身以外数组的乘积、LC 42 接雨水
