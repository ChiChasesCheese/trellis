---
slug: adding-spaces-to-a-string
---
## Q
**LC 2109 向字符串添加空格**｜Medium

给字符串 `s` 和严格递增的下标数组 `spaces`，在每个下标对应的字符之前插入一个空格，返回新字符串。

## A
**一句话。** 双指针：一个扫 `s`，一个指向下一个要插空格的位置，到了就先放空格；结果攒进列表最后一次拼接。

**图解。** `i` 扫字符串，`j` 指向下一个要插空格的位置，两者相等就先放空格。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 160">
<rect x="15" y="40" width="14" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="22.0" y="55.6" text-anchor="middle" font-size="10" font-family="ui-monospace,Menlo,monospace" fill="currentColor">L</text>
<rect x="29" y="40" width="14" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="36.0" y="55.6" text-anchor="middle" font-size="10" font-family="ui-monospace,Menlo,monospace" fill="currentColor">e</text>
<rect x="43" y="40" width="14" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50.0" y="55.6" text-anchor="middle" font-size="10" font-family="ui-monospace,Menlo,monospace" fill="currentColor">e</text>
<rect x="57" y="40" width="14" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="64.0" y="55.6" text-anchor="middle" font-size="10" font-family="ui-monospace,Menlo,monospace" fill="currentColor">t</text>
<rect x="71" y="40" width="14" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78.0" y="55.6" text-anchor="middle" font-size="10" font-family="ui-monospace,Menlo,monospace" fill="currentColor">c</text>
<rect x="85" y="40" width="14" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="92.0" y="55.6" text-anchor="middle" font-size="10" font-family="ui-monospace,Menlo,monospace" fill="currentColor">o</text>
<rect x="99" y="40" width="14" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="106.0" y="55.6" text-anchor="middle" font-size="10" font-family="ui-monospace,Menlo,monospace" fill="currentColor">d</text>
<rect x="113" y="40" width="14" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="120.0" y="55.6" text-anchor="middle" font-size="10" font-family="ui-monospace,Menlo,monospace" fill="currentColor">e</text>
<rect x="127" y="40" width="14" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="134.0" y="55.6" text-anchor="middle" font-size="10" font-family="ui-monospace,Menlo,monospace" fill="currentColor">H</text>
<rect x="141" y="40" width="14" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="148.0" y="55.6" text-anchor="middle" font-size="10" font-family="ui-monospace,Menlo,monospace" fill="currentColor">e</text>
<rect x="155" y="40" width="14" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="162.0" y="55.6" text-anchor="middle" font-size="10" font-family="ui-monospace,Menlo,monospace" fill="currentColor">l</text>
<rect x="169" y="40" width="14" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="176.0" y="55.6" text-anchor="middle" font-size="10" font-family="ui-monospace,Menlo,monospace" fill="currentColor">p</text>
<rect x="183" y="40" width="14" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="190.0" y="55.6" text-anchor="middle" font-size="10" font-family="ui-monospace,Menlo,monospace" fill="currentColor">s</text>
<rect x="197" y="40" width="14" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="204.0" y="55.6" text-anchor="middle" font-size="10" font-family="ui-monospace,Menlo,monospace" fill="currentColor">M</text>
<rect x="211" y="40" width="14" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="218.0" y="55.6" text-anchor="middle" font-size="10" font-family="ui-monospace,Menlo,monospace" fill="currentColor">e</text>
<rect x="225" y="40" width="14" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="232.0" y="55.6" text-anchor="middle" font-size="10" font-family="ui-monospace,Menlo,monospace" fill="currentColor">L</text>
<rect x="239" y="40" width="14" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="246.0" y="55.6" text-anchor="middle" font-size="10" font-family="ui-monospace,Menlo,monospace" fill="currentColor">e</text>
<rect x="253" y="40" width="14" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260.0" y="55.6" text-anchor="middle" font-size="10" font-family="ui-monospace,Menlo,monospace" fill="currentColor">a</text>
<rect x="267" y="40" width="14" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="274.0" y="55.6" text-anchor="middle" font-size="10" font-family="ui-monospace,Menlo,monospace" fill="currentColor">r</text>
<rect x="281" y="40" width="14" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="288.0" y="55.6" text-anchor="middle" font-size="10" font-family="ui-monospace,Menlo,monospace" fill="currentColor">n</text>
<line x1="127" y1="34" x2="127" y2="70" stroke-width="2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="127" y="82" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">8</text>
<line x1="197" y1="34" x2="197" y2="70" stroke-width="2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="197" y="82" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">13</text>
<line x1="225" y1="34" x2="225" y2="70" stroke-width="2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="225" y="82" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">15</text>
<polyline points="204.0,26 204.0,40" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="204.0,40.0 201.0,34.0 207.0,34.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="204.0" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i</text>
<rect x="110" y="100" width="34" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="127.0" y="116.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="144" y="100" width="34" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="161.0" y="116.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">13</text>
<rect x="178" y="100" width="34" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="195.0" y="116.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">15</text>
<text x="102" y="116" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">spaces</text>
<polyline points="161.0,136 161.0,124" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="161.0,124.0 164.0,130.0 158.0,130.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="161.0" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">j</text>
<text x="222" y="116" text-anchor="start" font-size="10" font-family="ui-monospace,Menlo,monospace" style="fill:var(--accent,#3b6fd4)">i == spaces[j]</text>
<text x="222" y="134" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">先放空格，j += 1</text>
</svg>

```python
def add_spaces(s, spaces):
    out, j = [], 0
    for i, c in enumerate(s):
        if j < len(spaces) and spaces[j] == i:
            out.append(" ")   # spaces 升序，指针只前进
            j += 1
        out.append(c)
    return "".join(out)
```

**复杂度。** 时间 `O(n + k)`，空间 `O(n + k)`。

**易错点。**
- 用 `s = s[:i] + " " + s[i:]` 反复插入：每次复制整串，`O(n·k)`，而且插入后后面的下标全部偏移。
- 用 `+=` 拼字符串：最坏退化成平方，改用列表加 `join`。

**追问。**
- 也可以按段切片？：`s[prev:p]` 逐段加入列表再用空格 `join`，同样线性。
- 原地修改（C 风格字符数组）？：先算新长度，从后往前写，避免覆盖未处理的字符。

**同模式。** LC 88 合并两个有序数组、LC 1768 交替合并字符串
