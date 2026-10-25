---
id: tlc-triangle-2-code
node: b.triangle
type: qa
step: 2
---
## Q
**LC 120 三角形最小路径和**｜写出 Python 实现

三角形 `triangle` 有 `1` 到 `200` 行，第 `i` 行有 `i + 1` 个数，值在 `[-10^4, 10^4]`。每一步从第 `i` 列走到下一行的第 `i` 列或第 `i + 1` 列。返回自顶向下的最小路径和，额外空间 `O(n)`，不修改输入。

## A
**思路。** 从最后一行开始，`dp` 先指向最后一行。往上一行时，新的 `dp[j] = row[j] + min(dp[j], dp[j + 1])`（用旧 `dp`），也就是该格加上它下方两个相邻格中较小的一个。用 `pairwise(dp)` 一次产出所有相邻对，和当前行 `zip` 起来；合并到顶行后 `dp[0]` 就是答案。

```python
from itertools import pairwise

def minimum_total(triangle: list[list[int]]) -> int:
    dp = triangle[-1]                      # 从最底行开始；下面每轮新建列表，不会改动输入
    for row in reversed(triangle[:-1]):    # 自底向上，一行一行往上合并
        dp = [v + min(pair) for v, pair in zip(row, pairwise(dp))]
    return dp[0]
```

运行：`[[2],[3,4],[6,5,7],[4,1,8,3]]` → `11`，`[[-10]]` → `-10`；`200` 行的随机三角形约 `0.001` 秒；`200` 行全是 `-10^4` → `-2000000`；调用之后 `triangle` 没有变化。

**复杂度。** 时间 `O(n^2)`（格子总数）；空间 `O(n)`。

**写法要点。** `dp` 先指向最后一行，只读不写；`reversed(triangle[:-1])` 从倒数第二行往上遍历；`pairwise(dp)` 给出 `(dp[0], dp[1])`、`(dp[1], dp[2])`…，长度比 `dp` 少一，恰好与上一行的长度对齐，省掉下标运算；`min(pair)` 对二元组取最小值；每轮用推导式新建列表 `dp`，旧列表丢弃，所以既不改动输入，也不会出现"边读边写同一个数组"的问题。`itertools.pairwise` 需要 Python 3.10 及以上。
