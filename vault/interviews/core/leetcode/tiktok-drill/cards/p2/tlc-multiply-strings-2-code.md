---
id: tlc-multiply-strings-2-code
node: p2.multiply-strings
type: qa
step: 2
---
## Q
**LC 43 字符串相乘**｜写出 Python 实现

两个非负整数的十进制字符串 `num1`、`num2`（长度各 `1` 到 `200`，只含数字，除 `"0"` 外没有前导零），返回乘积的字符串形式。不能使用大整数库，也不能把整个字符串转成整数。

## A
**思路。** 两个数各自反转，使个位在下标 0。`res[i + j] += a[i] * b[j]` 先累加不进位；再从低位到高位统一进位；最后去掉高位多余的 `0` 并反转拼接。

```python
def multiply(num1: str, num2: str) -> str:
    a = [int(c) for c in reversed(num1)]  # 个位在下标 0
    b = [int(c) for c in reversed(num2)]
    res = [0] * (len(a) + len(b))         # a[i] * b[j] 落在第 i + j 位
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            res[i + j] += x * y           # 先只累加，不进位
    carry = 0
    for k in range(len(res)):             # 统一进一遍位
        carry, res[k] = divmod(res[k] + carry, 10)
    while len(res) > 1 and res[-1] == 0:  # 去掉高位多余的 0；乘积为 0 时保留一个 "0"
        res.pop()
    return "".join(map(str, reversed(res)))
```

运行：`("2", "3")` → `"6"`，`("123", "456")` → `"56088"`，`("0", "9999")` → `"0"`，`("999", "999")` → `"998001"`，`("10", "10")` → `"100"`，`("0", "0")` → `"0"`。

**复杂度。** 时间 `O(mn)`：双重循环是主体，进位只有 `O(m + n)`；空间 `O(m + n)`：两个数字数组和结果数组。

**写法要点。** `reversed(str)` 不复制字符串，配合列表推导一步得到「个位在前」的数字数组；`enumerate` 同时拿下标与数值；`divmod(x, 10)` 一次得到进位和当前位，比 `x // 10` 加 `x % 10` 少一次除法；`while len(res) > 1` 保证乘积为 0 时仍保留一个 `0`；`"".join(map(str, reversed(res)))` 倒序拼接，没有手写循环。不要写成 `str(int(num1) * int(num2))`：它正是题面禁止的做法，也看不出你会处理进位。
