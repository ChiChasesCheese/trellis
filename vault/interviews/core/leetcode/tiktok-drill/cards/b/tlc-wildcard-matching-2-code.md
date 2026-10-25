---
id: tlc-wildcard-matching-2-code
node: b.wildcard-matching
type: qa
step: 2
---
## Q
**LC 44 通配符匹配**｜写出 Python 实现

字符串 `s` 和模式 `p`（长度都在 `0` 到 `2000`；`s` 只含小写字母，`p` 只含小写字母、`?`、`*`）。`?` 匹配任意单个字符，`*` 匹配任意字符序列（含空），要求整个 `s` 被匹配。返回是否匹配，时间 `O(mn)`。

## A
**思路。** `dp[j]` 表示当前 `s` 前缀能否被 `p` 的前 `j` 个字符匹配。每读入 `s` 的一个字符就算一行新的 `dp`：`*` 位置取「匹配空」（本行左边一格）或「多吞一个字符」（上一行同列）；`?` 或字母相等则取上一行左上角。

```python
def is_match(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    # dp[j]：s 的前 i 个字符能否被 p 的前 j 个字符匹配（只保留上一行和当前行）
    dp = [False] * (n + 1)
    dp[0] = True
    for j in range(1, n + 1):              # s 为空时，只有连续的 '*' 能匹配
        dp[j] = dp[j - 1] and p[j - 1] == "*"
    for i in range(1, m + 1):
        new = [False] * (n + 1)            # new[0]：非空 s 不能匹配空模式
        for j in range(1, n + 1):
            if p[j - 1] == "*":
                new[j] = new[j - 1] or dp[j]       # '*' 匹配空 / 再多吞掉 s[i-1]
            elif p[j - 1] in ("?", s[i - 1]):
                new[j] = dp[j - 1]
        dp = new
    return dp[n]
```

运行：`("aa", "a")` → `False`，`("aa", "*")` → `True`，`("cb", "?a")` → `False`，`("", "*")` → `True`，`("", "?")` → `False`，`("adceb", "*a*b")` → `True`，`("acdcb", "a*c?b")` → `False`。

**复杂度。** 时间 `O(mn)`：每个 `(i, j)` 一次常数转移；空间 `O(n)`：只留两行。

**写法要点。** `p[j - 1] in ("?", s[i - 1])` 用元组成员判断把「通配或相等」合成一个条件；布尔链 `dp[j - 1] and p[j - 1] == "*"` 直接得到初始化，不用单独的 `if`；每行新建 `new` 再整体赋给 `dp`，比就地覆盖少一个「左上角旧值」的暂存变量。
