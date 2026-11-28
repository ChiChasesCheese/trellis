---
id: hi-sdx-batch-map-shuffle-reduce
node: more.analytics
type: qa
step: 2
---
## Q
**批处理引擎怎么算：map、shuffle、reduce**｜补充 · 分析型系统：OLAP、数仓与批处理 · 必会

面试官：「100 GB 的订单日志，要统计每个用户的总消费，一台机器算太慢。MapReduce 或 Spark 这类批处理引擎，是怎么把它拆给几百台机器做的？为什么中间一定有一步 shuffle？」

## A
**结论。** 分三步完成。map 让各机并行处理自己那一块数据，输出（键，值）；shuffle 按键的哈希把相同键的记录送到同一台机器；reduce 对同一个键的全部值做聚合。计算跑到数据所在的机器上，只有 shuffle 这一步要把数据搬过网络。

**要点。**
- **map：** 输入切成约 128 MB 一块，100 GB 约 800 块，每块一个 map 任务，尽量排到存有这块的机器上读本地盘。任务只看自己那一块，输出（用户，金额），彼此不通信。
- **shuffle：** 同一用户的记录散在 800 个任务的输出里，而求和要看到他的全部金额。按 hash(用户) 对 reduce 任务数（如 200）取模决定去向：map 任务把输出按目标分好写在本机磁盘，reduce 任务再向每个 map 任务拉取属于自己的那份。
- **reduce：** 每个 reduce 任务拿到若干用户的全部金额，求和后写出。所有 map 任务完成后，reduce 才开始处理。
- **Spark 的叫法：** 一个作业是由多个阶段（stage）连成的图。filter、map 这类只看单条记录的算子在同一阶段里流水线执行；groupByKey、join 这类要让相同键聚到一起的算子，阶段之间需要 shuffle。
- **失败怎么办：** 输入不可变，任务之间只通过 shuffle 交换数据，所以某个任务失败，只需在别的机器上重跑它。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 228">
<rect x="8" y="8" width="96" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="56" y="27" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① map 1</text>
<rect x="122" y="8" width="96" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="27" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① map 2</text>
<rect x="236" y="8" width="96" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="284" y="27" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① map 800</text>
<polyline points="56,38 56,118" fill="none" stroke-width="0.9" style="stroke:var(--accent,#3b6fd4)"/>
<polyline points="56,38 170,118" fill="none" stroke-width="0.9" style="stroke:var(--accent,#3b6fd4)"/>
<polyline points="56,38 284,118" fill="none" stroke-width="0.9" style="stroke:var(--accent,#3b6fd4)"/>
<polyline points="170,38 56,118" fill="none" stroke-width="0.9" style="stroke:var(--accent,#3b6fd4)"/>
<polyline points="170,38 170,118" fill="none" stroke-width="0.9" style="stroke:var(--accent,#3b6fd4)"/>
<polyline points="170,38 284,118" fill="none" stroke-width="0.9" style="stroke:var(--accent,#3b6fd4)"/>
<polyline points="284,38 56,118" fill="none" stroke-width="0.9" style="stroke:var(--accent,#3b6fd4)"/>
<polyline points="284,38 170,118" fill="none" stroke-width="0.9" style="stroke:var(--accent,#3b6fd4)"/>
<polyline points="284,38 284,118" fill="none" stroke-width="0.9" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="150" y="67" width="40" height="22" rx="11" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="83" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">②</text>
<rect x="8" y="118" width="96" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="56" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ reduce 1</text>
<rect x="122" y="118" width="96" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ reduce 2</text>
<rect x="236" y="118" width="96" height="30" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="284" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ reduce 200</text>
<text x="8" y="176" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">① map：每个任务读本地一块，输出（用户，金额）</text>
<text x="8" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">② shuffle：hash(用户) 决定去哪个 reduce</text>
<text x="8" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">③ reduce：同一用户的金额到齐后求和</text>
</svg>

**面试里这样说。** 「批处理分三步：map 在数据所在的机器上并行读，输出（键，值）；shuffle 按键的哈希把相同键的记录送到同一个 reduce；reduce 做聚合。map 和 reduce 都读本地数据，只有 shuffle 过网络，所以它是主要成本。」

**易错。**
- **以为分组、连接、去重可以不 shuffle：** 凡是要让相同键聚到一起的计算都必须 shuffle，区别只在数据量。
- **以为任务之间能直接通信：** 只能通过 shuffle 交换，这正是任务能独立重跑的前提。
