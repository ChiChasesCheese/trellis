---
id: tlc-wildcard-matching-5-alt
node: b.wildcard-matching
type: qa
step: 5
---
## Q
**LC 44 通配符匹配**｜另一种解法

不建 DP 表，只用双指针怎么做通配符匹配？为什么只需要回溯到最近的一个 `*`？它和 DP 相比什么时候选哪个？

## A
**思路。** 双指针 `i`（`s`）、`j`（`p`）同时前进。遇到 `*` 时记下回溯点（`star` 是它在 `p` 中的位置，`mark` 是它当前匹配到 `s` 的位置），先让它匹配空串。之后一旦失配，就回到最近的 `*`，让它多吞一个字符再继续。

```python
def is_match_greedy(s: str, p: str) -> bool:
    i = j = 0
    star = mark = -1                       # star：最近一个 '*' 在 p 中的位置；mark：它已吞到 s 的哪里
    while i < len(s):
        if j < len(p) and p[j] in ("?", s[i]):
            i += 1
            j += 1
        elif j < len(p) and p[j] == "*":
            star, mark = j, i              # 先让 '*' 匹配空串，记住回溯点
            j += 1
        elif star != -1:                   # 失配：回到最近的 '*'，让它多吞一个字符
            mark += 1
            i, j = mark, star + 1
        else:
            return False
    return all(ch == "*" for ch in p[j:])  # s 用完后，p 剩下的必须全是 '*'
```

运行：`("aa", "a")` → `False`，`("aa", "*")` → `True`，`("cb", "?a")` → `False`，`("", "*")` → `True`，`("adceb", "*a*b")` → `True`，`("acdcb", "a*c?b")` → `False`。

**为什么只回溯最近的 `*`。** 最近的 `*` 之前的部分已经匹配成功；更早的 `*` 可以吞下任意长度，所以最近 `*` 之前的结构不依赖它们吞了多少。若最近的 `*` 无论吞多长都救不回来，更早的 `*` 改变吞法也无济于事。

**取舍。** 贪心：`O(1)` 额外空间，常见输入接近 `O(m + n)`，但最坏仍是 `O(mn)`（`s` 是 `2000` 个 `a`，`p` 是 `*` 加 `1000` 个 `a` 再加 `b`：约 `10^6` 步），代码里指针更新容易写错。DP：思路直接、边界清楚，空间 `O(mn)`；也是面试里先写出来更稳妥的版本，再提贪心作为空间优化。
