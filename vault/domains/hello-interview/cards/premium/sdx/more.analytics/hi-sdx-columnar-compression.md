---
id: hi-sdx-columnar-compression
node: more.analytics
type: qa
step: 6
---
## Q
**列存压缩：字典编码加游程编码**｜补充 · 分析型系统：OLAP、数仓与批处理 · 必会

面试官：「1 亿行的订单表里有一列 `country`，只有 200 个不同取值。列存为什么能把它压得很小？先按这一列排序之后又会怎样？」

## A
**结论。** 先做字典编码（dictionary encoding），再做游程编码（run-length encoding，RLE）。排序把相同值排在一起，游程就从 1 亿个值缩成 200 段。

**要点。**
- **字典编码：** 把重复的字符串换成小整数。200 个取值一个字节就够，1 亿行约 100 MB；原始字符串按平均 8 字节算是 800 MB。
- **游程编码：** 连续相同的值存成「值 + 次数」。同一列的值类型相同、取值有限，列存才有这个条件；行存里这一列被其他列隔开，做不了。
- **位图：** 对低基数列，每个取值一张位图，`WHERE country IN (...)` 变成位图的按位或，不用逐行比较。
- **排序放大效果：** 排序后相同值相邻，1 亿行变成 200 段，每段几个字节。
- **代价：** 一份数据只有一种排序。要把排序键对齐最常用的过滤列，或者在不同副本上存不同排序。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">未排序（8 行的 country 列）：游程很短</text>
<rect x="8" y="26" width="38" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="27.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CN</text>
<rect x="49" y="26" width="38" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="68.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">US</text>
<rect x="90" y="26" width="38" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="109.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CN</text>
<rect x="131" y="26" width="38" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="150.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">DE</text>
<rect x="172" y="26" width="38" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="191.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">US</text>
<rect x="213" y="26" width="38" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="232.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CN</text>
<rect x="254" y="26" width="38" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="273.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">DE</text>
<rect x="295" y="26" width="38" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="314.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">US</text>
<text x="8" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">按 country 排序后：相同值相邻</text>
<rect x="8" y="92" width="38" height="26" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="27.0" y="109.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CN</text>
<rect x="49" y="92" width="38" height="26" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="68.0" y="109.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CN</text>
<rect x="90" y="92" width="38" height="26" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="109.0" y="109.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CN</text>
<rect x="131" y="92" width="38" height="26" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="150.0" y="109.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">US</text>
<rect x="172" y="92" width="38" height="26" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="191.0" y="109.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">US</text>
<rect x="213" y="92" width="38" height="26" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="232.0" y="109.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">US</text>
<rect x="254" y="92" width="38" height="26" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="273.0" y="109.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">DE</text>
<rect x="295" y="92" width="38" height="26" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="314.0" y="109.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">DE</text>
<text x="8" y="148" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">游程编码后只存 3 段</text>
<rect x="8" y="156" width="100" height="26" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="58.0" y="173.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CN × 3</text>
<rect x="116" y="156" width="100" height="26" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="166.0" y="173.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">US × 3</text>
<rect x="224" y="156" width="100" height="26" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="274.0" y="173.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">DE × 2</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1 亿行 200 个取值 → 约 200 段</text>
</svg>

**面试里这样说。** 「列存先把低基数列做字典编码，再按排序键做游程编码；按 `country` 排序后，1 亿行只剩 200 段。代价是一份数据只有一种排序，所以排序键要选最常用的过滤列。」

**易错。**
- **排序列选错：** 排序键不是常用过滤列，压缩收益有限，范围扫描也没法跳过数据。
- **对高基数列硬做字典：** 订单号这种几乎每行都不同的列，字典和原值一样大，没有收益。
