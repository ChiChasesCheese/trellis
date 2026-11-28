---
id: hi-sdx-repl-read-repair-antientropy
node: more.replication
type: qa
step: 5
---
## Q
**读修复与反熵：为什么两个都要**｜补充 · 复制 · 追问

面试官：「无主（Dynamo 风格）复制里，读修复和反熵各怎样让落后的副本追平？为什么两个都要？反熵为什么说是「后台任务」却很贵？」

## A
**结论。** 读修复在读路径上把最新版本写回落后的副本，只惠及被读到的热键；反熵在后台用 Merkle 树比较整段数据，覆盖从不被读的冷数据。只有读修复，冷数据会无限期落后。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 300">
<rect x="10" y="8" width="320" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 两个副本比较范围的根哈希</text>
<text x="170.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不同，说明这段数据有差异</text>
<polyline points="170,48 170.0,59.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,66 166.8,59.0 173.2,59.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="66" width="320" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="82.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 比较左右两个子节点</text>
<text x="170.0" y="97.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">左边哈希相同，整棵子树跳过</text>
<polyline points="170,106 170.0,117.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,124 166.8,117.0 173.2,117.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="124" width="320" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 沿着不同的一侧继续下钻</text>
<text x="170.0" y="155.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">直到叶子：一小段键范围</text>
<polyline points="170,164 170.0,175.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,182 166.8,175.0 173.2,175.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="182" width="320" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="198.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 只传输这一小段的数据</text>
<text x="170.0" y="213.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">比较省带宽</text>
<text x="8" y="246" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">代价在建树：每个副本要把自己的数据</text>
<text x="8" y="262" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">全部读一遍算哈希，CPU 与 IO 接近全表扫描，</text>
<text x="8" y="278" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">所以要错峰运行并限速。</text>
</svg>

**要点。**
- **读修复：** quorum 读时协调者对比各副本版本，把最新值写回过时的副本。
- **反熵：** 每对副本按范围建 Merkle 树，自顶向下比较哈希，只传输不同的叶子范围。
- **成本在建树：** 比较省带宽，但建树要读完副本的全部数据，是大 Cassandra 集群最主要的运维开销，所以错峰运行并限速。
- **缺了会怎样：** 一个值只留在 3 个副本中的 1 个上，等于只有一块盘保着它。墓碑过期后还会让已删数据复活，所以要在 gc_grace_seconds（默认 10 天）内修一轮。

**面试里这样说。** 「热数据靠读修复，冷数据靠定期反熵。反熵的 Merkle 树比较很省带宽，但建树要扫全量数据，我会错峰限速，并保证在墓碑宽限期内修完一轮。」

**易错。**
- **只靠读修复：** 冷数据永远追不上。
- **把反熵当免费后台任务：** 全量扫描会和线上读写抢 IO。
