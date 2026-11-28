---
id: lct-learn-graph-5
node: graph.5
type: qa
step: 1
---
## Q
**图论算法 › 欧拉路径/欧拉回路**｜学习卡

套路是什么？

## A
**一句话。** 欧拉路径（Hierholzer）：DFS 每次走最小的未用边，走进死胡同才把点入结果，最后整体反转。

下图：LC 332，走进死胡同才把点加入结果；反转后就是欧拉路径。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 165">
<line x1="78.5" y1="62.4" x2="151.5" y2="32.6" stroke-width="1.2" stroke="currentColor"/>
<polygon points="151.5,32.6 146.8,37.8 144.5,32.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="78.5" y1="77.6" x2="151.5" y2="107.4" stroke-width="1.2" stroke="currentColor"/>
<polygon points="151.5,107.4 144.5,107.8 146.8,102.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<circle cx="60" cy="70" r="20" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="60" y="74" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">JFK</text>
<circle cx="170" cy="25" r="20" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="29" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">KUL</text>
<circle cx="170" cy="115" r="20" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="119" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">NRT</text>
<path d="M 150 125 C 110 140, 70 120, 62 92" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="62.0,92.0 66.4,97.4 60.6,98.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="160" y="70" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先走字典序小的</text>
<text x="210" y="30" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">KUL 死胡同：先入</text>
<text x="210" y="60" text-anchor="start" font-size="10" font-family="sans-serif" fill="currentColor">route：KUL JFK NRT JFK</text>
<text x="210" y="84" text-anchor="start" font-size="10" font-family="sans-serif" fill="currentColor">反转：</text>
<text x="210" y="100" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">JFK NRT JFK KUL</text>
<text x="170" y="160" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">后序入结果：死胡同一定是终点，最后整体反转</text>
</svg>

```python
def find_itinerary(tickets):
    g = defaultdict(list)
    for a, b in sorted(tickets, reverse=True):
        g[a].append(b)               # 逆序放，pop() 取到最小
    route = []

    def dfs(u):
        while g[u]:
            dfs(g[u].pop())
        route.append(u)              # 后序：死胡同先入

    dfs("JFK")
    return route[::-1]
```

**要点。**
- 为什么对？：先卡死的点必是路径的终点，它先入结果排在最后；其余走通的环按尝试顺序插在前面，后序反转后恰是欧拉路径。
- LC 2097 怎么改？：没有字典序要求，起点是出度比入度大 `1` 的点（没有就任取），其余同。

**易错点。**
- 普通贪心不回溯：`[["JFK","KUL"],["JFK","NRT"],["NRT","JFK"]]` 先走 `KUL` 就卡死。
- 忘了反转：`route` 是后序，直接返回是倒序行程。
- 正序存入再 `pop()`：会先走字典序最大的。

**对应题目。** LC 332 重新安排行程
