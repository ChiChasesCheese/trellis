---
id: uth-storage-buffer-pool-2-clock-sweep
node: storage.buffer-pool
type: qa
step: 2
---
## Q
**时钟扫描：近似 LRU，命中不挪节点**｜PostgreSQL · 18

PostgreSQL 的共享缓冲区（shared buffers）为什么不维护一条 LRU 链表？它怎么选被淘汰的页？

## A
**背景。** LRU 每次命中都要把页挪到队头，也就是改链表。很多进程同时访问时，改链表要加锁，成了瓶颈。

**结构。** 缓冲区是一个固定数组，一个环形指针循环扫描；每个缓冲区有使用计数 `usage_count`，取值 0 到 5（`BM_MAX_USAGE_COUNT`）。页每被使用一次，计数加 1，封顶 5；淘汰指针扫过时，计数非 0 就减 1 继续走，遇到计数为 0 且没人用的，就是牺牲者。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<circle cx="100" cy="32" r="15" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="100" y="36.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="139.6" cy="48.4" r="15" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="139.6" y="52.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="156" cy="88" r="15" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="156" y="92.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<circle cx="139.6" cy="127.6" r="15" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="139.6" y="131.8" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<circle cx="100" cy="144" r="15" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="100" y="148.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="60.4" cy="127.6" r="15" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60.4" y="131.8" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<circle cx="44" cy="88" r="15" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="44" y="92.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="60.4" cy="48.4" r="15" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60.4" y="52.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="100" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">指针</text>
<line x1="100" y1="72" x2="100" y2="56" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="100,50 103.0,56.0 97.0,56.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="196" y="44" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">命中: 计数 +1, 封顶 5</text>
<text x="196" y="70" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">指针扫过: 计数 -1</text>
<text x="196" y="96" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">遇到 0 且没人用:</text>
<text x="196" y="116" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">就是牺牲者</text>
</svg>
```

**细节。**

- 被钉住（pin，正被某个查询占着）的缓冲区一律跳过。
- 最坏要扫 5 + 1 圈才能找到空位（源码注释）。

**为什么。** 命中只要改一个计数，不用挪节点；上限取得很大就逼近真 LRU，但扫的圈数也跟着变多。

**对应 LeetCode：** 无直接对应的题
