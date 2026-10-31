---
id: tlc-find-the-difference-2-code
node: b.find-the-difference
type: qa
step: 2
---
## Q
**LC 389 找不同**｜写出 Python 实现

字符串 `s` 和 `t` 只含小写字母，`t` 是 `s` 重排后再插入一个字母的结果，`0 <= len(s) <= 1000`，`len(t) == len(s) + 1`。返回被插入的字母。

## A
**思路。** 对 `s` 和 `t` 的全部字符做异或。每个出现在两个字符串里的字符都出现偶数次，异或后抵消；多出来的字符出现奇数次，最后剩下它的编码。

```python
from itertools import chain


def find_the_difference(s: str, t: str) -> str:
    x = 0
    for ch in chain(s, t):          # 不拼接 s + t，省一个临时字符串
        x ^= ord(ch)                # 成对的字符异或为 0，只剩多出来的那个
    return chr(x)
```

运行：`("abcd", "abcde")` → `"e"`；`("", "y")` → `"y"`；`("a", "aa")` → `"a"`；`("aabb", "babba")` → `"b"`。

**复杂度。** 时间 `O(n)`，扫描 `2n + 1` 个字符；空间 `O(1)`，只有一个整数。

**写法要点。** `itertools.chain(s, t)` 把两个字符串按序遍历而不创建 `s + t`；`ord` / `chr` 在字符和码点之间转换，异或只能作用在整数上；初值 `0` 是异或的单位元（`0 ^ x = x`），所以 `s` 为空串时也直接成立；用循环而不是 `functools.reduce(xor, ...)`，两种写法等价，循环让「逐个吃进字符」更直观。
