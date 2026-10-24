---
id: tlc-patterns-math-bit-sim-6-string-arithmetic
node: patterns.math-bit-sim
type: qa
step: 6
---
## Q
**数学、位运算与模拟｜字符串大数运算：字符串相加（LC 415）与字符串相乘（LC 43）**

不用 `int()` 转换整个字符串，怎样逐位做加法和乘法？

## A
题目的意图是模拟竖式，所以不要用 `int(a) + int(b)` 直接算（Python 虽然能做，但面试官会要求手写）。

```python
def add_strings(num1: str, num2: str) -> str:
    res: list[str] = []
    i, j, carry = len(num1) - 1, len(num2) - 1, 0
    while i >= 0 or j >= 0 or carry:       # 最后还有进位也要输出一位
        carry += (int(num1[i]) if i >= 0 else 0) + (int(num2[j]) if j >= 0 else 0)
        carry, digit = divmod(carry, 10)
        res.append(str(digit))
        i -= 1
        j -= 1
    return "".join(reversed(res))

def multiply(num1: str, num2: str) -> str:
    if num1 == "0" or num2 == "0":
        return "0"
    res = [0] * (len(num1) + len(num2))    # 乘积最多 m + n 位
    for i in range(len(num1) - 1, -1, -1):
        for j in range(len(num2) - 1, -1, -1):
            total = res[i + j + 1] + int(num1[i]) * int(num2[j])
            res[i + j + 1] = total % 10    # 当前位
            res[i + j] += total // 10      # 进位加到高一位
    return "".join(map(str, res)).lstrip("0")
print(add_strings("11", "123"), add_strings("456", "77"), add_strings("999", "1"))   # 134 533 1000
print(multiply("2", "3"), multiply("123", "456"), multiply("99", "99"), multiply("0", "99"))   # 6 56088 9801 0
```

- 加法：`carry` 同时承载"本位和"与"进位"，`divmod(carry, 10)` 一步拆成新的进位和当前位；循环条件包含 `carry`，最后的进位会生成一位。
- 乘法：`num1[i] × num2[j]` 的结果落在结果数组的 `i + j + 1`（个位）和 `i + j`（进位）两位；`res` 先开足 `m + n` 位，最后用 `lstrip("0")` 去掉前导零。
- 乘法时间 `O(mn)`，空间 `O(m + n)`。
- 特判 `"0"`：否则结果会全是前导零，`lstrip` 后变成空串。
- 拼出的字符串用 `list` + `join`，不要每位 `+=`。
