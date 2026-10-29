---
id: uth-compose-connection-pool-2-structures
node: compose.connection-pool
type: qa
step: 2
---
## Q
**组合：线程本地列表、共享列表、交接队列**｜HikariCP · 7.0.2

HikariCP 的 `ConcurrentBag` 用哪几个结构分层？借和还各碰哪几个？

## A
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240">
<rect x="76" y="10" width="190" height="36" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="171.0" y="27.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 线程本地列表</text>
<text x="171.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ThreadLocal 最多 16 个</text>
<rect x="76" y="68" width="190" height="36" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="171.0" y="85.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2 sharedList</text>
<text x="171.0" y="99.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">所有连接 写时复制数组</text>
<rect x="76" y="126" width="190" height="36" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="171.0" y="143.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3 handoffQueue</text>
<text x="171.0" y="157.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SynchronousQueue 等归还</text>
<line x1="171" y1="46" x2="171.0" y2="62.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="171,68 168.0,62.0 174.0,62.0" fill="currentColor"/>
<text x="179" y="62" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没找到</text>
<line x1="171" y1="104" x2="171.0" y2="120.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="171,126 168.0,120.0 174.0,120.0" fill="currentColor"/>
<text x="179" y="120" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">全被占用</text>
<rect x="76" y="194" width="190" height="36" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="171.0" y="211.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PoolEntry</text>
<text x="171.0" y="225.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">state 0 空闲 1 在用 CAS</text>
<line x1="76" y1="212" x2="44" y2="212" stroke-width="1.2" stroke="currentColor"/>
<line x1="44" y1="212" x2="44" y2="28" stroke-width="1.2" stroke="currentColor"/>
<line x1="44" y1="28" x2="70.0" y2="28.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="76,28 70.0,31.0 70.0,25.0" fill="currentColor"/>
<text x="40" y="130" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没人等</text>
<line x1="266" y1="212" x2="282" y2="212" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="282" y1="212" x2="282" y2="144" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="282" y1="144" x2="272.0" y2="144.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="266,144 272.0,141.0 272.0,147.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="286" y="180" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">有人等</text>
</svg>
```

**结构。** 三层结构，加每个连接自带的状态：

- 线程本地列表（`ThreadLocal`）：这个线程上次用过的连接，不用抢任何共享结构。
- `sharedList`：所有连接，扫一遍找空闲的。它是写时复制数组：每次增删都复制一份新数组，读者不用加锁。
- `handoffQueue`（`SynchronousQueue`，同步交接队列）：借不到的线程在这里等，归还的线程直接把连接递给他。

连接的状态是一个整数，用 CAS（比较并交换：状态仍是旧值才改成新值）切换：0 空闲、1 在用、-1 已移除、-2 保留。

| 操作 | 碰哪几个结构 | 复杂度 |
|---|---|---|
| 借 | 本地列表 → `sharedList`（CAS 抢）→ `handoffQueue` 等 | 常数到 O(连接数) |
| 还 | 改状态为空闲；有人等则入 `handoffQueue`，否则进本地列表 | O(1) |
| 增删连接 | `sharedList`（写时复制） | O(连接数)，很少发生 |

**对应 LeetCode：** 无直接对应的题
