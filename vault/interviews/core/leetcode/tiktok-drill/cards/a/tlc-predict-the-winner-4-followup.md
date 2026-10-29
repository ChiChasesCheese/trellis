---
id: tlc-predict-the-winner-4-followup
node: a.predict-the-winner
type: qa
step: 4
---
## Q
**LC 486 预测赢家**｜追问

面试官接着问：（1）两人最终各得多少分？（2）数组长度为偶数时有没有 `O(1)` 的结论？（3）写成自顶向下的记忆化递归？

## A
1. **最终得分。** 总分 `S = p1 + p2`，分差 `d = p1 - p2 = dp[0][n-1]`，所以先手得分 `(S + d) // 2`，后手得分 `(S - d) // 2`。
2. **偶数个数。** 先手总能拿下全部奇数下标或全部偶数下标（这是 LC 877 的结论）：把下标按奇偶分成两类，总和较大的那类，先手每次取到的恰好都属于这一类，后手只能取到另一类。所以 `len(nums) % 2 == 0` 时先手不输，直接返回 `True`；奇数长度仍要 DP。
3. **自顶向下。** 子问题同样是区间 `[i, j]`，用 `functools.cache` 记忆化：

```python
from functools import cache


def predict_the_winner_memo(nums: list[int]) -> bool:
    @cache
    def diff(i: int, j: int) -> int:                # 区间 [i, j] 上取数者的最大分差
        if i == j:
            return nums[i]
        return max(nums[i] - diff(i + 1, j), nums[j] - diff(i, j - 1))

    return diff(0, len(nums) - 1) >= 0
```

空间可以压到 `O(n)`：见 Python 工具箱「DP 降维」。

**Python 提醒**：`@cache` 的参数必须可哈希，所以递归参数用下标 `(i, j)`，不要把 `nums` 的切片（列表）当参数；`n <= 20` 时递归深度只有 `20`，不会触到递归上限。
