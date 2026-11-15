---
slug: path-with-minimum-effort
---
## Q
**LC 1631 最小体力消耗路径**｜Medium

网格 `heights`，从左上走到右下，可上下左右移动。一条路径的体力 = 相邻格高度差绝对值的最大值，求最小体力。

## A
**一句话。** 路径代价是边权的最大值而不是和，Dijkstra 照样成立：松弛改成 `max(d, |Δh|)`，第一次弹出终点即答案。

**图解。** 深色是最优路径 `1→3→5→3→5`，相邻高度差最大为 2；穿过中间的 `8` 要付出 5 以上。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 190">
<rect x="26" y="12" width="34" height="34" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="43.0" y="33.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="60" y="12" width="34" height="34" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="77.0" y="33.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="94" y="12" width="34" height="34" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="111.0" y="33.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="26" y="50" width="34" height="34" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="43.0" y="71.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="60" y="50" width="34" height="34" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="77.0" y="71.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="94" y="50" width="34" height="34" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="111.0" y="71.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="26" y="88" width="34" height="34" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="43.0" y="109.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="60" y="88" width="34" height="34" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="77.0" y="109.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="94" y="88" width="34" height="34" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="111.0" y="109.1" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="16" y="136" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">深色路径：差值 2、2、2、2</text>
<text x="16" y="154" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">灰格 8：走它至少差 5</text>
<text x="16" y="172" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor" font-weight="600">答案 2</text>
</svg>

```python
def minimum_effort_path(heights):
    m, n = len(heights), len(heights[0])
    dist = [[inf] * n for _ in range(m)]
    dist[0][0] = 0
    pq = [(0, 0, 0)]
    while pq:
        d, i, j = heappop(pq)
        if (i, j) == (m - 1, n - 1):
            return d               # 第一次弹出即最优
        if d > dist[i][j]:
            continue               # 过期条目
        for x, y in ((i+1, j), (i-1, j),
                     (i, j+1), (i, j-1)):
            if 0 <= x < m and 0 <= y < n:
                step = abs(heights[x][y] - heights[i][j])
                nd = max(d, step)  # 代价取最大值
                if nd < dist[x][y]:
                    dist[x][y] = nd
                    heappush(pq, (nd, x, y))
```

**复杂度。** 时间 `O(mn log(mn))`，空间 `O(mn)`。

**易错点。**
- 松弛写成 `d + step`：那是路径和，这里要的是相邻差的最大值。
- 只能向右、向下走：最优路径可能要绕回来，必须四个方向。

**追问。**
- 别的做法？：二分体力 `t` 后 BFS 只走差值 `<= t` 的边；或把边按差值排序用并查集逐条加，起终点连通时的边权即答案。
- 为什么 Dijkstra 对 max 也对？：`max` 和加法一样单调不减，先弹出的点代价不会再被改小。

**同模式。** LC 778 水位上升的泳池中游泳、LC 743 网络延迟时间、LC 1102 得分最高的路径
