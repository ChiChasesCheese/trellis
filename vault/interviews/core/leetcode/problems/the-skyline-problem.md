---
slug: the-skyline-problem
---
## Q
**LC 218 天际线问题**｜Hard

`buildings[i] = [left, right, height]`，按 `left` 升序给出。返回天际线的关键点 `[x, y]`：每段水平线的左端点，最后一个点高度为 0。

## A
**一句话。** 扫描线从左往右走过每个端点，最大堆里放「当前覆盖这里的楼」，堆顶高度一变就记一个关键点。

**图解。** 三栋楼叠在一起，天际线每次换成当时最高的那栋，高度变化处（圆点）就是关键点。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 130">
<rect x="50" y="60" width="140" height="50" fill="none" stroke="currentColor" stroke-width="1" style="stroke-opacity:0.4"/>
<rect x="70" y="35" width="80" height="75" fill="none" stroke="currentColor" stroke-width="1" style="stroke-opacity:0.4"/>
<rect x="110" y="50" width="140" height="60" fill="none" stroke="currentColor" stroke-width="1" style="stroke-opacity:0.4"/>
<polyline points="50,110 50,60 70,60 70,35 150,35 150,50 250,50 250,110" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="2.5"/>
<circle cx="50" cy="60" r="4" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="70" cy="35" r="4" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="150" cy="50" r="4" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="250" cy="110" r="4" style="fill:var(--accent,#3b6fd4)"/>
<text x="50" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<text x="70" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<text x="150" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">7</text>
<text x="250" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">12</text>
<text x="160" y="26" font-size="11" font-family="sans-serif" fill="currentColor">关键点 (2,10) (3,15) (7,12) (12,0)</text>
</svg>

```python
def get_skyline(buildings):
    xs = sorted({x for b in buildings for x in b[:2]})
    heap, i, res = [], 0, []           # 堆里放 (-高度, 右端)
    for x in xs:
        while i < len(buildings) and buildings[i][0] <= x:
            l, r, h = buildings[i]
            heappush(heap, (-h, r))    # 左端到了：入堆
            i += 1
        while heap and heap[0][1] <= x:
            heappop(heap)              # 堆顶已结束：懒删除
        h = -heap[0][0] if heap else 0
        if not res or res[-1][1] != h: # 高度变了才记点
            res.append([x, h])
    return res
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 只弹堆顶且不比右端：楼已结束却留在堆顶，高度算错，要循环弹到堆顶仍覆盖 `x`。
- 同一高度重复记点：相邻两栋同高的楼会产生多余关键点，只在高度变化时记。
- 边界写成 `<`：楼是 `[left, right)`，`right == x` 时已不覆盖，要弹出。

**追问。**
- 为什么不用堆删除任意元素？：堆只能删堆顶，用「过期了再弹」的懒删除，每个元素最多进出一次。
- 不用堆能做吗？：分治合并两条天际线（像归并排序），同样 `O(n log n)`。

**同模式。** LC 253 会议室 II、LC 1851 包含每个查询的最小区间、LC 56 合并区间
