---
id: uth-python-numbers-floats-1-bigint
node: python.numbers-floats
type: qa
step: 1
---
## Q
**int 为什么不会溢出**｜Python · CPython 3.14

C 和 Java 的 `int` 超过 2^31 就绕回负数，Python 的 `2**100` 却能直接算出来。大整数在内存里是怎样存的？

## A
**背景。** 硬件一次只能算 64 位以内的数。要存更大的数，办法和小学竖式一样：把大数拆成几段，每段单独算，再处理进位。

**结构。** CPython 的 `int` 就是这样一个数组：把数按 2^30 进制拆成若干「位」（digit），每位放进一个 32 位的格子，只用其中 30 位，留出余量接进位。数变大就多要几格，所以不会溢出。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 176">
<text x="170" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2**65 拆成 3 位 每位 30 个二进制位</text>
<text x="68" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">位 0</text>
<rect x="24" y="48" width="88" height="36" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="68" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="170" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">位 1</text>
<rect x="126" y="48" width="88" height="36" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="272" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">位 2</text>
<rect x="228" y="48" width="88" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="272" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">32</text>
<text x="68" y="102" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">x 1</text>
<text x="170" y="102" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">x 2^30</text>
<text x="272" y="102" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">x 2^60</text>
<text x="170" y="130" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0 + 0 x 2^30 + 32 x 2^60 = 2^65</text>
<text x="170" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">24 字节头 + 3 位 x 4 字节 = 36 字节</text>
</svg>
```

**细节。**

- 对象头 24 字节，再加每位 4 字节：0 到 2^30−1 都是 28 字节，`2**100` 要 4 位，是 40 字节。
- 取 30 位，是因为两个 30 位的数相乘不超过 60 位，装得进 64 位的机器字（CPU 一次处理的宽度）。

**坑。** 题目要求「32 位整数溢出就返回 0」时，Python 不会自己溢出，得手动比较范围。

**例题：** LC 7 整数反转（同类：LC 8 字符串转换整数）

把 32 位有符号整数 `x` 的数字部分反转；结果超出 [-2^31, 2^31 - 1] 就返回 0。例：`123` → `321`，`-123` → `-321`。

```python
def reverse(x: int) -> int:
    sign = -1 if x < 0 else 1
    digits = abs(x)
    result = 0
    while digits:
        digits, last_digit = divmod(digits, 10)
        result = result * 10 + last_digit
    result *= sign
    if result < -2**31 or result > 2**31 - 1:
        return 0
    return result
```
