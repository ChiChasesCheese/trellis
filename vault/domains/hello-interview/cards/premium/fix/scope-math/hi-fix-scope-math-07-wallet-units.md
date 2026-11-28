---
id: hi-fix-scope-math-07-wallet-units
node: fix.scope-math
type: qa
step: 7
---
## Q
**Airbnb Wallet · 速率与存储**｜补强

面试官：「钱包用户 10,000,000，每人每周 1 笔转账，每天看 2 次余额或历史，每笔 500 字节，留 7 年。算速率、年笔数、存储，然后告诉我设计怎么变。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **公式先说：** 「速率 = 用户数 × 频率 ÷ 时间；存储 = 条数 × 大小 × 保留期。」
- **转账速率：** 「10,000,000 笔/周 ÷ 604,800 秒/周 ≈ 16.5 笔/秒；峰值按 3 倍，约 50 笔/秒。」
- **读速率：** 「10,000,000 用户 × 2 次/天 = 20,000,000 次/天；÷ 86,400 秒/天 ≈ 231 次/秒；峰值约 700 次/秒。」
- **年笔数：** 「10,000,000 笔/周 × 52 周 = 520,000,000 笔/年；回算：16.5 笔/秒 × 31,536,000 秒/年 ≈ 520,000,000，对得上。」
- **存储：** 「520,000,000 笔/年 × 500 字节 = 260 GB/年；× 7 年 ≈ 1.8 TB；索引按 2 倍约 3.6 TB。」
- **热数据：** 「最近 90 天 ≈ 130,000,000 行 × 500 字节 ≈ 65 GB，放得进内存的量级。」
- **决定：** 「写 50 笔/秒、读 700 次/秒、1.8 TB：一个 Postgres 主库加一个只读副本，不分片；交易表按月分区，旧的归档。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 231">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">公式，然后每行带单位</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">速率 = 用户数 × 频率 ÷ 时间</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">10,000,000 笔/周 ÷ 604,800 秒/周 ≈ 16.5 笔/秒</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">峰值 ×3：50 笔/秒</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">读</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">20,000,000 次/天 ÷ 86,400 秒/天 ≈ 231 次/秒</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">峰值 ×3：700 次/秒</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">存储 = 条数 × 大小 × 保留期</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">520,000,000 笔/年 × 500 字节 = 260 GB/年</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">× 7 年 ≈ 1.8 TB；索引 ×2 ≈ 3.6 TB</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 164">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">数字 → 决定</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">写 50 笔/秒，读 700 次/秒</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一个 Postgres 主库 + 一个只读副本</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不分片：这个量级远在单库范围内</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">热数据：最近 90 天</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">130,000,000 行 × 500 字节 ≈ 65 GB</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">放得进内存的量级；旧数据按月分区归档</text>
</svg>
白板上：三行算式，每行带单位；最后两行是决定。
**为什么这样说。** （约 1 分钟，放在估算最后。）面试官要的是能被一行一行检查的数字。强的回答速率、笔数、字节分开算，各带单位，并回算一遍；弱的回答把几个数混成一个「很大」。
**面试官可能接着问。**
- 为什么不分片？ → 写 50 笔/秒远低于单库的数千次/秒；1.8 TB 单库放得下；分片只会让钱包间转账变难，没有收益。
- 数字大 100 倍呢？ → 写 5,000 笔/秒，读 70,000 次/秒，存储 180 TB：这时才谈缓存、分片和归档。
- 为什么 500 字节？ → 我的假设：id、金额、状态、时间戳、两个外部 ID；给了别的数，我就改。
**常见失分。**
- **单位丢了：** 看不出是每秒、每年还是 GB。
- **笔数算小了：** 一年少一个数量级，存储方案跟着错。
- **算完不用：** 没有一个数字进入设计。
