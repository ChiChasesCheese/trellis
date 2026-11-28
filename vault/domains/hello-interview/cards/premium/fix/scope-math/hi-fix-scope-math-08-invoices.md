---
id: hi-fix-scope-math-08-invoices
node: fix.scope-math
type: qa
step: 8
---
## Q
**开票系统 · 一个主库够不够**｜补强

面试官：「做一个开票系统：500,000 个商家，每家每月开 20 张发票，每张 2 KB，保留 7 年；商家平均每天查看 5 次。算一下，要不要分片？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **张数：** 「500,000 商家 × 20 张/月 = 10,000,000 张/月；× 12 = 120,000,000 张/年。」
- **写速率：** 「平均 10,000,000 张/月 ÷ 2,592,000 秒/月 ≈ 3.9 张/秒。发票集中在月末，我假设一半在最后 3 天：5,000,000 张 ÷ 259,200 秒 ≈ 19 张/秒，用这个当峰值。」
- **读速率：** 「500,000 商家 × 5 次/天 = 2,500,000 次/天；÷ 86,400 秒/天 ≈ 29 次/秒；峰值按 3 倍约 87 次/秒。」
- **存储：** 「120,000,000 张/年 × 2 KB = 240 GB/年；× 7 年 ≈ 1.7 TB；索引按 2 倍约 3.4 TB。」
- **决定：** 「写 19 张/秒、读 87 次/秒、1.7 TB：一个 Postgres 主库加一个只读副本，不分片。发票按月分区，旧的归档；PDF 放对象存储，库里只存地址。」
- **为什么不分片：** 「每个数字都比单库的能力小一到两个数量级，分片只会增加复杂度。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 298">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">开票系统：每行带单位</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">张数</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">500,000 商家 × 20 张/月 = 10,000,000 张/月</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">× 12 月 = 120,000,000 张/年</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">写速率</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">平均：10,000,000 ÷ 2,592,000 秒/月 ≈ 3.9 张/秒</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一半在月末 3 天：5,000,000 ÷ 259,200 ≈ 19 张/秒</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">读</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">500,000 × 5 次/天 ÷ 86,400 ≈ 29 次/秒</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">峰值 ×3 ≈ 87 次/秒</text>
<rect x="8" y="227" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="245.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">存储</text>
<text x="18" y="260.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">120,000,000 张/年 × 2 KB = 240 GB/年</text>
<text x="18" y="275.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">× 7 年 ≈ 1.7 TB；索引 ×2 ≈ 3.4 TB</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 89">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">决定</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">一个 Postgres 主库 + 一个只读副本</text>
<text x="170" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不分片：写 19 张/秒，读 87 次/秒，1.7 TB</text>
<text x="170" y="74.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">发票按月分区；PDF 放对象存储</text>
</svg>
白板上：四行算式带单位，最后一个框是决定。
**为什么这样说。** （约 1 分钟。）面试官要看你敢不敢说「不用分片」，并且有数字撑着。强的回答每一行带单位，最后一句是一个明确的决定；弱的回答是「数据量大，先分片」。
**面试官可能接着问。**
- 如果是 5,000,000 个商家呢？ → 张数、速率、存储都乘 10：写约 190 张/秒，读约 870 次/秒，17 TB；写仍然轻松，存储要靠分区和归档，是否分片看热数据多大。
- 月末那 3 天的假设错了呢？ → 如果全部集中在最后 1 天：10,000,000 ÷ 86,400 ≈ 116 张/秒，仍然是一台主库的量级；结论对这个假设不敏感。
- 2 KB 怎么来的？ → 我的假设：发票头加十几行明细的 JSON；给了别的数就改。
**常见失分。**
- **平均当峰值：** 月末的尖峰被抹平。
- **看见 TB 就分片：** 存储大不是分片的理由，要看读写。
- **不带单位：** 「一年一亿多」不知道是张还是行。
