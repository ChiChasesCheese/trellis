---
id: lct-learn-greedy-2-3
node: greedy.2.3
type: qa
step: 1
---
## Q
**贪心算法 › 区间贪心 › 区间选点**｜学习卡

套路是什么？

## A
**一句话。** 区间选点：按右端点排序，新区间够不着上一个点就在它的右端点新放一个点，这样的点覆盖后面区间的机会最大。

下图：LC 452，箭放在右端点上，能顺带射中的后续区间最多。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="66" y="20" width="80" height="16" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="62" y="32" text-anchor="end" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[1,6]</text>
<rect x="82" y="44" width="96" height="16" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="78" y="56" text-anchor="end" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[2,8]</text>
<rect x="162" y="68" width="80" height="16" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="158" y="80" text-anchor="end" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[7,12]</text>
<rect x="210" y="92" width="96" height="16" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="206" y="104" text-anchor="end" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">[10,16]</text>
<line x1="146" y1="12" x2="146" y2="112" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<text x="146" y="10" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">箭</text>
<line x1="242" y1="12" x2="242" y2="112" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<text x="242" y="10" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">箭</text>
<line x1="50" y1="116" x2="306" y2="116" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="50" y="130" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="82" y="130" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="114" y="130" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<text x="146" y="130" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<text x="178" y="130" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8</text>
<text x="210" y="130" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10</text>
<text x="242" y="130" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">12</text>
<text x="274" y="130" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">14</text>
<text x="306" y="130" text-anchor="middle" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">16</text>
<text x="170" y="146" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">按右端点排序；够不着上一支箭，就在右端点射新的</text>
</svg>

```python
def min_arrows(points):          # 闭区间，一箭可射爆所含的气球
    arrows = 0
    last = -inf                  # 上一支箭的位置
    for l, r in sorted(points, key=itemgetter(1)):
        if l > last:             # 够不着：新射一支，射在右端点
            arrows += 1
            last = r
    return arrows
```

**要点。**
- 为什么对？：按右端点排序，当前区间的右端点是还没被射爆的区间里最靠左的，箭射得越靠右越可能顺带射爆后面的，射在右端点最划算。
- LC 452 与 LC 435 有何关系？：最少箭数 = 最多两两无公共点的区间数；但 LC 452 端点接触算同一支箭（`l > last`），LC 435 端点接触不算重叠（`l >= end`）。
- 气球改成开区间怎么改？：端点相接不能共用一支箭，条件改为 `l >= last`。

**易错点。**
- 条件写成 `l >= last`：闭区间端点相接可共用，`[[1,2],[2,3],[3,4],[4,5]]` 得 `4`，应为 `2`。
- 按左端点排序却不收缩右边界：`[[1,10],[2,3],[4,5]]` 一直用 `10` 当边界，得 `1`，应为 `2`。
- 排序用 `a[1] - b[1]` 当比较器：定宽整数语言里会溢出。

**对应题目。** LC 452 用最少数量的箭引爆气球
