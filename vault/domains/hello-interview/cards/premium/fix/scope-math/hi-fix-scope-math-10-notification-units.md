---
id: hi-fix-scope-math-10-notification-units
node: fix.scope-math
type: qa
step: 10
---
## Q
**通知系统 · 每行带单位**｜补强

面试官：「1 亿月活用户，平均每天 5 亿条通知，活动高峰每分钟 500 万条。算平均每秒、高峰每秒、峰均比，一年多少行、多少 TB，然后告诉我设计怎么变。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **公式先说，单位写满：** 速率 = 总量 ÷ 时间，每行写「条/天」「条/分钟」「条/秒」，不写裸数字。
- **平均：** 500,000,000 条/天 ÷ 86,400 秒/天 ≈ 5,800 条/秒。
- **高峰：** 题目给每分钟，5,000,000 条/分钟 ÷ 60 ≈ 83,000 条/秒，这已经是高峰，不再乘 3。
- **峰均比：** 83,000 ÷ 5,800 ≈ 14:1。回算：83,000 × 60 ≈ 5,000,000 条/分钟，5,800 × 86,400 ≈ 501,000,000 条/天，都对得上。
- **月活核对：** 500,000,000 ÷ 100,000,000 = 5 条/人/天（推送、邮件、短信合计），合理。
- **年行数和存储：** 500,000,000 × 365 = 1.8×10^11 行/年；× 1 KB = 180 TB/年，三年 ≈ 550 TB，三副本 ≈ 1.6 PB。日志带宽 83,000 × 1 KB = 83 MB/s。
- **落到设计：** 83,000 条/秒超过主库简单写的舒适区（约 20,000/秒），平均 5,800 没有，所以前面放日志吸收高峰；后面 20 片分片库按自己速度写，83,000 ÷ 20 ≈ 4,150 行/秒/片；热库只留 7 天（3.5 TB），其余冷存储。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 188">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">数字 → 决定</text>
<rect x="8" y="26" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">83,000 条/秒 &gt; 单库舒适区 20,000/秒</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">日志在前，吸收高峰（83 MB/s）</text>
<rect x="8" y="80" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="99.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">日志后面：分片库按自己的速度写</text>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">20 片 → 83,000 ÷ 20 ≈ 4,150 行/秒/片</text>
<rect x="8" y="134" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="153.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">保留期：热库只留 7 天</text>
<text x="18" y="168.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">7 × 500 GB/天 = 3.5 TB；其余去冷存储</text>
</svg>
白板上：三行算式，每行带单位；下面三行决定。

**常见失分。**
- **每分钟当成每秒：** 5,000,000 ÷ 60 写成 10,000 条/秒，低 8 倍，会漏掉「前面要日志」。先写分母。
- **每年行数少一个数量级：** 写成 2×10^10 行、20 TB，实际 1.8×10^11 行、180 TB。回算。
- **峰均比写成 200:1：** 实际 14:1；200:1 意味着峰值 1,160,000 条/秒，是题目的 14 倍。
- **算完不用：** 没有一个数字进入设计。

**面试官可能接着问。**
- 把每分钟当成每秒会怎样？ → 5,000,000 条/秒 ÷ 20,000 = 250 个主库的写量，设计完全不同。
- 为什么 1 KB/行？ → 假设：id、类型、状态、时间戳、收件人、模板参数；给了别的数就改。
- 高峰全进日志要多大？ → 一次活动 10,000,000 × 1 KB = 10 GB，日志装得下；按 20,000 条/秒往外发，500 秒排空。
