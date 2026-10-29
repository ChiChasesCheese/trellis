---
id: tlc-distinct-subsequences-5-alt
node: a.distinct-subsequences
type: qa
step: 5
---
## Q
**LC 115 不同的子序列**｜另一种解法

不填「前缀」表，改成从头往后看的自顶向下记忆化（`@cache`）怎么写？它和自底向上的表有什么区别，什么时候选哪个？

## A
**思路。** `f(i, j)` 是 `s[i:]` 的子序列里 `t[j:]` 出现的次数，答案是 `f(0, 0)`。`t` 配完（`j == n`）：剩下的 `s` 什么都不选，恰有一种。`s` 剩下的字符比 `t` 剩下的还少：配不出，`0`。否则不用 `s[i]` 是 `f(i+1, j)`，字符相等时再加上用它配 `t[j]` 的 `f(i+1, j+1)`。

```python
import sys
from functools import cache


def num_distinct_top_down(s: str, t: str) -> int:
    m, n = len(s), len(t)

    @cache
    def f(i: int, j: int) -> int:           # s[i:] 的子序列里 t[j:] 出现的次数
        if j == n:
            return 1                        # t 配完了：剩下的 s 什么都不选，恰好一种
        if m - i < n - j:
            return 0                        # s 剩下的字符不够配 t 剩下的
        ways = f(i + 1, j)                  # 不用 s[i]
        if s[i] == t[j]:
            ways += f(i + 1, j + 1)         # 用 s[i] 去配 t[j]
        return ways

    sys.setrecursionlimit(max(sys.getrecursionlimit(), m + 100))   # 递归深度可达 m
    return f(0, 0)
```

运行：`("rabbbit", "rabbit")` → `3`，`("babgbag", "bag")` → `5`，`("a", "aa")` → `0`，`("aaa", "a")` → `3`；`("ab" * 500, "ab" * 250)` 与自底向上的表结果相同。

**取舍。** 自顶向下：只算用得到的状态，思路和暴力递归一一对应（「用不用 `s[i]`」），加上剪枝（`s` 剩下的不够配）常数更小；缺点是递归深度可达 `len(s) = 1000`，要提高递归上限，再长就会栈溢出。自底向上的表：没有递归深度问题，面试里先写这个，状态含义和边界一目了然；需要回溯具体方案时也直接用它。
