---
id: tlc-add-strings-4-followup
node: a.add-strings
type: qa
step: 4
---
## Q
**LC 415 字符串相加**｜追问

面试官接着问：（1）改成**二进制**或 **36 进制**的字符串相加？（2）输入可能带**前导零**或**负号**？（3）要做**乘法**（LC 43）？

## A
1. **其他进制**：进位基数从 `10` 换成 `base`。二进制把 `divmod(…, 10)` 换成 `divmod(…, 2)`。36 进制的字符是 `0-9a-z`，不能用 `int(a)`，要查表：`DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"`，值用 `DIGITS.index(a)`（或预先建字典），输出用 `DIGITS[d]`，基数 `36`。
2. **前导零与负号**：前导零不影响逐位加法，但结果可能需要去掉（结果的最高位若是 `0` 且长度大于 `1`，就 `lstrip("0") or "0"`）。负号：先比较绝对值大小，同号相加、异号用大减小，写一个 `subtract_strings`，思路同样是逐位带借位。
3. **乘法（LC 43）**：开一个长度 `m + n` 的整数数组，`num1[i] * num2[j]` 累加到 `res[i + j + 1]`，最后统一处理进位。逐位算完再进位，整体 `O(m · n)`。

**Python 提醒**：Python 的 `int` 本身支持任意精度，但 3.11 之后，`int(s)` 和 `str(n)` 在超过 4300 位时默认抛 `ValueError`（可以用 `sys.set_int_max_str_digits` 调整）。所以「`str(int(a) + int(b))`」在长输入上不只是违规，还会直接出错。单个字符的 `int("7")` 不受影响。
