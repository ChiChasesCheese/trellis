---
id: lct-learn-graph-1-3
node: graph.1.3
type: qa
step: 1
---
## Q
**图论算法 › 图的遍历 › 图论建模 + BFS 最短路**｜学习卡

套路是什么？

## A
**一句话。** 把「局面」当作图上的点、一步操作当作边，从初始局面做 BFS，第一次到达目标的层数就是最少步数；关键是想清楚状态是什么、邻居怎么生成。

下图：把局面当点、一步操作当边，从初始局面 BFS，到达目标的层数就是最少步数。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 165">
<rect x="17" y="67" width="56" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="45" y="84" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0000</text>
<rect x="122" y="12" width="56" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="29" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1000</text>
<line x1="73" y1="80" x2="120" y2="25" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="120.0,25.0 118.2,31.8 113.6,27.9" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<rect x="122" y="49" width="56" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="66" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">9000</text>
<line x1="73" y1="80" x2="120" y2="62" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="120.0,62.0 115.2,67.1 113.0,61.5" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<rect x="122" y="86" width="56" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="103" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0100</text>
<line x1="73" y1="80" x2="120" y2="99" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="120.0,99.0 113.0,99.4 115.3,93.9" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<rect x="122" y="123" width="56" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="140" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">…</text>
<line x1="73" y1="80" x2="120" y2="136" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="120.0,136.0 113.6,133.1 118.2,129.2" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<rect x="232" y="27" width="56" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260" y="44" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1100</text>
<rect x="232" y="77" width="56" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="260" y="94" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0200</text>
<line x1="178" y1="62" x2="230" y2="88" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="230.0,88.0 223.0,87.8 225.7,82.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="178" y1="25" x2="230" y2="40" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<polygon points="230.0,40.0 223.1,41.1 224.7,35.4" style="fill:var(--dim,#6b7280);stroke:var(--dim,#6b7280)" stroke-width="0.5"/>
<text x="45" y="120" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">初始局面</text>
<text x="260" y="122" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">目标：第 2 层</text>
<text x="170" y="158" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">点 = 局面，边 = 一步操作；状态要能哈希，入队即标记</text>
</svg>

```python
def min_steps(start, target, neighbors):
    if start == target:
        return 0
    seen = {start}                   # 状态要可哈希
    q = deque([start])
    steps = 0
    while q:
        steps += 1                   # 本层的邻居都是 steps 步
        for _ in range(len(q)):
            x = q.popleft()
            for y in neighbors(x):   # 题目相关：生成下一步状态
                if y == target:
                    return steps
                if y not in seen:
                    seen.add(y)      # 入队即标记
                    q.append(y)
    return -1
```

**要点。**
- 为什么对？：每步代价相同，BFS 按层扩展，第一次碰到目标就是最少步数；状态总数就是复杂度上界。
- LC 752 怎么改？：状态是四位字符串，邻居是某一位 `±1`（模 `10`），死亡数字当作已访问。
- LC 433 / 127 怎么改？：状态是基因或单词，邻居是改一个字符后仍在词库中的串；词库用集合，访问过就从集合删掉，127 的层数从 `1` 数。
- LC 1345 怎么改？：状态是下标，邻居是 `i±1` 和所有同值下标；同值下标列表展开一次后清空，否则退化成 `O(n^2)`。

**易错点。**
- 出队才标记已访问：同一状态会重复入队，`"0000"` 开始的锁会指数级膨胀。
- 起点就在禁用集合：`"0000"` 是死亡数字应直接返回 `-1`。
- 终点不在词库：127 的 `end_word` 不在词表时直接返回 `0`。

**对应题目。** LC 1345 跳跃游戏 IV、LC 433 最小基因变化、LC 752 打开转盘锁、LC 127 单词接龙
