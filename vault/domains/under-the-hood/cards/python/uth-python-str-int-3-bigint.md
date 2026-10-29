---
id: uth-python-str-int-3-bigint
node: python.str-int
type: qa
step: 3
---
## Q
**Python 的大整数怎么存、怎么乘**｜Python · CPython 3.14

Python 的 `int` 没有溢出，`2**1000` 底下是什么？两个 8000 位的整数相乘，比 4000 位的慢几倍？

## A
**背景。** 机器一次只能算 64 位以内的整数，再大会溢出。想表示任意大的数，办法和手算竖式一样：把数拆成很多「位」，用一个数组存，每位单独计算再处理进位。

**结构。** 数位数组（digit array），每个数位 30 位，放在 32 位字里；数越大数组越长。例：`2**60` 要 3 个数位。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<text x="170" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2**60 = 3 个数位</text>
<rect x="40" y="34" width="80" height="34" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="80" y="55" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="80" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">数位 0 低</text>
<rect x="126" y="34" width="80" height="34" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="166" y="55" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="166" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">数位 1</text>
<rect x="212" y="34" width="80" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="252" y="55" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="252" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">数位 2 高</text>
<text x="170" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个数位 30 位 放在 32 位字里</text>
<text x="170" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">值 = 1 x (2^30)^2</text>
</svg>
```

**细节。**

- `getsizeof`：`1` 为 28，`2**30` 为 32，`2**60` 为 36。
- 两边都超过 70 个数位（约 630 位十进制）时改用 Karatsuba（把一次大乘法拆成三次小乘法），O(n^1.585)。
- 实测 4000 位 36 微秒，8000 位 112 微秒，约 3.1 倍，朴素算法是 4 倍。

**为什么。** 30 位乘 30 位刚好放进 64 位积；小数用朴素乘法常数更小，所以设阈值切换。

**坑。** 大整数与十进制字符串互转没有线性算法，3.11 起默认超过 4300 位会抛 `ValueError`。

**例题：** LC 43 字符串相乘

给两个字符串形式的非负整数 `num1`、`num2`，返回它们乘积的字符串形式；不能用内置大整数，也不能直接把输入转成整数。`1 <= 长度 <= 200`。例：`"123"` 乘 `"456"` 得 `"56088"`。

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
