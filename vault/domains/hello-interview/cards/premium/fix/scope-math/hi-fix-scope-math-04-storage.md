---
id: hi-fix-scope-math-04-storage
node: fix.scope-math
type: qa
step: 4
---
## Q
**GoFundMe · 存储**｜补强

面试官：「数据量有多大？要不要分库？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **公式先说：** 「存储 = 条数 × 每条大小 × 年数 × 倍数。」
- **捐款表：** 「前面的每天 100 万笔是高峰日，全年平均约每天 27 万笔，一年约 1 亿笔；每笔约 1 KB：1e8 × 1e3 = 1e11 字节 = 100 GB 一年；5 年 500 GB；索引按 2 倍，约 1 TB。」
- **结论：** 「1 TB 一台库放得下，存储不是分库的理由。就算天天都是高峰日，一年 3.65 亿笔，5 年连索引约 3.7 TB，结论也不变。分库要有读写压力来推。」
- **图片另算：** 「100 万个活动，每个 2 MB 图片：100 万 × 2 MB = 2 TB。图片放对象存储加 CDN，不放数据库。」
- **小表和小结构：** 「applied 表一笔一行，每行约 50 字节：1 亿 × 50 = 5 GB。Redis 每个活动约 2 KB：100 万 × 2 KB = 2 GB，内存放得下。」
- **说出倍数的依据：** 「索引 2 倍、副本另算，这是我的假设；副本是可用性的账，不是容量的账。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 296">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">存储 = 条数 × 每条大小 × 年数 × 倍数</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">捐款表</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1 亿笔/年 × 1 KB = 100 GB/年</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">5 年 500 GB，索引 ×2 = 1 TB：一台库</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">活动图片</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">100 万个活动 × 2 MB = 2 TB</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">放对象存储 + CDN，不进数据库</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">applied 表</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1 亿行 × 50 字节 = 5 GB</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一笔捐款一行，量很小</text>
<rect x="8" y="227" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="245.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Redis 小结构</text>
<text x="18" y="260.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">每个活动约 2 KB × 100 万 = 2 GB</text>
<text x="18" y="275.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">内存放得下；只放活跃的活动更少</text>
</svg>
白板上：四块存储，每块一行算式、一行决定。
**为什么这样说。** （约 1 分钟。）估算存储是为了决定「一台够不够、放哪里」。强的回答把大对象和小记录分开，各自给出去处。弱的回答是一个总数加一句「很大，要分片」。
**面试官可能接着问。**
- 要保留多久？ → 捐款是财务记录，要保留几年；我按 5 年算。到期的归档到便宜存储，不影响在线库。
- 1 TB 的库查询会不会慢？ → 按主键和 (campaign_id, status) 索引查，不扫全表；热数据在内存里，冷数据只在对账时读。
- 图片谁来存？ → 浏览器直传对象存储，我们的服务只存地址；这样图片的流量不经过我们的服务。
**常见失分。**
- **把所有东西算在一起：** 图片和记录不是一类数据。
- **一报大数就分片：** 存储大不等于要分片，先看读写。
- **倍数没有依据：** 索引、副本、保留年数都是假设，要说出来。
