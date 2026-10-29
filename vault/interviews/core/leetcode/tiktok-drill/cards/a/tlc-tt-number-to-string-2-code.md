---
id: tlc-tt-number-to-string-2-code
node: a.tt-number-to-string
type: qa
step: 2
---
## Q
**手写数字转字符串**｜写出 Python 实现

不使用 `str`、`repr`、`format`、f-string：写 `int_to_str(n)`（64 位有符号整数）和 `decimal_to_str(sign, int_part, frac_value, frac_len)`（`sign` 为 `-1` 或 `1`，`frac_value` 是小数部分当整数读出的值，`frac_len` 是小数位数）。后者输出规范写法：去掉小数末尾的 `0`，小数全为 `0` 时不输出小数点，数值为 `0` 时不带负号。

## A
**思路。** 整数：`divmod(n, 10)` 取最低位，低位先出再反转；`0` 特判，负数先取绝对值。小数：整数部分照旧；先去掉小数末尾的 `0`，再把 `frac_value` 转成数字串并在左边补零到 `frac_len` 位。

```python
def int_to_str(n: int) -> str:
    if n == 0:
        return "0"
    neg = n < 0
    n = -n if neg else n                       # 先取绝对值：Python 的 divmod 对负数向下取整，会得到负的余数位
    digits: list[str] = []
    while n:
        n, d = divmod(n, 10)                   # 一次同时拿商和余数
        digits.append(chr(48 + d))             # 48 是 '0' 的编码；d 是 0..9
    if neg:
        digits.append("-")
    return "".join(reversed(digits))           # 低位先出，最后整体反转


def decimal_to_str(sign: int, int_part: int, frac_value: int, frac_len: int) -> str:
    while frac_len and frac_value % 10 == 0:   # 去掉小数末尾的 0：frac_value 缩小十倍，位数减一
        frac_value //= 10
        frac_len -= 1
    out = int_to_str(int_part)
    if frac_len:                               # frac_len == 0 说明小数部分全为 0：不输出小数点
        frac = int_to_str(frac_value)
        out += "." + "0" * (frac_len - len(frac)) + frac   # 左边补回被整数表示吞掉的前导 0
    if sign < 0 and (int_part or frac_len):    # 数值为 0 时不输出负号，避免 "-0"
        out = "-" + out
    return out
```

运行：`int_to_str` 对 `0`、`5`、`-5`、`120`、`-2^63`、`2^63 - 1` 得 `"0"`、`"5"`、`"-5"`、`"120"`、`"-9223372036854775808"`、`"9223372036854775807"`；`decimal_to_str`：`(-1, 12, 50, 3)` → `"-12.05"`，`(1, 0, 5, 3)` → `"0.005"`，`(-1, 0, 5, 2)` → `"-0.05"`，`(-1, 0, 0, 2)` → `"0"`，`(1, 7, 0, 4)` → `"7"`，`(1, 3, 100, 3)` → `"3.1"`，`(1, 100, 0, 0)` → `"100"`。

**复杂度。** 时间 `O(d)`，`d` 为数字位数：整数至多 `19` 位，小数部分 `O(frac_len)`；空间 `O(d)`。

**写法要点。** `n, d = divmod(n, 10)` 一次拿商和余数，同时赋值；`chr(48 + d)` 用字符编码把数字变字符，不依赖 `str`；用 `list` 收集再 `"".join(reversed(...))`，避免 `s = c + s` 在循环里反复拷贝；去末尾 `0` 用整数运算（`% 10`、`// 10`）而不是先转成字符串再 `rstrip`，这样 `frac_len` 同步减少；`int_part or frac_len` 利用整数的真值判断“数值是否非零”。
