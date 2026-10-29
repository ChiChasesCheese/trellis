---
id: tlc-regular-expression-matching-5-alt
node: a.regular-expression-matching
type: qa
step: 5
---
## Q
**LC 10 正则表达式匹配**｜另一种解法

不用递归缓存，改成自底向上的二维表怎么写？什么时候选表、什么时候选记忆化递归？

## A
**自底向上。** `f[i][j]` 表示 `s[i:]` 能否被 `p[j:]` 匹配，从后往前填：`f[m][n] = True`（两边都空）；`i` 从 `m` 到 `0`，`j` 从 `n-1` 到 `0`，转移和递归版完全一致。

```python
def is_match_table(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    f = [[False] * (n + 1) for _ in range(m + 1)]
    f[m][n] = True                              # 两边都空：匹配
    for i in range(m, -1, -1):
        for j in range(n - 1, -1, -1):
            first = i < m and p[j] in (s[i], '.')
            if j + 1 < n and p[j + 1] == '*':
                f[i][j] = f[i][j + 2] or (first and f[i + 1][j])
            else:
                f[i][j] = first and f[i + 1][j + 1]
    return f[0][0]
```

输出与记忆化版完全一致：`("aa", "a")` → `False`，`("aa", "a*")` → `True`，`("ab", ".*")` → `True`，`("aab", "c*a*b")` → `True`，`("mississippi", "mis*is*p*.")` → `False`。

**取舍。**
- 表：没有递归，没有深度限制；可以滚动数组把空间压到 `O(n)`；但会算出所有 `(m+1)(n+1)` 个状态，包括永远用不到的。
- 记忆化递归：只算从 `(0, 0)` 能到达的状态，代码更短、更贴近状态定义，面试里更不容易写错；代价是递归深度（这里 `<= m + n`，对 `20` 毫无压力）。
- 约束 `m, n <= 20` 时两者没有速度差别。题目规模上去（比如 `10^4`）就必须用表加滚动数组，或者转 NFA。

先写记忆化递归（思路直接、改动小），被问「去掉递归」时再给表。
