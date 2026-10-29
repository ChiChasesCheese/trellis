---
id: tlc-tt-number-to-string-4-followup
node: a.tt-number-to-string
type: qa
step: 4
---
## Q
**手写数字转字符串**｜追问

整数和小数两版写完后，面试官接着问：（1）直接给一个浮点数 `x`，保留 `k` 位小数并四舍五入，为什么不能用 `x * 10**k` 再取整？怎么做才对？（2）如果语言是 64 位整数（C++ / Java），`-2^63` 怎么处理？（3）要输出 16 进制呢？

## A
1. **浮点数保留 `k` 位。** 浮点数是二进制的，`2.675` 实际存的是 `2.67499999999999982...`，正确的四舍五入结果是 `2.67`。但 `2.675 * 100` 这次乘法先舍入成了 `267.5`，再取整进位得到 `2.68`，错了；`k` 大时 `x * 10**k` 还可能溢出成 `inf`（`1e300 * 10**20`）。正确做法：用 `x.as_integer_ratio()` 拿到精确的分数 `num / den`（两个整数），全程只做整数运算。

```python
import math


def float_to_str(x: float, k: int) -> str:
    """x 保留 k 位小数，对 x 的精确二进制值四舍五入（0.5 进位）。"""
    if not math.isfinite(x):
        raise ValueError("x 必须是有限数")
    num, den = x.as_integer_ratio()            # x == num / den，两个整数，精确无误差
    neg = num < 0
    q, r = divmod(abs(num) * 10**k, den)       # q 是 |x| * 10^k 的整数部分，r 是余数
    if 2 * r >= den:                           # 余数 >= 一半：进位
        q += 1
    int_part, frac_value = divmod(q, 10**k)
    out = int_to_str(int_part)
    if k:
        frac = int_to_str(frac_value)
        out += "." + "0" * (k - len(frac)) + frac
    return "-" + out if neg and q else out
```

   运行：`float_to_str(2.675, 2)` → `"2.67"`，`float_to_str(1.005, 2)` → `"1.00"`，`float_to_str(123.456, 1)` → `"123.5"`，`float_to_str(-1.25, 1)` → `"-1.3"`，`float_to_str(0.5, 0)` → `"1"`，`float_to_str(-0.001, 2)` → `"0.00"`。恰好在中点的数（`0.125` 保留两位）按“0.5 进位”得 `"0.13"`，而 `f"{0.125:.2f}"` 按偶数舍入得 `"0.12"`，面试时先问清规则。
2. **`-2^63`。** 它的绝对值 `2^63` 超出 `int64`。不取绝对值，改在负数一侧累积：负数的余数取反得到数字（`digit = -(n % 10)` 在“向零取整”的语言里成立），每轮 `n /= 10`。
3. **16 进制。** 基数 `10` 换成 `16`，数字由 `chr(48 + d)` 换成查字符表 `DIGITS[d]`（`DIGITS` 是按顺序排好 0 到 9、a 到 f 的字符串）；负数的补码表示要先 `n & 0xFFFFFFFFFFFFFFFF` 转成无符号。

**Python 提醒**：`Decimal(2.675)` 会把浮点数的**精确**值展开成 `2.67499999999999982236431605997495353221893310546875`，而 `Decimal("2.675")` 才是字面量 `2.675`；`round(2.675, 2)` 得到 `2.67` 也是同一原因。
