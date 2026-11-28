---
id: hi-sdx-compaction-strategies
node: sd.core-concepts.db-indexing.more
type: qa
step: 2
---
## Q
**压实策略：按大小分层还是按层级**｜补充 · 数据库索引 · 追问

面试官：「LSM 引擎的 size-tiered 和 leveled 两种压实，文件各怎么组织？为什么 leveled 的读更省？什么负载选哪个？」

## A
**结论。** size-tiered 攒够几个大小相近的文件就合成一个更大的，写放大低，但键范围在很多文件里重叠，读和空间放大高。leveled 每层容量约是上一层的 10 倍、层内文件的键范围互不重叠，点查每层最多查一个文件，读和空间放大低，但写放大高。

**要点。**
- **size-tiered：** Cassandra 默认攒 4 个大小相近的 SSTable 合并，文件按大小成层。每个字节被重写的次数少。
- **size-tiered 的代价：** 同一个键可能出现在很多文件里，读要查多个；合并大文件时新旧文件并存，最坏需要约两倍的临时空间。
- **leveled：** L1、L2… 每层约 10 倍大，层内键范围不重叠，所以一次点查在每层最多命中一个文件。
- **leveled 的代价：** 数据每下沉一层，要和下一层约 10 倍大小的数据重新合并，最坏每层写放大约 10。
- **选择：** 写多、以追加为主（日志、时序）选 size-tiered；读多、更看重读延迟和空间选 leveled。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 300">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">size-tiered</text>
<text x="178" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">leveled · L1 不重叠</text>
<rect x="8" y="26" width="34" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="25.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a–z</text>
<rect x="46" y="26" width="34" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="63.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a–z</text>
<rect x="84" y="26" width="34" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="101.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a–z</text>
<rect x="122" y="26" width="34" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="139.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a–z</text>
<polyline points="80,52 80.0,69.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="80,76 76.8,69.0 83.2,69.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="8" y="76" width="150" height="26" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83.0" y="93.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">一个更大的文件 a–z</text>
<text x="8" y="126" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">键范围在多个文件里重叠</text>
<text x="8" y="144" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">点查要看多个文件</text>
<text x="8" y="162" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个字节重写次数少</text>
<rect x="178" y="26" width="48" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="202.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a–f</text>
<rect x="229" y="26" width="48" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="253.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">g–m</text>
<rect x="280" y="26" width="48" height="26" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="304.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">n–z</text>
<text x="178" y="74" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">L2：约 10 倍大，同样不重叠</text>
<rect x="178" y="84" width="36" height="26" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="196.0" y="101.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a–c</text>
<rect x="217" y="84" width="36" height="26" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="235.0" y="101.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d–f</text>
<rect x="256" y="84" width="36" height="26" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="274.0" y="101.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">g–i</text>
<rect x="295" y="84" width="33" height="26" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="311.5" y="101.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">…</text>
<text x="178" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">点查每层最多 1 个文件</text>
<text x="178" y="152" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">下沉一层合并约 10 倍数据</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">写多读少、追加为主：size-tiered</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读延迟与空间优先：leveled</text>
<text x="8" y="258" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">size-tiered 大合并最坏要约两倍空间</text>
<text x="8" y="276" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">leveled 写放大最坏约每层 10</text>
</svg>

**面试里这样说。** 「写密集、读少的场景我选 size-tiered，每个字节重写次数少；读延迟和空间更重要就选 leveled，层内键范围不重叠，点查每层只查一个文件，代价是写放大高。」

**易错。**
- **说 leveled「文件更少」：** 文件并不少，是每次查找要看的文件少。
- **忽略 size-tiered 的临时空间：** 磁盘用到八成再做大合并，会因为空间不够而失败。
