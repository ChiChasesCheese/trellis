---
id: lct-learn-data-structures-5-5
node: data-structures.5.5
type: qa
step: 1
---
## Q
**常用数据结构 › 堆（优先队列） › 反悔堆**｜学习卡

套路是什么？

## A
**一句话。** 反悔堆：先按最省事的方式做选择并把它放进堆，资源不够时，从堆里取出代价最大（或最小）的一次选择反悔，换成另一种方式。

下图：先按最省事的方式选，资源不够时从堆里取出最不划算的一次反悔。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 260">
<rect x="89.0" y="7.5" width="161.9" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">下一段上坡 d（下坡跳过）</text>
<rect x="83.6" y="53.5" width="172.7" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="70.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">先用梯子：push d 进小根堆</text>
<polygon points="109.6,114.0 118.6,101.5 221.4,101.5 230.4,114.0 221.4,126.5 118.6,126.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">堆大小 &gt; 梯子数？</text>
<rect x="89.0" y="153.5" width="161.9" height="25" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="170.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">反悔：弹最小的 d，改用砖</text>
<polygon points="136.1,214.0 145.1,201.5 194.9,201.5 203.9,214.0 194.9,226.5 145.1,226.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="218.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">砖 &lt; 0？</text>
<rect x="262.0" y="201.5" width="60" height="25" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="292" y="218.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">返回 i</text>
<path d="M 170.0 32.5 L 170.0 53.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,53.5 167.0,47.2 173.0,47.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 170.0 78.5 L 170.0 101.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,101.5 167.0,95.2 173.0,95.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 170.0 126.5 L 170.0 153.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,153.5 167.0,147.2 173.0,147.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="178.0" y="144.0" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是</text>
<path d="M 170.0 178.5 L 170.0 201.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,201.5 167.0,195.2 173.0,195.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 203.9 214.0 L 262.0 214.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="262.0,214.0 255.7,217.0 255.7,211.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="235" y="208" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是</text>
<path d="M 109.6 114.0 L 20.0 114.0 L 20.0 20.0 L 89.0 20.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="89.0,20.0 82.7,23.0 82.7,17.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="12" y="70" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<path d="M 136.1 214.0 L 40.0 214.0 L 40.0 20.0 L 89.0 20.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="89.0,20.0 82.7,23.0 82.7,17.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="50" y="190" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<text x="170" y="252" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">梯子永远留给最高的那几段</text>
</svg>

```python
def furthest_building(h, bricks, ladders):
    pq = []                          # 小根堆：用了梯子的攀爬高度
    for i in range(len(h) - 1):
        d = h[i + 1] - h[i]
        if d <= 0:
            continue                 # 下坡或平地免费
        heappush(pq, d)              # 先假设用梯子
        if len(pq) > ladders:        # 梯子不够：最小的一次反悔用砖
            bricks -= heappop(pq)
            if bricks < 0:           # 砖也不够，走不到 i + 1
                return i
    return len(h) - 1
```

**要点。**
- 为什么对？：梯子可以抵消任意高度，应留给最高的几次攀爬；堆里始终是当前最高的 `ladders` 次，被挤出来的最小一次改用砖，总用砖量最小。
- LC 871 怎么改？：把路过的加油站的油量放进大根堆，不先加油；油不够到下一站时，反悔取堆里最大的一站补油，计一次，堆空仍不够就返回 `-1`。

**易错点。**
- 返回下标：在 `i → i + 1` 这步失败，能到的最远建筑是 `i`，不是 `i + 1`；全部走完才是 `len(h) - 1`。
- 871 终点当作一座油量为 `0` 的加油站：终点要放进站点列表，否则最后一段不检查。
- 堆的方向：1642 用小根堆（弹出最小的攀爬），871 用大根堆（弹出最大的油量），写反会得到最差解。

**对应题目。** LC 1642 可以到达的最远建筑、LC 871 最低加油次数
