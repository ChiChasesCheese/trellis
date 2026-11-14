---
slug: roman-to-integer
---
## Q
**LC 13 罗马数字转整数**｜Easy

把罗马数字字符串转成整数，小数在大数左边表示减法（`IV=4`、`IX=9`、`XL`、`XC`、`CD`、`CM`）。

## A
**一句话。** 从右往左扫，当前值比右邻小就减，否则加。

**图解。** 从右往左扫，比右邻小的字符取负号，其余取正号。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 150">
<polyline points="288,12 50,12" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="50.0,12.0 56.0,9.0 56.0,15.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="169.0" y="26" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">从右往左，比右邻小就减</text>
<rect x="50" y="34" width="34" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="67.0" y="51.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">M</text>
<rect x="84" y="34" width="34" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="51.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">C</text>
<rect x="118" y="34" width="34" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="135.0" y="51.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">M</text>
<rect x="152" y="34" width="34" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="169.0" y="51.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">X</text>
<rect x="186" y="34" width="34" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="203.0" y="51.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">C</text>
<rect x="220" y="34" width="34" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="237.0" y="51.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">I</text>
<rect x="254" y="34" width="34" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="271.0" y="51.32" text-anchor="middle" font-size="12" font-family="ui-monospace,Menlo,monospace" fill="currentColor">V</text>
<text x="67.0" y="80" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1000</text>
<text x="101.0" y="80" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">100</text>
<text x="135.0" y="80" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1000</text>
<text x="169.0" y="80" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10</text>
<text x="203.0" y="80" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">100</text>
<text x="237.0" y="80" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="271.0" y="80" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="50" y="90" width="34" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="67.0" y="106.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+</text>
<rect x="84" y="90" width="34" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="106.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">−</text>
<rect x="118" y="90" width="34" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="135.0" y="106.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+</text>
<rect x="152" y="90" width="34" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="169.0" y="106.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">−</text>
<rect x="186" y="90" width="34" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="203.0" y="106.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+</text>
<rect x="220" y="90" width="34" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="237.0" y="106.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">−</text>
<rect x="254" y="90" width="34" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="271.0" y="106.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+</text>
<text x="42" y="51" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s</text>
<text x="42" y="80" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">值</text>
<text x="42" y="106" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">符号</text>
<text x="50" y="140" text-anchor="start" font-size="10" font-family="sans-serif" fill="currentColor">1000 − 100 + 1000 − 10 + 100 − 1 + 5 = 1994</text>
</svg>

```python
def roman_to_int(s):
    val = {"I": 1, "V": 5, "X": 10, "L": 50,
           "C": 100, "D": 500, "M": 1000}
    total = prev = 0         # prev：右邻的值，最右边当 0
    for ch in reversed(s):
        v = val[ch]
        total += v if v >= prev else -v
        prev = v
    return total
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 比较写成 `v > prev`：`"II"` 变成 `1 - 1 = 0`，应为 `2`。
- 从左往右扫：要看右邻，最后一个字符容易越界或漏加。

**追问。**
- 怎么校验是否合法？：正则 `^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$`。

**同模式。** LC 12 整数转罗马数字、LC 8 字符串转换整数、LC 168 Excel 表列名称、LC 171 Excel 表列序号
