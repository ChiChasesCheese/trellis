---
id: tlc-length-of-the-longest-alphabetical-continuous-substring-2-code
node: b.length-of-the-longest-alphabetical-continuous-substring
type: qa
step: 2
---
## Q
**LC 2414 最长的字母序连续子字符串的长度**｜写出 Python 实现

仅由小写英文字母组成的非空字符串 `s`（长度 `1..10^5`）。字母序连续子串指字母表中连续的字母，如 `"abc"`（`"acb"` 和 `"za"` 不是）。返回 `s` 中最长的字母序连续子串的长度。

## A
**思路。** 逐对看相邻字符：后一个恰好比前一个大 `1` 就延续当前连续段，否则新段从当前字符开始；每步更新最大长度。

```python
from itertools import pairwise


def longest_continuous_substring(s: str) -> int:
    best = run = 1                             # s 非空，单个字符本身就是长度 1
    for prev, cur in pairwise(s):
        run = run + 1 if ord(cur) - ord(prev) == 1 else 1   # 恰好差 1 才延续，否则从自己重新开始
        best = max(best, run)
    return best
```

运行：`"abacaba"` → `2`，`"abcde"` → `5`，`"a"` → `1`，`"zab"` → `2`，`"yz"` → `2`。

**复杂度。** 时间 `O(n)`：一趟扫描；空间 `O(1)`：`pairwise` 是迭代器，不建中间列表。

**写法要点。** `itertools.pairwise`（Python 3.10+）直接给出相邻对 `(s[i-1], s[i])`，省掉下标运算和 `range(1, n)`。`ord(cur) - ord(prev) == 1` 比 `cur == chr(ord(prev) + 1)` 更短，也不会产生新字符串。`run + 1 if 条件 else 1` 把“延续 / 重置”写成一个条件表达式。`best = run = 1` 链式赋值只对不可变的整数安全。
