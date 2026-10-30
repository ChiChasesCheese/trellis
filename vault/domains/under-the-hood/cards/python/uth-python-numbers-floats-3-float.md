---
id: uth-python-numbers-floats-3-float
node: python.numbers-floats
type: qa
step: 3
---
## Q
**0.1 + 0.2 为什么不等于 0.3**｜Python · CPython 3.14

`0.1 + 0.2 == 0.3` 为什么是 `False`？`float` 在内存里到底存了什么？

## A
**背景。** 十进制写不出 1/3（0.333… 无穷下去），只能截断。二进制同样写不出 1/10，会无穷循环。`float` 只有 64 位，必须截断，存下的是最接近真值的近似。

**结构。** IEEE 754（浮点数的国际标准）双精度（binary64）：1 位符号 + 11 位指数 + 52 位尾数，再加一个隐含的首位 1，共 53 位有效数字，值 ≈ ±1.尾数 × 2^指数。`0.1` 存成 3602879701896397 / 2^55，比真值多一点点；`0.2` 同理；相加后再取最近的近似，得到 `0.30000000000000004`。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="34.0" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1 位</text>
<rect x="15" y="28" width="38" height="32" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="34.0" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">符号</text>
<text x="97.0" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">11 位</text>
<rect x="53" y="28" width="88" height="32" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="97.0" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">指数</text>
<text x="233.0" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">52 位</text>
<rect x="141" y="28" width="184" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="233.0" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">尾数</text>
<text x="170" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0.1 的二进制 0.000110011001100... 无穷循环</text>
<text x="170" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只留 53 位有效数字</text>
<text x="170" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">= 3602879701896397 / 2^55</text>
<text x="170" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">= 0.1000000000000000055511...</text>
<text x="170" y="178" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0.1 + 0.2 = 0.30000000000000004</text>
</svg>
```

**细节。**

- 53 位有效数字，所以 2^53 以上的整数不能再逐个表示：`float(2**53) + 1 == float(2**53)`。

**坑。** 别用 `==` 比较浮点数，用 `math.isclose(a, b)`（默认相对误差 1e-9）。

**例题：** LC 2469 温度转换（同类：LC 1344 时钟指针的夹角）

给四舍五入到两位小数的摄氏度 `celsius`，返回 `[开氏度, 华氏度]`：开氏度 = celsius + 273.15，华氏度 = celsius * 1.80 + 32.00。与标准答案误差不超过 10^-5 算对。

```python
def convert_temperature(celsius: float) -> list[float]:
    return [celsius + 273.15, celsius * 1.80 + 32.00]
```
