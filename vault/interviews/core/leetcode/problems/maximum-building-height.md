---
slug: maximum-building-height
---
## Q
**LC 1840 最高建筑高度**｜Hard

`n`（`<= 10^9`）栋楼排成一列，第 1 栋高 0，相邻高度差不超过 1，部分楼有高度上限 `[id, maxHeight]`。求能达到的最大高度。

## A
**一句话。** 把 `[1, 0]` 加进限制并按位置排序，左右各扫一遍把每个上限收紧到「邻居上限 + 距离」；两个相邻限制之间先升后降，峰顶是 `(h1 + h2 + 距离) // 2`，最后一个限制之后一路升到 `n`。

**图解。** 收紧后的上限（浅色）之间先升后降，最高的是第 8 栋，高 5。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 326 148">
<text x="42" y="28.1" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">位置</text>
<text x="63.0" y="28.1" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<text x="89.0" y="28.1" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<text x="115.0" y="28.1" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<text x="141.0" y="28.1" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4</text>
<text x="167.0" y="28.1" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">5</text>
<text x="193.0" y="28.1" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">6</text>
<text x="219.0" y="28.1" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">7</text>
<text x="245.0" y="28.1" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">8</text>
<text x="271.0" y="28.1" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">9</text>
<text x="297.0" y="28.1" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">10</text>
<text x="42" y="58.1" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">上限</text>
<rect x="50" y="42" width="26" height="26" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="63.0" y="58.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="76" y="42" width="26" height="26" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="89.0" y="58.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="102" y="42" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="128" y="42" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="154" y="42" width="26" height="26" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="167.0" y="58.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="180" y="42" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="206" y="42" width="26" height="26" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="219.0" y="58.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="232" y="42" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="258" y="42" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="284" y="42" width="26" height="26" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="297.0" y="58.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="42" y="88.1" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">高度</text>
<rect x="50" y="72" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63.0" y="88.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="76" y="72" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="89.0" y="88.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="102" y="72" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="115.0" y="88.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="128" y="72" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="141.0" y="88.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="154" y="72" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="167.0" y="88.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="180" y="72" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="193.0" y="88.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="206" y="72" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="219.0" y="88.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="232" y="72" width="26" height="26" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="245.0" y="88.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="258" y="72" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="271.0" y="88.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="284" y="72" width="26" height="26" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="297.0" y="88.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="16" y="112" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">浅色：左右两遍收紧后的上限</text>
<text x="16" y="130" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">7 与 10 之间先升后降，峰顶 5</text>
</svg>

```python
def max_building(n, restrictions):
    r = sorted(restrictions + [[1, 0]])
    for i in range(1, len(r)):          # 左边传来的上限
        d = r[i][0] - r[i - 1][0]
        r[i][1] = min(r[i][1], r[i - 1][1] + d)
    for i in range(len(r) - 2, -1, -1):  # 右边传来的上限
        d = r[i + 1][0] - r[i][0]
        r[i][1] = min(r[i][1], r[i + 1][1] + d)
    ans = 0
    for (x1, h1), (x2, h2) in pairwise(r):
        # 两点间先升后降，峰顶高度
        ans = max(ans, (h1 + h2 + x2 - x1) // 2)
    return max(ans, r[-1][1] + n - r[-1][0])  # 尾段一直升
```

**复杂度。** 时间 `O(k log k)`（`k` 为限制数），空间 `O(k)`。

**易错点。**
- 只从左往右收紧：右边一个很低的上限会压低左边，必须再从右往左扫一遍。
- 忘了最后一个限制之后的部分：那里没有约束，可以一直升到第 `n` 栋。

**追问。**
- 峰顶公式怎么来？：从 `h1` 升 `t` 步再降到 `h2`，`h1 + t = h2 + (d - t)`，峰高 `(h1 + h2 + d) / 2`，取整向下。
- 和「分发糖果」的关系？：同样是左右两遍把相邻约束传播开，只是这里是上限而那里是下限。

**同模式。** LC 135 分发糖果、LC 1846 减小和重新排列数组后的最大元素
