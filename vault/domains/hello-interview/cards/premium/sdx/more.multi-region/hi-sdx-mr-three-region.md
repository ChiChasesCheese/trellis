---
id: hi-sdx-mr-three-region
node: more.multi-region
type: qa
step: 2
---
## Q
**零数据丢失为什么需要三个区域**｜补充 · 多区域部署 · 追问

面试官：「要求丢掉整个区域也不丢数据、也不停写。用两个区域做同步复制行不行？为什么通常要三个？有没有便宜的做法？」

## A
**结论。** 不行。同步共识需要多数派，两个区域丢一个就只剩一半，要么停写，要么退回异步而丢数据。三个区域丢任意一个仍有 2/3，写入继续，RPO 为零；第三个区域可以只做见证，不存全量数据。

**要点。**
- **多数派：** N 个副本需要超过一半同意才提交，两个区域时多数是 2，丢一个就凑不齐。
- **三区域：** 丢任意一个仍有 2/3，写入继续，数据不丢。
- **见证区域：** 第三个区域只存投票和日志元数据（witness），不存全量数据，也不承担服务，成本低很多。
- **2026 亮点：** DynamoDB 全局表的多区域强一致模式（MRSC）正是这个形状：写入同步复制到至少另一个区域后才返回，RPO 为零，任一副本的强一致读都是最新；必须正好三个区域（三个副本，或两个副本加一个 witness），代价是写与强一致读延迟随区域间往返上升，且不支持 TTL、事务和本地二级索引，建表后不能改模式。
- **写延迟：** 每次提交要等最近的另一个区域确认，所以区域选择决定写延迟下限，通常两近一远。
- **分区时：** 被隔离的少数派区域不能继续写，保证不分裂。

**为什么。** 多数派保证任意两个多数派必然相交，所以新旧领导者不会各自提交冲突的写入。代价是每次写入付出一次跨区域往返。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 252">
<rect x="100" y="8" width="140" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">区域 A</text>
<text x="170" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">领导者</text>
<rect x="8" y="120" width="140" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="78" y="138.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">区域 B</text>
<text x="78" y="153.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">近，存全量</text>
<rect x="192" y="120" width="140" height="44" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="262" y="138.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">区域 C</text>
<text x="262" y="153.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">见证：只投票</text>
<polyline points="130,52 80,120" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="80,120 81.3,113.1 86.2,116.7" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="96" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">等 B 确认</text>
<polyline points="210,52 262,120" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="262,120 255.8,116.8 260.6,113.1" style="fill:var(--accent,#3b6fd4)"/>
<text x="240" y="96" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">投票</text>
<text x="8" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3 个里 2 个同意即提交</text>
<text x="8" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">丢任一区域，仍有 2/3，写入继续</text>
<text x="8" y="238" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">写延迟 = 最近另一区域的往返</text>
</svg>

**面试里这样说。** 「两个区域做同步多数派，丢一个就没有多数，所以我用三个区域，第三个只做见证，存投票和日志元数据。每次提交等最近的另一个区域，所以我把两个区域放近、一个放远。」

**易错。**
- **两区域同步复制：** 分区时无法区分对方死了还是网络断了，要么停写要么脑裂。
- **三个区域都放很远：** 每次写入都背着最大的往返延迟。
- **见证区域也存全量：** 成本没降，只是多一个副本。
