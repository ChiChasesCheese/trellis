---
id: uth-python-numbers-floats-2-bigint-cost
node: python.numbers-floats
type: qa
step: 2
---
## Q
**大整数越大越慢**｜Python · CPython 3.14

大整数的乘法、转成十进制字符串各有多贵？为什么 `print(10**5000)` 会抛 `ValueError`？

## A
**背景。** 小学竖式乘法：两个 n 位数要做 n × n 次单位乘法，位数翻倍，时间变 4 倍。

**结构。** CPython 的 `int` 乘法默认就是竖式；两个数都超过 70 位（70 × 30 = 2100 个二进制位，约 630 个十进制数字）时，改用 Karatsuba 算法：把每个数劈成高低两半，用 3 次半长乘法代替 4 次。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 176">
<text x="80" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">竖式 4 次乘法</text>
<text x="260" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Karatsuba 3 次</text>
<rect x="14" y="28" width="132" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="80" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a1*b1</text>
<rect x="14" y="58" width="132" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="80" y="75" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a1*b0</text>
<rect x="14" y="88" width="132" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="80" y="105" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a0*b1</text>
<rect x="14" y="118" width="132" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="80" y="135" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a0*b0</text>
<rect x="194" y="28" width="132" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="260" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a1*b1</text>
<rect x="194" y="58" width="132" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="260" y="75" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a0*b0</text>
<rect x="194" y="88" width="132" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="260" y="105" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">(a1+a0)*(b1+b0)</text>
<rect x="194" y="118" width="132" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="260" y="135" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">省掉 1 次</text>
<text x="170" y="166" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每次乘的数只有原来一半长</text>
</svg>
```

**细节。**

- 十进制转换（`str(n)`、`int(s)`）没有线性算法；只有 2、4、8、16、32 进制的转换是线性的。
- 3.11 起默认最多转换 4300 个十进制数字，超出抛 `ValueError`（防止恶意输入拖垮服务，CVE-2020-10735），`sys.set_int_max_str_digits()` 可调。
- 3.12 起，位数极多时转换和除法改用 `_pylong` 模块里渐近更快的算法。

**坑。** `str(10**5000)` 报错，`hex(10**5000)` 却没事。

**对应 LeetCode：** 无直接对应的题
