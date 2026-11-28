---
id: hi-sdx-lakehouse-commit
node: more.analytics
type: qa
step: 11
---
## Q
**湖表格式：对象存储上的原子提交**｜补充 · 分析型系统：OLAP、数仓与批处理 · 追问

面试官：「对象存储本身没有事务。Iceberg 或 Delta 是怎么在它上面做到原子提交和快照隔离的？两个作业同时提交会怎样？」

## A
**结论。** 数据文件一旦写出就不改。提交时先写好新数据文件和新的元数据，最后只做一次原子操作：把表的根指针换成新版本。整套 ACID 就压缩成这一次指针切换。

**要点。**
- **不可变文件：** 数据文件和元数据都是只写一次的对象，提交不改旧文件。
- **换根指针：** Iceberg 靠目录服务（catalog）对「当前元数据文件」做比较并交换（CAS）；Delta 靠原子地创建下一个编号的日志文件，已存在就失败。对象存储的条件写（`If-None-Match`）正好能做到后者。
- **读者：** 查询开始时记下自己看到的根，整个查询只读这一个快照，所以天然是快照隔离。
- **写者：** 乐观并发。读到的指针在提交前被别人换走，CAS 失败；写者检查两次改动有没有碰同一批文件，没有就基于新版本重试，有就整体失败。
- **半成品：** 没提交的数据文件没人引用，读者看不到，之后当孤儿文件清理。
- **2026 亮点：** 目录这一步已标准化为 Iceberg REST Catalog 规范，Apache Polaris 是其开源实现，Spark、Flink、Trino 等多个引擎经同一目录共享同一张表，权限也集中管理；S3 Tables 同样提供 REST 端点。代价是目录服务成为新的关键依赖，要做高可用，压实和过期快照仍要有人执行（目录只存放维护策略，不执行）。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 300">
<rect x="70" y="8" width="200" height="36" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">表的根指针</text>
<text x="170.0" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">catalog 或日志文件名</text>
<rect x="10" y="100" width="150" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85.0" y="114.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">元数据 v12</text>
<text x="85.0" y="129.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">（旧，读者可固定）</text>
<rect x="180" y="100" width="150" height="36" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255.0" y="114.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">元数据 v13</text>
<text x="255.0" y="129.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">（新）</text>
<polyline points="120,44 88.7,94.1" fill="none" stroke-width="1.3" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="85,100 86.0,92.4 91.4,95.8" fill="currentColor"/>
<polyline points="220,44 251.3,94.1" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="255,100 248.6,95.8 254.0,92.4" style="fill:var(--accent,#3b6fd4)"/>
<text x="238" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">CAS 换指针</text>
<rect x="10" y="176" width="150" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="85.0" y="190.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">清单 + 数据文件</text>
<text x="85.0" y="205.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">a.parquet b.parquet</text>
<rect x="180" y="176" width="150" height="36" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255.0" y="190.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">旧文件 + 新文件</text>
<text x="255.0" y="205.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">a b + c.parquet</text>
<polyline points="85,136 85.0,169.0" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="85,176 81.8,169.0 88.2,169.0" fill="currentColor"/>
<polyline points="255,136 255.0,169.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="255,176 251.8,169.0 258.2,169.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="8" y="236" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">写者：先写新文件和元数据，最后一次 CAS</text>
<text x="8" y="254" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读者：开始时固定一个根，只读一个快照</text>
<text x="8" y="272" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">CAS 失败：有人先换了，查冲突后重试</text>
<text x="8" y="290" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">未提交的文件没人引用，读者看不到</text>
</svg>

**面试里这样说。** 「文件不可变，提交就是把根指针原子换成新的元数据；读者固定一个快照，写者用乐观并发，CAS 失败就检查冲突后重试。没提交成功的文件没人引用，读者永远看不到半成品。」

**易错。**
- **以为对象存储自带事务：** 没有这一步原子换指针，并发提交会互相覆盖元数据。
- **冲突就一律失败：** 两个写者改不同分区或不同文件时可以基于新版本重试，一律失败会让流式作业频繁失败。
