---
id: tlc-flip-string-to-monotone-increasing-4-followup
node: p4.flip-string-to-monotone-increasing
type: qa
step: 4
---
## Q
**LC 926 将字符串翻转到单调递增**｜追问

面试官接着问：（1）怎么用前缀和讲清楚「分界点」这个想法？（2）要返回最终的字符串，而不只是次数；（3）字符串是一个很长的输入流，不能存下来。

## A
1. **前缀和写法**：枚举分界点 `k`，左边 `s[:k]` 要全为 `0`，代价是其中 `1` 的个数；右边要全为 `1`，代价是其中 `0` 的个数，`O(n)`。

```python
from itertools import accumulate


def min_flips_prefix(s: str) -> int:
    n = len(s)
    ones = list(accumulate((c == "1" for c in s), initial=0))   # ones[k]：s[:k] 里 1 的个数
    return min(ones[k] + (n - k) - (ones[n] - ones[k]) for k in range(n + 1))
```

`"00110"` → `1`，`"010110"` → `2`，`"00011000"` → `2`。
2. **返回字符串**：用上面的式子取得最优的 `k`（`min(range(n + 1), key=...)`），结果就是 `"0" * k + "1" * (n - k)`。同一个最小值可能有多个 `k`，任选一个都对。
3. **流式输入**：`ones` 与 `flips` 只依赖已读的前缀，读到每个字符就能更新，空间 `O(1)`，且每一步的 `flips` 都是「到目前为止读到的前缀」的答案。前缀和版需要知道整串长度，不适合流式。

**Python 提醒**：`accumulate(..., initial=0)` 会在最前面多产出一个 `0`，因此长度是 `n + 1`，下标恰好对应「前 `k` 个字符」；布尔值参与求和时 `True` 就是 `1`，所以不必写 `int(c == "1")`。
