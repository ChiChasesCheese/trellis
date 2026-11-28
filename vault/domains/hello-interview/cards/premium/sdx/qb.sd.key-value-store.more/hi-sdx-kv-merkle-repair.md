---
id: hi-sdx-kv-merkle-repair
node: qb.sd.key-value-store.more
type: qa
step: 4
---
## Q
**副本修复：Merkle 树只往不一致的子树下钻**｜补充 · 分布式键值存储 · 追问

面试官：「两个副本之间只有少量键不一致（节点宕机、hint 丢失）。后台修复为什么不逐键比较，而用 Merkle 树？」

## A
**结论。** 逐键比较要读出并传输两边全部数据，差异再小成本也不变。Merkle 树把每段键范围哈希成叶子，向上合并成根；两个副本先比根哈希，只往哈希不同的子树下钻，比较次数约为「差异数 × 树深」，而不是数据总量。

**要点。**
- **构建：** 每个节点对它负责的每段键范围维护一棵树。叶子是一小段键范围的哈希，父节点是子节点哈希的哈希。
- **比较：** 根相同就一致；不同就比较两个子节点，只递归哈希不同的那边，最后得到不一致的叶子范围，只传这些范围里的键。
- **算一下：** 1 亿个键、每叶 1000 个键，约 10 万个叶子，树深约 17。只有一个叶子不同时约 34 次哈希比较，而不是 1 亿次键比较。
- **代价：** 数据变化后受影响的子树要重新计算；成员变更或再平衡改变范围时，相关的树要重建，所以虚拟节点数不能无限大。叶子粒度太粗会多传数据，太细则树太大。
- **分工：** hint 补短暂宕机，读修复补被读到的键，Merkle 树兜底很久没人读的冷数据。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<rect x="125" y="6" width="90" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">根 ≠</text>
<rect x="45" y="60" width="70" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="80.0" y="78.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">= 跳过</text>
<rect x="225" y="60" width="70" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="260.0" y="78.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">≠ 下钻</text>
<polyline points="150,34 80,60" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polyline points="190,34 260,60" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="10" y="116" width="68" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44.0" y="134.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">范围 1</text>
<rect x="94" y="116" width="68" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128.0" y="134.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">范围 2</text>
<rect x="178" y="116" width="68" height="28" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212.0" y="134.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">范围 3</text>
<rect x="262" y="116" width="68" height="28" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="296.0" y="134.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">范围 4</text>
<polyline points="80,88 44,116" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polyline points="80,88 128,116" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polyline points="260,88 212,116" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polyline points="260,88 296,116" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="10" y="170" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">只传输不一致范围里的键</text>
<text x="10" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1 亿键、每叶 1000 键：约 34 次哈希比较</text>
<text x="10" y="208" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">而不是 1 亿次键比较</text>
</svg>

**面试里这样说。** 「副本反熵我用 Merkle 树：先比根，只往哈希不同的子树下钻，找出不一致的范围再同步。1 亿键大约 34 次哈希比较就能定位，代价是维护树和再平衡时重建。」

**易错。**
- **以为 Merkle 树本身修复数据：** 它只负责定位差异。
- **对写入很热的范围频繁重建：** 树的维护成本会超过收益。
