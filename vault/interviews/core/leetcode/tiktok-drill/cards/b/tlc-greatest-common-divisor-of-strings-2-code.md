---
id: tlc-greatest-common-divisor-of-strings-2-code
node: b.greatest-common-divisor-of-strings
type: qa
step: 2
---
## Q
**LC 1071 字符串的最大公因子**｜写出 Python 实现

`str1` 和 `str2` 是大写英文字母串（长度 `1..1000`）。`t` 能除尽 `s` 指 `s` 是 `t` 重复一次或多次。返回能同时除尽两者的最长字符串，没有则返回 `""`。

## A
**思路。** 若两个字符串有公因子串，两种拼接顺序一定相同；反过来，拼接顺序相同也说明有公因子串，且最长的长度是两个长度的最大公约数。所以先比较拼接，再取前缀。

```python
from math import gcd


def gcd_of_strings(str1: str, str2: str) -> str:
    if str1 + str2 != str2 + str1:         # 有公因子串 <=> 两种拼接顺序结果一致
        return ""
    return str1[:gcd(len(str1), len(str2))]
```

运行：`("ABCABC", "ABC")` → `'ABC'`，`("ABABAB", "ABAB")` → `'AB'`，`("LEET", "CODE")` → `''`，`("AAAAAB", "AAA")` → `''`，`("A", "A")` → `'A'`，`("AB", "BA")` → `''`，`("A" * 1000, "A" * 999)` → `'A'`。

**复杂度。** 时间 `O(n)`：两次拼接与一次比较各 `O(n)`，`gcd` 为 `O(log n)`；空间 `O(n)`。

**写法要点。** `math.gcd` 是标准库，不要手写辗转相除；`str1[:g]` 的切片取前缀，结果是新字符串；两个字符串拼接比较直接用 `!=`，Python 的字符串比较是 C 实现的逐字节比较，很快。不要把它写成 `str1.replace(…)` 之类的循环，意图不清楚且容易出错。
