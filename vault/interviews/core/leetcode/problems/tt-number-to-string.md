---
slug: tt-number-to-string
---
## Q
**手写数字转字符串**｜Medium

不用 `str`、`repr`、`format`、f-string，把数转成十进制字符串。（1）64 位整数 `n`，注意 `0` 和负数；（2）小数 `(sign, int_part, frac_value, frac_len)`，`frac_value` 是小数部分当整数读出的值，输出去掉小数末尾 `0`，小数全为 `0` 不带小数点，数值为 `0` 不带负号。例：`(-1, 12, 50, 3)` → `"-12.05"`，`(1, 0, 5, 3)` → `"0.005"`。

## A
**一句话。** 反复 `divmod(n, 10)` 低位先出再反转；小数部分先去末尾 `0`，转成数字串后在左边补回前导 `0` 凑够位数。

```python
def int_to_str(n):
    if n == 0:
        return "0"
    neg = n < 0
    n = -n if neg else n      # divmod 对负数会给负余数
    digits = []
    while n:
        n, d = divmod(n, 10)
        digits.append(chr(48 + d))   # 48 是 '0'
    if neg:
        digits.append("-")
    return "".join(reversed(digits))

def decimal_to_str(sign, int_part, frac_value, frac_len):
    while frac_len and frac_value % 10 == 0:  # 去末尾 0
        frac_value //= 10
        frac_len -= 1
    out = int_to_str(int_part)
    if frac_len:
        frac = int_to_str(frac_value)
        out += "." + "0" * (frac_len - len(frac)) + frac
    if sign < 0 and (int_part or frac_len):   # 数值为 0 不带负号
        out = "-" + out
    return out
```

**复杂度。** 时间 `O(d)`，空间 `O(d)`（`d` 为位数）。

**易错点。**
- `n = 0` 不特判：循环不进，返回 `""`，应为 `"0"`。
- 直接对负数 `divmod`：`divmod(-1, 10)` 是 `(-1, 9)`，`n` 到不了 `0`，死循环。
- 小数前导 `0` 丢失：`(1, 0, 5, 3)` 得 `"0.5"`，应为 `"0.005"`。
- 符号只看 `int_part`：`(-1, 0, 5, 2)` 丢负号得 `"0.05"`；`(-1, 0, 0, 2)` 错成 `"-0"`。

**追问。**
- 直接给浮点数、保留 `k` 位四舍五入？：不能先乘 `10**k` 再取整（乘法本身会舍入），用 `x.as_integer_ratio()` 拿精确分数再整数舍入。
- 其他进制？：把 `chr(48 + d)` 换成查字符表 `DIGITS[d]`。

**同模式。** LC 8 字符串转换整数、LC 7 整数反转、LC 168 Excel 表列名称、LC 415 字符串相加
