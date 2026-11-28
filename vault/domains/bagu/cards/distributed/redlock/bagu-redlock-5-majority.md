---
id: bagu-redlock-5-majority
node: a.distributed.redlock
type: qa
step: 5
---
## Q
**容错 · 5 个节点挂 2 个还能加锁吗**｜追问

面试官：「RedLock 部署 5 个节点，挂了 2 个还能加锁吗？挂了 3 个呢？」

## A
**基本回答。** 挂 2 个还能加锁：多数派是 N/2+1 = 3，只要 3 个节点存活就能加到锁。挂 3 个就加不上锁了，此时牺牲可用性，安全性仍然保持。容忍的故障数是 (N−1)/2 向下取整，5 个节点容忍 2 个，容忍 f 个要 2f+1 个节点；任意两次成功加锁的节点集合必有交集，所以不会两个客户端同时持锁。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">挂 2 个：剩 3 个 ≥ 多数派 3，能加锁</text>
<rect x="6" y="26" width="62" height="34" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="37" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 1</text>
<text x="37" y="54.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">存活 ✓</text>
<rect x="70" y="26" width="62" height="34" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="101" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 2</text>
<text x="101" y="54.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">存活 ✓</text>
<rect x="134" y="26" width="62" height="34" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="165" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 3</text>
<text x="165" y="54.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">存活 ✓</text>
<rect x="198" y="26" width="62" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="229" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 4</text>
<text x="229" y="54.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">宕机 ✗</text>
<rect x="262" y="26" width="62" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="293" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 5</text>
<text x="293" y="54.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">宕机 ✗</text>
<text x="8" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">挂 3 个：剩 2 个 < 3，加不上锁</text>
<rect x="6" y="92" width="62" height="34" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="37" y="105.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 1</text>
<text x="37" y="120.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">存活 ✓</text>
<rect x="70" y="92" width="62" height="34" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="101" y="105.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 2</text>
<text x="101" y="120.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">存活 ✓</text>
<rect x="134" y="92" width="62" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="165" y="105.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 3</text>
<text x="165" y="120.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">宕机 ✗</text>
<rect x="198" y="92" width="62" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="229" y="105.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 4</text>
<text x="229" y="120.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">宕机 ✗</text>
<rect x="262" y="92" width="62" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="293" y="105.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">节点 5</text>
<text x="293" y="120.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">宕机 ✗</text>
<text x="8" y="160" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">容忍的故障数 = (N−1)/2，N=5 时是 2</text>
<text x="8" y="182" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">任意两个多数派必有公共节点</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">所以不会有两个客户端同时拿到锁</text>
<text x="8" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">挂 3 个牺牲可用性，安全性仍然保持</text>
</svg>
第一行挂 2 个，还剩 3 个存活，刚好凑够多数派 3，能加锁。第二行挂 3 个，只剩 2 个，不够，加不上锁，但也不会出现两个客户端同时持锁。
**容易错。**
- **以为挂了 3 个也能凑合：** 只剩 2 个，凑不出多数派，加不上锁。
- **以为 4 个节点比 3 个更能容错：** 都只容忍 1 个故障，4 个反而多花一台。
- **5 个节点放同一个机架：** 机架断电一次挂 3 个，整套锁不可用，节点要分散在独立的故障域。
- **节点重启后立刻加入：** 它丢了 key，可能重新放出已授予的锁，要延迟重启至少一个 TTL，或用 AOF `always`（牺牲性能）。

