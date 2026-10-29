---
id: tlc-longest-palindrome-2-code
node: a.longest-palindrome
type: qa
step: 2
---
## Q
**LC 409 最长回文串**｜写出 Python 实现

只含大小写字母的字符串 `s`（长度 `1..2000`，区分大小写），用其中的字母（可重排）构造回文串，求最大长度。要求 `O(n)`。

## A
**思路。** 计数后每种字母取 `v // 2 * 2` 个成对放两侧；若这些成对的字母没用完 `s` 的全部字母，说明有字母落单，取一个放正中间。

```python
from collections import Counter


def longest_palindrome(s: str) -> int:
    pairs = sum(v // 2 * 2 for v in Counter(s).values())   # 每种字母能成对放在两侧的部分
    return pairs + (pairs < len(s))                          # 还有剩下的字母，就放一个在正中间
```

运行：`"abccccdd"` → `7`，`"a"` → `1`，`"Aa"` → `1`，`"aaabbbcc"` → `7`，`"abc"` → `1`。

**复杂度。** 时间 `O(n)`：`Counter` 计数一遍；空间 `O(Σ)`：至多 52 个键。

**写法要点。** `Counter(s).values()` 直接拿到每种字母的次数；`v // 2 * 2` 把奇数向下取到偶数；`pairs < len(s)` 是布尔值，`bool` 是 `int` 的子类，`True` 加法时等于 1，一行表达「有剩余就加 1」；生成器表达式传给 `sum`，不建中间列表。
