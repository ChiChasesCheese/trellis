---
id: hi-fix-scope-math-11-time-base-trap
node: fix.scope-math
type: qa
step: 11
---
## Q
**时间基准陷阱 · 叫车平台**｜补强

面试官：「叫车平台：20 万名在线司机，每 4 秒上报一次位置，每条 100 字节；每小时 60 万个叫车请求，晚高峰最忙的一分钟有 18,000 个。算位置写入每秒、带宽、每天的位置数据，再算叫车请求的平均和高峰每秒，最后说哪一个决定架构。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先圈出每个数的时间基准：** 「位置是『每 4 秒』，请求一个是『每小时』、一个是『每分钟』。换成每秒之前，先写下分母：1 天 = 86,400 秒，1 小时 = 3,600 秒，1 分钟 = 60 秒；『每 4 秒一次』就是除以 4。」
- **位置写入：** 「200,000 司机 ÷ 4 秒 = 50,000 条/秒。」
- **带宽和每天：** 「50,000 条/秒 × 100 B = 5,000,000 B/s = 5 MB/s；× 86,400 秒/天 = 432,000 MB/天 = 432 GB/天。」
- **叫车平均：** 「600,000 次/小时 ÷ 3,600 秒/小时 ≈ 167 次/秒。」
- **叫车高峰：** 「18,000 次/分钟 ÷ 60 秒/分钟 = 300 次/秒。题目给了最忙的一分钟，就直接用它，不再乘 3。峰均比 300 ÷ 167 ≈ 1.8:1。」
- **回算：** 「300 次/秒 × 60 = 18,000 次/分钟，167 次/秒 × 3,600 = 601,200 ≈ 600,000 次/小时，都对得上。」
- **决定：** 「位置 50,000 条/秒，约是叫车 300 次/秒 的 167 倍，也超过单库的舒适区（约 20,000 次/秒），而且只关心最新位置：放内存里的地理索引，按城市分片，不进关系库。叫车请求 300 次/秒，一个关系库绰绰有余。位置历史若要留，432 GB/天走追加流加对象存储。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 233">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">叫车平台：先写分母，再除</text>
<rect x="8" y="26" width="324" height="61" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">分母</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1 天 = 86,400 秒 · 1 小时 = 3,600 秒</text>
<text x="18" y="75.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1 分钟 = 60 秒 · 每 4 秒一次 = ÷ 4</text>
<rect x="8" y="95" width="324" height="61" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">位置</text>
<text x="18" y="129.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">200,000 司机 ÷ 4 秒 = 50,000 条/秒</text>
<text x="18" y="144.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">× 100 B = 5 MB/s = 432 GB/天</text>
<rect x="8" y="164" width="324" height="61" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="183.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">叫车</text>
<text x="18" y="198.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">600,000 次/小时 ÷ 3,600 = 167 次/秒</text>
<text x="18" y="213.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">18,000 次/分钟 ÷ 60 = 300 次/秒</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 242">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">三种常见的错 → 一个决定</text>
<rect x="8" y="26" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">18,000 次/分钟 ÷ 3,600 = 5 次/秒</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分母用了小时：低 60 倍</text>
<rect x="8" y="80" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="99.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">600,000 次/小时 ÷ 60 = 10,000 次/秒</text>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分母用了分钟：高 60 倍</text>
<rect x="8" y="134" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="153.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">每 4 秒一次当成 4 次/秒</text>
<text x="18" y="168.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">200,000 × 4 = 800,000：高 16 倍</text>
<rect x="8" y="188" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="207.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">位置 50,000 条/秒 ≈ 叫车 300 次/秒 的 167 倍</text>
<text x="18" y="222.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">位置放内存地理索引；叫车一个关系库</text>
</svg>
白板上：先写一行分母，再三个结果；下面是三种常见的错，和一句决定。
**为什么这样说。** （约 2 分钟。）这张卡练的是一件事：看到每分钟、每小时、每天混在一道题里，先写分母再除。强的回答每一行带单位并回算；弱的回答随手用同一个分母除所有的数，差 60 倍也不察觉。
**面试官可能接着问。**
- 题目换成每月呢？ → 每月按 30 天：÷ 2,592,000 秒/月。每周 ÷ 604,800，每年 ÷ 31,536,000。
- 高峰一定要乘 3 吗？ → 只有题目没有给高峰时才用 3 倍；这里给了最忙的一分钟，直接换算。
- 『每 4 秒一次』为什么不是每秒 4 次？ → 间隔和频率互为倒数：每 4 秒 1 次 = 0.25 次/秒/司机；把它当 4 次/秒会得到 800,000 条/秒，高 16 倍。
- 每天 432 GB 要不要留？ → 先问需求：只要最新位置就不留；要做轨迹回放才留，走追加流加对象存储，不进热库。
- 怎么快速验算？ → 把结果乘回分母，看能否还原题目给的数；还原不了，就是分母用错了。
**常见失分。**
- **用小时的分母除分钟的量：** 18,000 ÷ 3,600 = 5 次/秒，低 60 倍。
- **用分钟的分母除小时的量：** 600,000 ÷ 60 = 10,000 次/秒，高 60 倍。
- **把『每 4 秒』当成每秒 4 次：** 高 16 倍。
- **不回算：** 乘回去就能发现分母错了。
- **算完不用：** 位置和叫车相差 167 倍，这才是架构的分界。
