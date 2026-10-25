---
id: tlc-string-to-integer-atoi-2-code
node: b.string-to-integer-atoi
type: qa
step: 2
---
## Q
**LC 8 字符串转换整数 (atoi)**｜写出 Python 实现

字符串 `s`（长度 `0` 到 `200`，由字母、数字、空格、`+`、`-`、`.` 组成）：丢弃前导空格，读一个可选符号，读数字到非数字为止，结果截断到 `[-2^31, 2^31 - 1]`；没读到数字返回 `0`。

## A
**思路。** 下标 `i` 依次越过空格、读符号、读数字。符号决定 `limit`：正数 `2^31 - 1`，负数 `2^31`。累加数字时如果 `num` 已经达到 `limit`，直接返回 `sign * limit`，不再继续读。

```python
def my_atoi(s: str) -> int:
    INT_MAX, INT_MIN = 2**31 - 1, -(2**31)
    i, n = 0, len(s)
    while i < n and s[i] == " ":                   # 1. 空格：只有 ' ' 才跳过
        i += 1
    sign = 1
    if i < n and s[i] in "+-":                     # 2. 符号：至多一个
        sign = -1 if s[i] == "-" else 1
        i += 1
    limit = INT_MAX if sign == 1 else -INT_MIN     # 正数最大 2^31-1，负数的绝对值最大 2^31
    num = 0
    while i < n and "0" <= s[i] <= "9":            # 3. 数字：遇到第一个非数字就停
        num = num * 10 + (ord(s[i]) - ord("0"))
        if num >= limit:                           # 4. 数字只会越来越大，达到上限就能提前返回
            return sign * limit
        i += 1
    return sign * num
```

运行：`"42"` → `42`，`" -042"` → `-42`，`"4193 with words"` → `4193`，`"0-1"` → `0`，`"words and 987"` → `0`，`""` → `0`，`"+-12"` → `0`，`"-91283472332"` → `-2147483648`，`"21474836470"` → `2147483647`，`"3.14159"` → `3`。

**复杂度。** 时间 `O(n)`；空间 `O(1)`。

**写法要点。** `s[i] in "+-"` 用成员测试代替两个 `==`；`"0" <= s[i] <= "9"` 链式比较只接受 ASCII 数字；`ord(c) - ord("0")` 得到数字值；`limit` 把正负两个上界统一成一个比较；`num >= limit` 的提前返回同时覆盖「恰好等于边界」和「超出边界」两种情形，Python 的整数不会溢出，但这样写和固定位宽语言的思路一致。
