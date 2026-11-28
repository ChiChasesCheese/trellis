---
id: lct-learn-greedy-2-4
node: greedy.2.4
type: qa
step: 1
---
## Q
**贪心算法 › 区间贪心 › 不相交区间**｜学习卡

套路是什么？

## A
**一句话。** 不相交区间：最少移除 = 总数 - 最多保留；按右端点排序，起点不早于上一个保留区间右端点的就保留，这样给后面留的空间最大。

下图：LC 435，按右端点排序后贪心保留，最少移除 = 总数 - 最多保留。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="110" y="20" width="50" height="16" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="106" y="32" text-anchor="end" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[1,2]</text>
<rect x="160" y="44" width="50" height="16" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="156" y="56" text-anchor="end" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[2,3]</text>
<rect x="110" y="68" width="100" height="16" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="106" y="80" text-anchor="end" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[1,3]</text>
<rect x="210" y="92" width="50" height="16" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="206" y="104" text-anchor="end" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[3,4]</text>
<text x="216" y="72" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">与上一个重叠：移除</text>
<line x1="60" y1="116" x2="310" y2="116" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="60" y="130" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="110" y="130" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="160" y="130" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="210" y="130" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="260" y="130" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<text x="310" y="130" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<text x="170" y="146" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">按右端点排序，起点 ≥ 上一个保留的右端点就保留</text>
</svg>

```python
def erase_overlap(intervals):
    kept, end = 0, -inf          # 保留数、最后保留区间的右端点
    for l, r in sorted(intervals, key=itemgetter(1)):
        if l >= end:             # 端点接触不算重叠
            kept += 1
            end = r
    return len(intervals) - kept
```

**要点。**
- 为什么对？：交换论证：任一最优解里把第一个区间换成右端点最小的那个，不会与后面的区间冲突，所以每步选结束最早的最优。
- 区间带权重、要最大总权重怎么改？：贪心失效，按右端点排序加二分的 DP（LC 1235）。
- 与 LC 452 有何不同？：同一个贪心，但 LC 452 端点接触算同一箭，条件是 `l > last`；这里端点接触不算重叠，条件 `l >= end`。

**易错点。**
- 按起点排序、遇重叠丢后来的：`[[1,100],[2,3],[4,5]]` 得 `2`，应为 `1`。
- `>=` 写成 `>`：`[[1,2],[2,3]]` 得 `1`，应为 `0`。
- `end` 初值写 `0`：起点可为负，会误丢区间。

**对应题目。** LC 435 无重叠区间
