---
id: hi-sdx-skew-vs-straggler
node: more.analytics
type: qa
step: 4
---
## Q
**一个任务跑了一小时：倾斜还是慢节点**｜补充 · 分析型系统：OLAP、数仓与批处理 · 必会

面试官：「一个 1000 个任务的阶段，999 个五分钟跑完，剩下一个跑了一小时还没结束。可能的原因有哪两类？怎么区分，各怎么解决？」

## A
**结论。** 一类是数据倾斜（skew），一类是慢节点（straggler）。先看这个任务读了多少数据：输入特别大是倾斜，输入正常却进度慢是慢节点。

**要点。**
- **数据倾斜：** 哈希分区把某个超大的键（空值、头部客户）全送给一个 reduce 任务。解法是加盐（salting）：把键拆成 `key#0..N`，先按加盐键聚合，再去盐聚合一次；也可以在 map 端先预聚合，连接倾斜还可以交给引擎（Spark 的自适应查询执行 AQE 会自动拆分过大的分区）。
- **慢节点：** 数据量和别人一样，但这台机器有问题，比如磁盘快坏了、邻居抢资源。解法是推测执行（speculative execution）：在别的机器上启动同一任务的副本，谁先完成用谁。
- **区分方法：** 看每个任务的输入字节数和记录数，不要只看运行时间。
- **别混用：** 推测执行救不了倾斜，副本拿到的还是那个超大的键，一样慢，还白占资源。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">正常任务：输入 50 MB，5 分钟</text>
<rect x="8" y="24" width="30" height="18" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="23.0" y="37.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor"></text>
<text x="8" y="70" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">倾斜任务：输入 50 GB，60 分钟</text>
<rect x="8" y="78" width="324" height="18" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="91.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor"></text>
<text x="8" y="124" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">慢节点任务：输入 50 MB，60 分钟</text>
<rect x="8" y="132" width="324" height="18" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="145.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor"></text>
<text x="8" y="176" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">输入特别大：加盐 / 预聚合 / AQE 拆分</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">输入正常却慢：推测执行换机器</text>
<text x="8" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">推测执行救不了倾斜：副本拿到同一个热键</text>
</svg>

**面试里这样说。** 「我先比较各任务的输入大小：输入特别大是数据倾斜，用加盐或 AQE 拆分；输入正常但慢就是慢节点，开推测执行换一台机器重跑。推测执行对倾斜没用，因为副本拿到的还是同一个热键。」

**易错。**
- **倾斜时开推测执行：** 副本同样跑一小时，还多占一份资源。
- **把空值当普通键：** 连接键里大量 NULL 会全部哈希到同一分区，应先过滤或打散。
- **以为推测执行默认开着：** Spark 默认关闭（`spark.speculation=false`），要显式打开。
