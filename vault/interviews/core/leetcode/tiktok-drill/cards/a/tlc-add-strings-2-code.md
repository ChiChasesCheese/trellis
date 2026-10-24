---
id: tlc-add-strings-2-code
node: a.add-strings
type: qa
step: 2
---
## Q
**LC 415 字符串相加**｜写出 Python 实现

两个由数字 `0-9` 组成、不含前导零的字符串 `num1`、`num2`（长度都在 `[1, 10^4]`），不能把整个字符串转成整数。返回它们的和，同样是字符串。

## A
**思路。** 同时从两个字符串的末尾往前走，用 `zip_longest` 把较短的串补 `"0"`。每一位：数字之和加上进位，`divmod(…, 10)` 得到新进位和当前位；当前位追加到列表。循环结束后若还有进位，再追加 `"1"`。最后把列表反转并拼接成字符串。

```python
from itertools import zip_longest


def add_strings(num1: str, num2: str) -> str:
    digits: list[str] = []
    carry = 0
    # 从个位开始配对；短的那个用 "0" 补齐
    for a, b in zip_longest(reversed(num1), reversed(num2), fillvalue="0"):
        carry, d = divmod(int(a) + int(b) + carry, 10)    # 一步同时得到进位和当前位
        digits.append(str(d))
    if carry:
        digits.append("1")
    return "".join(reversed(digits))
```

运行：`("11", "123")` → `"134"`，`("456", "77")` → `"533"`，`("0", "0")` → `"0"`，`("999", "1")` → `"1000"`，`("1", "999")` → `"1000"`，`10^4` 个 `"9"` 加 `"1"` → `"1"` 后面跟 `10^4` 个 `"0"`。

**复杂度。** 时间 `O(max(m, n))`：每位常数次操作；空间 `O(max(m, n))`：结果列表。

**写法要点。** `reversed(str)` 返回迭代器，不拷贝字符串；`zip_longest` 的 `fillvalue` 一次解决「长度不同」，免去两个 `while` 和下标越界的判断；`divmod(x, 10)` 同时返回商（进位）和余数（当前位），比分别写 `// 10` 和 `% 10` 少算一次；用列表 `append` 加最后 `"".join` 拼接，是 `O(n)`；反复 `result = d + result` 在前面插入会让每次都复制整串，是 `O(n^2)`。
