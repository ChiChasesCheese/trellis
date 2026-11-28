---
id: lct-learn-graph-2-2
node: graph.2.2
type: qa
step: 1
---
## Q
**图论算法 › 拓扑排序 › 在拓扑序上 DP**｜学习卡

套路是什么？

## A
**一句话。** 拓扑序上的 DP：按拓扑序处理节点，每个节点的值由所有前驱的值合并（取最大），处理完再推给后继。

下图：LC 2050，按拓扑序处理，每门课的开始时间取所有先修课完成时间的最大值。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<line x1="62.5" y1="43.6" x2="157.5" y2="71.4" stroke-width="1.2" stroke="currentColor"/>
<polygon points="157.5,71.4 150.6,72.5 152.3,66.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="62.5" y1="106.4" x2="157.5" y2="78.6" stroke-width="1.2" stroke="currentColor"/>
<polygon points="157.5,78.6 152.3,83.2 150.6,77.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="183.0" y1="75.0" x2="267.0" y2="75.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="267.0,75.0 260.7,78.0 260.7,72.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<circle cx="50" cy="40" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="44" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="50" cy="110" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="114" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="170" cy="75" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="79" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<circle cx="280" cy="75" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="280" y="79" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">4</text>
<text x="50" y="18" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">用时 3，完成 3</text>
<text x="50" y="140" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">用时 2，完成 2</text>
<text x="170" y="112" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">start = max(3, 2) = 3</text>
<text x="170" y="126" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">用时 5，完成 8</text>
<text x="280" y="50" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">start = 8</text>
</svg>

```python
def minimum_time(n, relations, time):
    g = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for a, b in relations:
        g[a].append(b)
        indeg[b] += 1
    start = [0] * (n + 1)            # 最早开始月份
    q = deque(i for i in range(1, n + 1) if indeg[i] == 0)
    ans = 0
    while q:
        u = q.popleft()
        fin = start[u] + time[u - 1]
        ans = max(ans, fin)
        for v in g[u]:
            start[v] = max(start[v], fin)   # 要等所有先修课
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return ans
```

**要点。**
- 为什么对？：节点出队时所有前驱都已处理，`start[u]` 已经是最终值；后继的开始时间是各前驱完成时间的最大值。
- LC 1136 怎么改？：按层 Kahn：每一层入度为 `0` 的课是一个学期，层数即答案；修完的课数不足 `n` 说明有环，返回 `-1`。

**易错点。**
- 答案取最后出队那门课的完成时间：`n = 3`、无先修、`time = [1,9,4]` 得 `4`，应为 `9`。
- 后继开始时间覆盖而不取最大：示例二得 `7`，应为 `12`。
- LC 1136 每个节点出队都 `sem += 1`：同一批可并行修，按层计一个学期。

**对应题目。** LC 1136 平行课程、LC 2050 并行课程 III
