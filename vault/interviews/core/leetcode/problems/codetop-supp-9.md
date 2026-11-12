---
slug: codetop-supp-9
---
## Q
**补充题 9 36进制加法**｜Medium

两个非负 36 进制数（`0-9a-z`）的字符串，返回它们的和（36 进制字符串）。不能用 `int(s, 36)` 整串转换。

## A
**一句话。** 竖式加法：双指针从末尾逐位相加带进位，`divmod(total, 36)` 拆出进位和当前位。

```python
def add_36(num1, num2):
    D = string.digits + string.ascii_lowercase
    val = {ch: v for v, ch in enumerate(D)}
    i, j, carry = len(num1) - 1, len(num2) - 1, 0
    out = []
    while i >= 0 or j >= 0 or carry:
        total = carry
        if i >= 0:
            total += val[num1[i]]
            i -= 1
        if j >= 0:
            total += val[num2[j]]
            j -= 1
        carry, digit = divmod(total, 36)
        out.append(D[digit])
    return "".join(reversed(out))
```

**复杂度。** 时间 `O(max(m, n))`，空间 `O(max(m, n))`。

**易错点。**
- 循环漏掉 `or carry`：`"zz" + "1"` 得 `"00"`，应为 `"100"`。
- 字母按十进制处理：`"19" + "1"` 应为 `"1a"`，不是 `"20"`。
- 用 `int(num, 36)`：`"z" * 10000` 在 Python 3.11+ 抛 `ValueError`（超过 4300 位）。

**追问。**
- 其他进制怎么改？：把 `36` 和字母表参数化。
- 相乘（LC 43）？：位置 `i + j` 累加，最后统一进位。

**同模式。** LC 415 字符串相加、LC 67 二进制求和、LC 2 两数相加、LC 43 字符串相乘
