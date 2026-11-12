---
slug: regular-expression-matching
---
## Q
**LC 10 正则表达式匹配**｜Hard

实现支持 `.`（任意单个字符）和 `*`（前一个元素重复零次或多次）的正则匹配，要匹配整个 `s`。

## A
**一句话。** 记忆化递归：`match(i, j)` 判断 `s[i:]` 能否匹配 `p[j:]`，遇 `x*` 分「匹配零次」和「再吃一个」两路。

```python
def is_match(s, p):
    @cache
    def match(i, j):              # s[i:] 能否被 p[j:] 整个匹配
        if j == len(p):
            return i == len(s)
        first = i < len(s) and p[j] in (s[i], '.')
        if j + 1 < len(p) and p[j + 1] == '*':
            # 零次：跳过 "x*"；多一次：吃掉 s[i]，p 不动
            return (match(i, j + 2)
                    or (first and match(i + 1, j)))
        return first and match(i + 1, j + 1)

    return match(0, 0)
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 把 `*` 当贪心吃光：`s="aa"`、`p="a*a"` 得 `False`，应为 `True`。
- 漏掉「零次」分支：`s="aab"`、`p="c*a*b"` 的 `c*` 必须匹配零次。
- `i` 越界时直接取 `s[i]`：先判 `i < len(s)`，`("", "a*")` 仍要走跳过分支得 `True`。

**追问。**
- 自底向上怎么写？：`f[i][j]` 倒着填，只依赖 `f[i][j+2]`、`f[i+1][j]`、`f[i+1][j+1]`，可滚动成 `O(n)` 空间。
- 通配符匹配（LC 44）有何不同？：`*` 匹配任意序列、不依赖前一个元素，可用双指针加回溯点。

**同模式。** LC 44 通配符匹配、LC 72 编辑距离、LC 97 交错字符串、LC 115 不同的子序列
