---
id: tlc-multiply-strings-4-followup
node: a.multiply-strings
type: qa
step: 4
---
## Q
**LC 43 字符串相乘**｜追问

面试官接着问：（1）顺手写一个字符串**加法**？（2）数字有几十万位，`O(mn)` 太慢怎么办？（3）Python 里直接 `int(a) * int(b)` 在这题里为什么被禁，现实中又有什么限制？

## A
1. **字符串加法**（LC 415）：从低位同时走两个串，用 `zip_longest` 把较短的串补 `"0"` 对齐，进位用 `divmod`。`"11" + "123"` → `"134"`，`"999" + "1"` → `"1000"`。
```python
from itertools import zip_longest

def add_strings(a: str, b: str) -> str:
    out: list[str] = []
    carry = 0
    for x, y in zip_longest(reversed(a), reversed(b), fillvalue="0"):
        carry, d = divmod(int(x) + int(y) + carry, 10)
        out.append(str(d))
    if carry:
        out.append("1")
    return "".join(reversed(out))
```
2. **超长数字**：Karatsuba 把乘法拆成三次半长度乘法，`O(n^1.585)`；更长用 FFT / NTT，把竖式卷积变成点乘，`O(n log n)`。竖式里的 `res[k] = Σ a[i] b[k-i]` 本来就是一个卷积，这正是 FFT 能加速的原因。
3. **`int` 的限制**：题面禁用大数库，所以内置 `int` 在这里不算解法。现实里 Python 的 `int` 是任意精度，但整数与字符串互转在 3.11+ 默认限制 4300 位，超出会抛 `ValueError`（`sys.set_int_max_str_digits` 可调），这是防止恶意输入造成二次方时间的拒绝服务。

**Python 提醒**：`zip` 遇到最短的序列就停，位数不同的两个串必须用 `zip_longest`，否则较长串的高位会被悄悄丢掉；`fillvalue` 要给 `"0"` 而不是默认的 `None`，否则 `int(None)` 报错。
