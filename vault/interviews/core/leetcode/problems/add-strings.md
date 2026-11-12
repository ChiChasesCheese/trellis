---
slug: add-strings
---
## Q
**LC 415 字符串相加**｜Easy

给两个字符串形式的非负整数，返回它们的和（字符串）。不能用大整数库，也不能把整串转成整数。

## A
**一句话。** 模拟竖式加法，从个位起逐位加进位，短的数用 `"0"` 补齐。

```python
def add_strings(num1, num2):
    digits, carry = [], 0
    # 从个位配对，短的补 "0"
    for a, b in zip_longest(reversed(num1), reversed(num2),
                            fillvalue="0"):
        carry, d = divmod(int(a) + int(b) + carry, 10)
        digits.append(str(d))
    if carry:
        digits.append("1")
    return "".join(reversed(digits))
```

**复杂度。** 时间 `O(max(m, n))`，空间 `O(max(m, n))`。

**易错点。**
- 漏掉最后的进位：`("999", "1")` 得 `"000"`，应为 `"1000"`。
- 用 `zip` 代替 `zip_longest`：较长数的高位被丢掉，`("11", "123")` 得 `"34"`。
- 忘了反转：`digits` 低位在前，`"134"` 会变成 `"431"`。

**追问。**
- 其他进制怎么改？：把 `10` 换成基数，字符转数值改成查表。
- 链表存的大数（LC 2 / LC 445）？：低位在前直接逐节点加；高位在前先反转或用栈。

**同模式。** LC 43 字符串相乘、LC 67 二进制求和、LC 2 两数相加、LC 445 两数相加 II
