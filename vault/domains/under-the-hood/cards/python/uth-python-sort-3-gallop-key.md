---
id: uth-python-sort-3-gallop-key
node: python.sort
type: qa
step: 3
---
## Q
**归并时的 galloping 与 key 函数**｜Python · CPython 3.14

两段各 10 万的有序数据，后一段全比前一段小，归并要比较 20 万次吗？`sorted(a, key=f)` 里 `f` 被调用几次？

## A
**背景。** 合并两个有序段，常规做法是每次比较两段的队头、取小的。可如果一段连续很多个都比另一段小，逐个比较就是浪费，直接成块搬过去更省。

**结构。** 一边连续赢 `MIN_GALLOP = 7` 次，就切到 galloping（疾驰）模式：用指数加二分查找（先跳 1、3、7、15 个……，越界后在最后一段里二分）找到边界，再整块拷贝。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<rect x="26" y="70" width="18" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="44" y="70" width="18" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="62" y="70" width="18" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="80" y="70" width="18" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="98" y="70" width="18" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="116" y="70" width="18" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="134" y="70" width="18" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="152" y="70" width="18" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="170" y="70" width="18" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="188" y="70" width="18" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="206" y="70" width="18" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="224" y="70" width="18" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="242" y="70" width="18" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="260" y="70" width="18" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="278" y="70" width="18" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="296" y="70" width="18" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一边连赢 7 次 切到 galloping</text>
<path d="M 35 66 Q 44.0 38.8 53 66" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="53.0,66.0 48.5,61.0 54.3,59.4" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<path d="M 53 66 Q 71.0 37.6 89 66" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="89.0,66.0 83.5,62.1 88.8,59.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<path d="M 89 66 Q 125.0 35.2 161 66" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="161.0,66.0 154.6,64.1 158.6,59.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<path d="M 161 66 Q 233.0 30.4 305 66" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="305.0,66.0 298.3,66.2 300.8,60.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="53" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<line x1="53" y1="98" x2="53" y2="102" stroke-width="1" stroke="currentColor"/>
<text x="89" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<line x1="89" y1="98" x2="89" y2="102" stroke-width="1" stroke="currentColor"/>
<text x="161" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<line x1="161" y1="98" x2="161" y2="102" stroke-width="1" stroke="currentColor"/>
<text x="305" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">15</text>
<line x1="305" y1="98" x2="305" y2="102" stroke-width="1" stroke="currentColor"/>
<line x1="27" y1="132" x2="205" y2="132" stroke-width="1.5" style="stroke:var(--accent,#3b6fd4)"/>
<text x="116" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">整块拷贝</text>
<line x1="206" y1="66" x2="206" y2="128" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="242" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">二分找边界</text>
</svg>
```

**细节。**

- 实测总比较数 200042，一个 20 万有序段是 199999，只多 43 次。
- `key` 对每个元素只调用一次（1000 个元素调用 1000 次）。
- 排序稳定：`sorted(data, key=lambda t: t[1])` 保持同键元素原来的先后。

**为什么。** 数据有大块结构时，逐个比较是浪费；稳定性让你能先按次要键、再按主键排两遍。

**例题：** LC 56 合并区间

给区间集合 `intervals`，合并所有重叠的区间，返回互不重叠且覆盖原输入的区间数组。

```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort(key=lambda pair: pair[0])
    merged: list[list[int]] = []
    for start, end in intervals:
        if merged and start <= merged[-1][1]:  # 与上一个区间重叠（含端点相接）
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
```
