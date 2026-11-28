---
id: hi-fix-resumable-job-04-table-after-a-year
node: fix.resumable-job
type: qa
step: 4
---
## Q
**通知系统 · 一年后那张表是什么样**｜补强

面试官：「你说一个 SQL 数据库就够了，可是请求表每天进 5 亿行。一年之后这张表是什么样子？你对它做什么？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先算，每行带单位：** 500,000,000 行/天 × 1 KB = 500 GB/天，× 365 = 1.8×10^11 行/年 ≈ 180 TB/年（未计索引和副本）。结论：不能是一张表，也不能全在热库，热库只留 7 天。
- **热库：** 按天分区，7 天 × 500 GB = 3.5 TB，索引 2 倍 = 7 TB，分 20 片每片 350 GB。7 天是假设（覆盖重试、对账、状态查询窗口），给了别的数就改；保留期是最便宜的旋钮，回执留多久由合规和客服定，先问。
- **删除用 DROP 分区，不 DELETE：** 每天 DELETE 5 亿行要扫 500 GB、写同量级日志、留死元组；DROP 是与行数无关的元数据操作。
- **冷存储：** 第 8 天摘下的分区去掉正文，只留 id、状态、时间约 100 字节/行 = 50 GB/天 ≈ 18 TB/年，留 3 年 54 TB，写成 Iceberg（Parquet 放对象存储）；导出后先核对行数，再 DROP。
- **分片键：** `hash(notification_id)`，同一 id 永远在同一分片，唯一约束才能在分片内原子裁决；不按消息类型，回执和活动量差几个数量级，一个分片拿走大部分写入。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 164">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">删旧数据：DELETE 行 还是 DROP 分区</text>
<rect x="8" y="26" width="324" height="61" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">每天 DELETE 5 亿行</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">扫描 500 GB，写出同量级的日志</text>
<text x="18" y="75.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">留下死元组，VACUUM 追不上</text>
<rect x="8" y="95" width="324" height="61" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">DROP 一个日分区</text>
<text x="18" y="129.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">与行数无关的元数据操作</text>
<text x="18" y="144.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">空间立刻归还，不留死元组</text>
</svg>
白板上：热、导出、冷、DROP 四步各带数字；再画 DELETE 和 DROP 的对照。

**常见失分。**
- **数量级错：** 算成 2×10^10 行、20 TB/年，少了 10 倍，单库还是分片的结论就错；每行带单位回算。
- **定时逐行删：** 5 亿行/天的 DELETE，日志和死元组追不上。
- **按消息类型分片：** 一个分片过热。
- **只说「冷存储」：** 不说留什么、多大、多久、怎么搬、怎么核对。

**面试官可能接着问。**
- 分区后唯一约束怎么办？ → PostgreSQL 唯一约束必须含分区列：键里带日期（如 UUIDv7），主键写成 (day, notification_id)；`receipt:pay_881` 这类业务键不带时间，就把去重放进一张不分区的小表（只存键和时间），按保留期分批删旧行。
- 客服查 3 个月前的回执？ → 查 Iceberg，秒到分钟级够用；热库只服务 7 天内。
- 为什么不全放热库多分片？ → 180 TB/年 ÷ 20 片 = 9 TB/片/年，3 年 27 TB/片加索引副本更多，而 7 天外几乎没人读。
- DROP 前怎么确认导出完整？ → 行数对账加校验和，失败的分区留着并告警。
