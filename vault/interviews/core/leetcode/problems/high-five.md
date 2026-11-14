---
slug: high-five
---
## Q
**LC 1086 前五科的均分**｜Easy

给 `items[i] = [id, score]`，每个学生至少 5 个分数。按 `id` 升序返回每人最高 5 个分数的平均分（整数除法）。

## A
**一句话。** 按学生分组，每人维护大小为 5 的小顶堆，超过 5 个就弹出最小的，剩下的就是最高的 5 个。

**图解。** 一个学生的小顶堆（按大小排开画）：推入新分数后超过 5 个，就弹出最小的。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 150">
<rect x="76" y="24" width="36" height="26" rx="2" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="94.0" y="41.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">60</text>
<rect x="112" y="24" width="36" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130.0" y="41.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">65</text>
<rect x="148" y="24" width="36" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="166.0" y="41.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">87</text>
<rect x="184" y="24" width="36" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="202.0" y="41.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">91</text>
<rect x="220" y="24" width="36" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="238.0" y="41.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">92</text>
<rect x="272" y="24" width="36" height="26" rx="3" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="290.0" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">100</text>
<polyline points="270,37 258,37" fill="none" stroke-width="1.4" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="258.0,37.0 264.0,34.0 264.0,40.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="290.0" y="16" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">推入</text>
<text x="68" y="41" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">堆</text>
<polyline points="94.0,50 94.0,74" fill="none" stroke-width="1.4" style="stroke:var(--dim,#6b7280)"/>
<polygon points="94.0,74.0 91.0,68.0 97.0,68.0" style="fill:var(--dim,#6b7280)"/>
<text x="100.0" y="70" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">超过 5 个，弹出堆顶 60</text>
<rect x="76" y="82" width="36" height="26" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="94.0" y="99.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">65</text>
<rect x="112" y="82" width="36" height="26" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="130.0" y="99.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">87</text>
<rect x="148" y="82" width="36" height="26" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="166.0" y="99.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">91</text>
<rect x="184" y="82" width="36" height="26" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="202.0" y="99.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">92</text>
<rect x="220" y="82" width="36" height="26" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="238.0" y="99.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">100</text>
<text x="68" y="99" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最高 5 个</text>
<text x="76" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">435 // 5 = 87</text>
</svg>

```python
def high_five(items):
    top = defaultdict(list)    # id -> 大小为 5 的小顶堆
    for sid, score in items:
        heappush(top[sid], score)
        if len(top[sid]) > 5:
            heappop(top[sid])  # 踢掉当前最小的
    return [[sid, sum(h) // 5]
            for sid, h in sorted(top.items())]
```

**复杂度。** 时间 `O(n log 5 + k log k)`，`k` 是学生数；空间 `O(k)`。

**易错点。**
- 用大顶堆：要的是「最大的 5 个」，留下它们得用小顶堆，堆顶才是要淘汰的。
- 忘了按 `id` 排序输出：字典遍历顺序不是 `id` 顺序。

**追问。**
- 分数范围只有 0–100？：每人一个计数数组，从 100 往下取 5 个，`O(n)`。
- 数据流不断到达？：堆就是在线结构，每来一个分数 `O(log 5)` 更新。

**同模式。** LC 215 数组中的第K个最大元素、LC 703 数据流中的第 K 大元素、LC 347 前 K 个高频元素
