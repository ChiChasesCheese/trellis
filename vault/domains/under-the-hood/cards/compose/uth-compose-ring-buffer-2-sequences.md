---
id: uth-compose-ring-buffer-2-sequences
node: compose.ring-buffer
type: qa
step: 2
---
## Q
**环形数组 + 两个只增不减的序号**｜Linux kfifo · v6.12 · Disruptor 4.0.0

环形缓冲区由哪几块结构组成？怎样区分空和满？

## A
**结构。** 一个定长数组 `buf`，加两个只增不减的整数（序号，sequence）：`write`（已写入的总个数）和 `read`（已读走的总个数）。第 `n` 个元素放在 `buf[n & mask]`，`mask` 是容量减 1，所以容量必须是 2 的幂。`write - read` 是 0 就是空，等于容量就是满，不会混淆。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<path d="M 296 30 C 296 4, 44 4, 44 30" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="1" stroke-dasharray="4 3"/>
<line x1="44" y1="24" x2="44.0" y2="26.0" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="44,33 47.2,26.0 40.8,26.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="170" y="14" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">绕回</text>
<text x="44.0" y="46" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="26" y="52" width="36" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="44.0" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<text x="80.0" y="46" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="62" y="52" width="36" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="80.0" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<text x="116.0" y="46" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="98" y="52" width="36" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="116.0" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<text x="152.0" y="46" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="134" y="52" width="36" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="188.0" y="46" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="170" y="52" width="36" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="224.0" y="46" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="206" y="52" width="36" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="260.0" y="46" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<rect x="242" y="52" width="36" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="296.0" y="46" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<rect x="278" y="52" width="36" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<line x1="44.0" y1="120" x2="44.0" y2="93.0" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="44.0,86 40.8,93.0 47.2,93.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="50.0" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">read = 8</text>
<text x="50.0" y="148" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8 &amp; 7 = 0</text>
<line x1="152.0" y1="120" x2="152.0" y2="93.0" stroke="currentColor" stroke-width="1"/>
<polygon points="152.0,86 148.8,93.0 155.2,93.0" fill="currentColor"/>
<text x="172.0" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">write = 11</text>
<text x="172.0" y="148" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">11 &amp; 7 = 3</text>
<text x="170" y="180" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">槽里的数字是序号, 方格上方是下标</text>
<text x="170" y="198" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">已用 = write - read = 3, 满 = 8</text>
</svg>
```

| 操作 | 碰哪几个结构 | 复杂度 |
|---|---|---|
| `offer` | 读 `write`、`read` 判满；写 `buf[write & mask]`；`write` 加 1 | O(1) |
| `poll` | 读 `read`、`write` 判空；读 `buf[read & mask]`；`read` 加 1 | O(1) |
| 当前个数 | `write - read` | O(1) |

**为什么。** 序号只往前走，`write - read` 永远不二义。`write` 只有生产者改，`read` 只有消费者改，一个生产者加一个消费者时不用锁。Linux 内核的 `kfifo`（`in`、`out`、`mask`）用的就是这个结构；Disruptor 的序号从 -1 起，记的是最后一个序号而不是个数，思路相同。

**对应 LeetCode：** 无直接对应的题
