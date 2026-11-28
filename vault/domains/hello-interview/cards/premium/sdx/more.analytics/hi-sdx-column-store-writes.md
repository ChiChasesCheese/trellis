---
id: hi-sdx-column-store-writes
node: more.analytics
type: qa
step: 7
---
## Q
**列存怎么接收写入**｜补充 · 分析型系统：OLAP、数仓与批处理 · 追问

面试官：「列存把压缩、有序的列文件当作不可变的，没法原地更新。可业务数据不停地进来，列存是怎么接收写入的？这对使用方式有什么限制？」

## A
**结论。** 做法和 LSM 树一样：新写入先进一个小的、按行存放或无序的内存增量区，查询时把增量区和不可变的压缩列文件合并着读，后台再把增量重写成新的有序列段。

**要点。**
- **写入路径：** 写入落到内存里的增量存储（delta store），攒够一批再刷成新的列段（segment）。
- **读取路径：** 查询同时扫描列文件和增量区，对用户透明。
- **后台合并：** 定期把小段合并成大段，重新排序、压缩，并丢掉已删除的行。
- **限制一：** 单行的更新和删除很贵（要标记删除再重写），列存适合批量、以追加为主的写入。
- **限制二：** 零散的小批量写入会让增量区和小段越积越多，扫描变慢，直到合并追上。
- **2026 亮点：** ClickHouse 在 25.7 引入标准 SQL `UPDATE`（当时是实验性功能，25.8 起 Beta，26.10 起正式 GA），写成只含被改列和行的补丁分片（patch part），查询时叠加、后台合并时才并入数据分片，和「增量区加后台合并」是同一思路。适合更新不超过表约 10% 的行；补丁未合并前读变慢，并让相关分片上的跳数索引和投影失效，太碎还会触发 too many parts，所以要批量更新，大范围改写仍用 mutation。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 280">
<rect x="100" y="8" width="140" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="27.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写入（批量追加）</text>
<polyline points="170,38 170.0,55.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,62 166.8,55.0 173.2,55.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="60" y="62" width="220" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="78.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">内存增量区</text>
<text x="170.0" y="93.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">行式 / 无序，可更新</text>
<polyline points="170,102 170.0,127.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,134 166.8,127.0 173.2,127.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="178" y="124" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">攒够一批刷出</text>
<rect x="40" y="134" width="260" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="150.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">列段（不可变，有序，压缩）</text>
<text x="170.0" y="165.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">列 A 段 1   列 A 段 2   …</text>
<rect x="40" y="206" width="260" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="225.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">查询：合并读增量区 + 列段</text>
<polyline points="170,206 170.0,181.0" fill="none" stroke-width="1.3" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="170,174 173.2,181.0 166.8,181.0" fill="currentColor"/>
<text x="8" y="256" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">后台：合并小段、重排序、丢掉已删除行</text>
<text x="8" y="274" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">单行更新很贵，要攒批导入</text>
</svg>

**面试里这样说。** 「列文件不可变，所以写入先进内存增量区，查询时合并读，后台再合并成新的有序列段。它适合批量追加；高频的单行更新会让小段堆积，扫描性能下降。」

**易错。**
- **把列存当 OLTP 用：** 高频单行更新和点查是行存的强项，放进列存会被合并开销拖垮。
- **一条一条插入：** 每次插入产生一个小段，应该攒批导入。
