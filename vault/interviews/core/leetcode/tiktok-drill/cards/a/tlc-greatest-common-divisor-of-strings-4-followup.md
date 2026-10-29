---
id: tlc-greatest-common-divisor-of-strings-4-followup
node: a.greatest-common-divisor-of-strings
type: qa
step: 4
---
## Q
**LC 1071 字符串的最大公因子**｜追问

面试官接着问：（1）有多个字符串，求它们共同的最大公因子？（2）求“最短的、能被两个字符串都整除的串”（最小公倍串）？（3）不让你用拼接比较的技巧，怎么写？

## A
1. **多个字符串**：最大公因子满足结合律，两两合并。

```python
from functools import reduce
from math import gcd


def gcd_of_many(strs: list[str]) -> str:
    def pair(a: str, b: str) -> str:
        return a[:gcd(len(a), len(b))] if a + b == b + a else ""

    return reduce(pair, strs)
```

   `["ABABAB", "ABAB", "AB"]` → `'AB'`，`["AAAA", "AA", "AAAAAA"]` → `'AA'`，`["AB", "AC"]` → `''`，`["AB"]` → `'AB'`。中间一旦得到 `""`，后面每一步拼接比较都成立，`gcd` 为 `len(b)`，切片 `""[:k]` 仍是 `""`，结果保持为空。
2. **最小公倍串**：拼接顺序相同时，取 `str1 * (len(str2) // gcd(len1, len2))`，长度是 `lcm(len1, len2)`。`("ABAB", "ABABAB")` → 长度 `12` 的 `'ABABABABABAB'`；`("AB", "ABA")` → `''`。
3. **不用拼接技巧**：枚举候选长度 `L`（只需看 `gcd(len1, len2)` 的约数，从大到小），取 `str1[:L]`，检查 `t * (len(str1) // L) == str1` 且 `t * (len(str2) // L) == str2`，第一个满足的就是答案。复杂度 `O(n · d(g))`，`d(g)` 是约数个数；`n <= 1000` 时同样很快，面试里可以把它当作可读性最好的基线。

**Python 提醒**：`functools.reduce` 在空序列上会抛 `TypeError`，没有初始值时要保证 `strs` 非空；字符串乘法 `t * k` 在 `k = 0` 时得到 `""`，在 `k` 为负数时也是 `""`，不会报错，容易掩盖算错 `k` 的 bug。
