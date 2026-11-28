---
id: lct-learn-greedy-2-6
node: greedy.2.6
type: qa
step: 1
---
## Q
**贪心算法 › 区间贪心 › 其他区间贪心**｜学习卡

套路是什么？

## A
**一句话。** 区间排序后一遍扫描：起点升序、同起点终点降序，终点没超过已见最大终点的区间就是被覆盖的。

下图：LC 1288，排序后只需记住已见的最大终点。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<rect x="78" y="20" width="84" height="16" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="74" y="32" text-anchor="end" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[1,4]</text>
<rect x="106" y="44" width="168" height="16" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="102" y="56" text-anchor="end" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[2,8]</text>
<rect x="134" y="68" width="84" height="16" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="130" y="80" text-anchor="end" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[3,6]</text>
<line x1="274" y1="14" x2="274" y2="96" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<text x="278" y="22" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">max_end</text>
<text x="170" y="136" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[3,6] 终点 6 ≤ max_end 8：被覆盖</text>
<line x1="50" y1="100" x2="302" y2="100" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="50" y="114" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="78" y="114" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="106" y="114" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="134" y="114" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="162" y="114" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<text x="190" y="114" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<text x="218" y="114" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<text x="246" y="114" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<text x="274" y="114" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8</text>
<text x="302" y="114" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">9</text>
<text x="170" y="154" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">起点升序、同起点终点降序；终点超过 max_end 才保留</text>
</svg>

```python
def remove_covered_intervals(intervals):
    intervals.sort(key=lambda iv: (iv[0], -iv[1]))
    kept = 0
    max_end = 0
    for _, end in intervals:
        if end > max_end:            # 超出前面所有区间：没被覆盖
            kept += 1
            max_end = end
    return kept
```

**要点。**
- 为什么对？：起点升序保证前面区间的起点都不晚于当前，只需比终点；同起点让长的在前，短的紧随其后就被识别为覆盖。
- 要返回剩下的区间本身怎么改？：保留时把区间追加进结果，其余不变。

**易错点。**
- 同起点终点升序（默认排序）：`[[1,2],[1,4]]` 得 `2`，应为 `1`。
- 终点相等也保留（`>=`）：`[[1,4],[2,4]]` 得 `2`，应为 `1`。

**对应题目。** LC 1288 删除被覆盖区间
