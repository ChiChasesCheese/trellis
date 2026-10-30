---
id: tlc-regular-expression-matching-2-code
node: p3.regular-expression-matching
type: qa
step: 2
---
## Q
**LC 10 正则表达式匹配**｜写出 Python 实现

字符串 `s`（长度 `1..20`，小写字母）和模式 `p`（长度 `1..20`，小写字母、`'.'`、`'*'`，每个 `'*'` 前都有有效字符）。`'.'` 匹配任意单个字符，`'*'` 匹配零个或多个前面的元素，要求匹配整个 `s`。写 `is_match(s, p)`。

## A
**思路。** `match(i, j)` 表示 `s[i:]` 能否被 `p[j:]` 完整匹配，用 `functools.cache` 缓存。看 `p[j+1]` 是不是 `'*'`：是就「跳过 `x*`」或「首字符匹配后留在 `j` 吃下一个」；不是就首字符匹配后两边一起前进。

```python
from functools import cache


def is_match(s: str, p: str) -> bool:
    @cache
    def match(i: int, j: int) -> bool:      # s[i:] 能否被 p[j:] 整个匹配
        if j == len(p):
            return i == len(s)
        first = i < len(s) and p[j] in (s[i], '.')   # 当前字符能否匹配 p[j]
        if j + 1 < len(p) and p[j + 1] == '*':
            # 星号两条路：匹配零次（跳过 "x*"），或匹配一次后留在原位继续
            return match(i, j + 2) or (first and match(i + 1, j))
        return first and match(i + 1, j + 1)

    return match(0, 0)
```

运行：`("aa", "a")` → `False`，`("aa", "a*")` → `True`，`("ab", ".*")` → `True`，`("aab", "c*a*b")` → `True`，`("mississippi", "mis*is*p*.")` → `False`，`("aaa", "a*a")` → `True`，`("a", "ab*")` → `True`，`("ab", ".*c")` → `False`。

**复杂度。** 时间 `O(mn)`：状态 `(i, j)` 至多 `(m+1)(n+1)` 个，每个常数次转移；空间 `O(mn)`：缓存，递归深度至多 `m + n`，远小于默认的递归上限。

**写法要点。** `@cache`（`functools.cache`，3.9+）把递归自动变成记忆化，嵌套函数能直接用外层的 `s`、`p`，缓存键只剩 `(i, j)`。`p[j] in (s[i], '.')` 一次覆盖「字符相同」和「通配符」。`first and match(...)` 利用短路：`first` 为假就不再递归。星号分支先试「零次」再试「吃一个」，顺序不影响正确性，只影响速度。
