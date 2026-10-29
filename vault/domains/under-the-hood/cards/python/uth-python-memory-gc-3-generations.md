---
id: uth-python-memory-gc-3-generations
node: python.memory-gc
type: qa
step: 3
---
## Q
**GC 什么时候运行**｜Python · CPython 3.14.8

`gc.get_threshold()` 返回 `(2000, 10, 10)`，这三个数是什么意思？

## A
**背景。** 每次都检查所有容器对象太贵。经验是大多数对象朝生夕灭，活下来的往往活得很久。所以只频繁检查「年轻」的，老的少查。

**结构。** 三代（generation）的分代 GC：新对象进第 0 代，扛过一次回收就晋升到下一代。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<rect x="10" y="30" width="90" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="55" y="51" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第 0 代</text>
<line x1="102" y1="47" x2="123" y2="47" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="123.0,47.0 117.0,50.0 117.0,44.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="118" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">晋升</text>
<rect x="125" y="30" width="90" height="34" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="51" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第 1 代</text>
<line x1="217" y1="47" x2="238" y2="47" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="238.0,47.0 232.0,50.0 232.0,44.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="233" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">晋升</text>
<rect x="240" y="30" width="90" height="34" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="285" y="51" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第 2 代</text>
<text x="55" y="86" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新对象从这里开始</text>
<text x="55" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分配-释放&gt;2000</text>
<text x="170" y="86" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第 0 代回收</text>
<text x="170" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">超过 10 次</text>
<text x="285" y="86" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第 1 代回收</text>
<text x="285" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">超过 10 次</text>
<text x="170" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">扛过一次回收就往后一代 越老查得越少</text>
</svg>
```

**细节。**

- 分配数减释放数超过 2000，回收第 0 代。
- 第 0 代回收超过 10 次，这一轮再带上第 1 代，第 2 代同理。
- 完整回收还要求新晋升的老对象超过存量的 1/4。
- 3.14.0 到 3.14.4 曾用增量 GC，3.14.5 起退回分代。

**为什么。** 全量扫描随老对象增多而变贵，所以越做越少。

**对应 LeetCode：** 无直接对应的题
