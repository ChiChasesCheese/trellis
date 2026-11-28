---
id: hi-mock-notification-03-estimate
node: fix.notification-mock
type: qa
step: 3
---
## Q
**通知系统 · 第 3 步 · 估算（每行带单位）**｜模拟面试

面试官：「有没有数字想先算一下？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **规矩：** 每行两边写单位，回算 10 的幂；给定 1 亿 MAU、5 亿条/天、500 万条/分钟。
- **平均：** 500,000,000 ÷ 86,400 = 5,787 ≈ 5.8k 条/秒（5e8 ÷ 8.6e4 ≈ 5.8e3，对）。
- **峰值：** 500 万条**每分钟**不是每秒：5,000,000 ÷ 60 = 83,333 ≈ 83k 条/秒，峰均比约 14:1。
- **回执：** 占比没给，假设 20%：1 亿条/天 ÷ 86,400 ≈ 1,157 条/秒，峰值 3 倍约 3.5k 条/秒；其余 80% 是活动。
- **年行数与存储：** 500,000,000 × 365 = 1.8 × 10^11 行（一千八百亿，不是两百亿）；每行 1 KB（假设：正文约 600 字节加状态、时间戳）= 180 TB/年；带宽 83k × 1 KB = 83 MB/秒，对日志集群是小数目。
- **用数字做决定：** 平均 5.8k 行/秒，主库（约 2 万行/秒舒适区）够；峰值 83k 是它的 4 倍；180 TB/年远超单库。所以写入口前放持久日志吸收峰值，状态库分片，旧数据设保留期。
- **回头检查：** 500,000,000 ÷ 100,000,000 = 5 条/人/天，合理。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 298">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">年计数、存储与带宽</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">每年行数</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">500,000,000 条/天 × 365 天/年</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">= 1.8 × 10^11 行/年（1,800 亿）</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">每年存储（每行 1 KB，我假设）</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1.8 × 10^11 行 × 1 KB/行</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">= 1.8 × 10^14 字节 = 180 TB/年</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">日志带宽（峰值）</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">83,333 条/秒 × 1 KB/条</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">= 83 MB/秒：一个小集群够</text>
<rect x="8" y="227" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="245.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">单个主库 vs 峰值写</text>
<text x="18" y="260.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">83k ÷ 10k 行/秒/主库 ≈ 8</text>
<text x="18" y="275.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">峰值是单库的 4 倍：日志在前，库要分片</text>
</svg>
白板上新增：两张表，每行带单位；最后一行写出三条决定：日志在前、分片、保留期。

**常见失分。**
- **每分钟当成每秒：** 算成 10k/秒，差 8 倍。
- **比例前后不一致：** 先说 20:1，白板写 200:1，实际约 14:1。
- **年行数少一个数量级：** 说成 2 × 10^10，存储也少 10 倍（应为 180 TB）。
- **用户数写错：** 把 1 亿写成「1mil users/month」。
- **算了不用：** 说完 83k/秒，不说「所以日志放在写入口前面」。

**面试官可能接着问。**
- 回执峰值为何 3 倍？ → 假设：回执跟支付走、白天多；给真实曲线我就换，结论不变，回执很小。
- 峰值持续 10 分钟？ → 5,000,000 × 10 = 5,000 万条 × 1 KB = 50 GB；日志每天 500 GB，保留 3 天 1.5 TB，放得下。
- 三副本是多少？ → 约 540 TB 磁盘，但副本不改变逻辑大小，分片和保留期按 180 TB/年算。
