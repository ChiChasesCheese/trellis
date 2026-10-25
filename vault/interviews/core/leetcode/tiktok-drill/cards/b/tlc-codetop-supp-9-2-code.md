---
id: tlc-codetop-supp-9-2-code
node: b.codetop-supp-9
type: qa
step: 2
---
## Q
**补充题 9 36进制加法**｜写出 Python 实现

`num1`、`num2` 是两个非负 36 进制数的字符串（`0`~`9`、`a`~`z` 依次表示 0 到 35，没有前导零，长度在 `1` 到 `10^4`）。返回它们的和的 36 进制字符串，不能使用 `int(s, 36)` 这类整体转换。

## A
**思路。** 两个指针 `i`、`j` 从各自的末尾向前，进位 `carry` 初值 `0`。每轮把进位和还没走完的数字相加，`divmod(total, 36)` 得到新的进位和本位数字，把本位字符放进列表；`i`、`j` 都走完且没有进位时停止，最后反转列表。

```python
import string

DIGITS = string.digits + string.ascii_lowercase       # "0-9a-z"，下标就是数值
VALUE = {ch: v for v, ch in enumerate(DIGITS)}       # 字符 -> 数值

def add_36(num1: str, num2: str) -> str:
    i, j, carry = len(num1) - 1, len(num2) - 1, 0
    out: list[str] = []
    while i >= 0 or j >= 0 or carry:           # 最后还有进位时也要再走一轮
        total = carry
        if i >= 0:
            total += VALUE[num1[i]]
            i -= 1
        if j >= 0:
            total += VALUE[num2[j]]
            j -= 1
        carry, digit = divmod(total, 36)
        out.append(DIGITS[digit])
    return "".join(reversed(out))
```

运行：`("zz", "1")` → `"100"`，`("1z", "1")` → `"20"`，`("abc", "xyz")` → `"18ab"`，`("z", "z")` → `"1y"`，`("9", "1")` → `"a"`，`("0", "0")` → `"0"`；`("z" * 10000, "1")` → 长度 `10001`，以 `"100"` 开头。

**复杂度。** 时间 `O(max(m, n))`，每个字符处理一次；空间 `O(max(m, n))`。

**写法要点。** `string.digits + string.ascii_lowercase` 一次得到字母表，字母表的下标就是数值，反过来用字典 `VALUE` 查数值，比 `ord(c) - ord("a") + 10` 的分支少；`carry, digit = divmod(total, 36)` 一步完成「进位」和「本位」；`while i >= 0 or j >= 0 or carry` 把三种收尾情形统一在一个循环里；结果列表倒序拼接，避免对字符串做 `O(n)` 的头部插入。
