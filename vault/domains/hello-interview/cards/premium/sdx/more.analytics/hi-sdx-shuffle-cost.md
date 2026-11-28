---
id: hi-sdx-shuffle-cost
node: more.analytics
type: qa
step: 3
---
## Q
**Shuffle：批作业最贵的一步**｜补充 · 分析型系统：OLAP、数仓与批处理 · 必会

面试官：「Spark 或 MapReduce 作业里，`groupByKey` 或两张大表的连接为什么往往占掉大半运行时间？shuffle 到底做了什么，你会怎么减少它？」

## A
**结论。** shuffle 要把相同键的记录送到同一台机器，是一次全对全的网络传输加落盘，而且下游阶段必须等它结束。优化的总方向是少 shuffle 字节、少 shuffle 次数。

**要点。**
- **写出端：** 每个 map 任务按键的哈希把输出分成每个 reduce 任务一份，排序后溢写到本地磁盘。
- **拉取端：** 每个 reduce 任务向每一个 map 任务拉取属于自己的那一份，合并后处理。1000 个 map、200 个 reduce 就是 20 万个小块。
- **为什么贵：** 数据全量过网络，还要落盘；它是屏障，最慢的拉取完成之前下游不能开始。
- **少传字节：** map 端先局部聚合（combiner），再 shuffle；小表用广播连接（broadcast join）直接避开大表的 shuffle。
- **少做次数：** 先过滤再连接，让相邻算子共用同一种分区方式，避免重复重分区。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="170" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">M 个 map 任务（每个先按键哈希分好 R 份）</text>
<rect x="10" y="26" width="96" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="58.0" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">map 1</text>
<text x="58.0" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分 R 份落盘</text>
<rect x="122" y="26" width="96" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">map 2</text>
<text x="170.0" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分 R 份落盘</text>
<rect x="234" y="26" width="96" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="282.0" y="42.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">map 3</text>
<text x="282.0" y="57.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分 R 份落盘</text>
<rect x="34" y="140" width="120" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="94.0" y="156.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">reduce 1</text>
<text x="94.0" y="171.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">拉取自己那份</text>
<rect x="186" y="140" width="120" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="246.0" y="156.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">reduce 2</text>
<text x="246.0" y="171.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">拉取自己那份</text>
<polyline points="58,66 90.9,133.7" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="94,140 88.1,135.1 93.8,132.3" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="58,66 239.5,137.4" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="246,140 238.3,140.4 240.7,134.5" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="170,66 99.0,135.1" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="94,140 96.8,132.8 101.2,137.4" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="170,66 241.0,135.1" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="246,140 238.8,137.4 243.2,132.8" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="282,66 100.5,137.4" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="94,140 99.3,134.5 101.7,140.4" style="fill:var(--accent,#3b6fd4)"/>
<polyline points="282,66 249.1,133.7" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="246,140 246.2,132.3 251.9,135.1" style="fill:var(--accent,#3b6fd4)"/>
<text x="170" y="212" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每个 reduce 向每个 map 各拉一份</text>
<text x="170" y="230" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1000 × 200 = 20 万次拉取，全量过网络</text>
<text x="170" y="246" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最慢的拉取没完，下游阶段不能开始</text>
</svg>

**面试里这样说。** 「shuffle 是 M 个 map 对 R 个 reduce 的全对全传输，数据要落盘、过网络，并且是阶段屏障，所以是批作业的主要成本。我会先在 map 端做局部聚合，能广播小表就广播，减少要 shuffle 的字节。」

**易错。**
- **用 `groupByKey` 代替 `reduceByKey`：** 前者把所有原始记录都送过网络，后者先在 map 端合并，数据量可能差一个数量级以上（取决于每个键的重复程度）。
- **只加机器：** shuffle 的块数随 M×R 增长，机器多了小块更多，网络和磁盘寻址反而更碎。
