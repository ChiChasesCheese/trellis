---
slug: isomorphic-strings
---
## Q
**LC 205 同构字符串**｜Easy

判断 `s` 能否通过一一映射替换字符得到 `t`：相同字符映射到同一字符，不同字符不能映射到同一字符。

## A
**一句话。** 逐位同时维护 `s→t` 和 `t→s` 两张映射，任一边冲突就不同构。

```python
def is_isomorphic(s, t):
    s2t, t2s = {}, {}
    for a, b in zip(s, t):
        if (s2t.setdefault(a, b) != b
                or t2s.setdefault(b, a) != a):
            return False
    return True
```

**复杂度。** 时间 `O(n)`，空间 `O(Σ)`。

**易错点。**
- 只查一个方向：`("badc","baba")` 只用 `s→t` 得 `True`，但 `b`、`d` 都映射到 `b`，应为 `False`。
- 用 `s.index(c)` 比首次位置：每次 `O(n)`，整体 `O(n²)`。

**追问。**
- 不建两张表还能怎么写？：把每个字符替换成它首次出现的下标，比较两串的结果是否相等。

**同模式。** LC 290 单词规律、LC 242 有效的字母异位词、LC 49 字母异位词分组
