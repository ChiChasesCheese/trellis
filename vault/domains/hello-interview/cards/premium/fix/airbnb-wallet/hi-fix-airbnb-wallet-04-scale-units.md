---
id: hi-fix-airbnb-wallet-04-scale-units
node: fix.airbnb-wallet
type: qa
step: 4
---
## Q
**Airbnb Wallet · 带单位的估算**｜复盘

面试官：「钱包用户 10,000,000，每人每周 1 笔转账，每天看 2 次余额或历史。重新算一下转账速率、一年多少笔、存储多大。」

你会怎么回答？

## A
**当时的回答。**
- **修正后的数字没有单位：** 重新算转账和存储时，数字报出来没有「每秒、每年、GB」。
- **全年笔数偏小：** 年转账量被低估了，但你仍然用规模来支持存储和读的选择。
**差在哪。**
- **面试官分不清你在说什么：** 没有单位，看不出一个数是速率、总数还是字节。
- **错的数量级推出错的设计：** 笔数偏小，存储和索引的选择就建立在假数字上；面试官要回头逐条核对。
- **混在一起算：** 速率、笔数、字节是三次不同的换算，一口气说完，中间错了也看不出。
**应该这样说。**
- **转账速率：** 「10,000,000 笔/周 ÷ 604,800 秒/周 ≈ 16.5 笔/秒。」
- **全年笔数：** 「10,000,000 × 52 周 = 520,000,000 笔/年。」
- **读速率：** 「10,000,000 用户 × 2 次/天 = 20,000,000 次/天；÷ 86,400 秒/天 ≈ 231 次/秒。」
- **存储：** 「520,000,000 笔 × 500 字节 = 2.6 × 10^11 字节 = 260 GB/年；留 7 年 ≈ 1.8 TB，这是索引和副本之前。」
- **回算一遍再下结论：** 「验一下：16.5 笔/秒 × 31,536,000 秒/年 ≈ 520,000,000 笔/年，对得上。峰值按 3 倍：写约 50 笔/秒，读约 700 次/秒，一台主库够，不用分片。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 283">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">10,000,000 用户，每人每周 1 笔，每天看 2 次</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">转账速率（次/秒）</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">10,000,000 笔/周 ÷ 604,800 秒/周</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">≈ 16.5 笔/秒；峰值 ×3 ≈ 50 笔/秒</text>
<rect x="8" y="93" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">全年笔数（笔/年）</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">10,000,000 × 52 周 = 520,000,000 笔/年</text>
<rect x="8" y="145" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="163.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">读（次/秒）</text>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">10,000,000 × 2 次/天 = 20,000,000 次/天</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">÷ 86,400 秒/天 ≈ 231 次/秒</text>
<rect x="8" y="212" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="230.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">存储（GB/年、TB）</text>
<text x="18" y="245.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">520,000,000 笔 × 500 字节 = 260 GB/年</text>
<text x="18" y="260.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">× 7 年 ≈ 1.8 TB（不含索引、副本）</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 138">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">速率、笔数、字节：三次换算，分开写</text>
<rect x="8" y="26" width="102.67" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="59.33" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">次/秒</text>
<text x="59.33" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">速率</text>
<rect x="118.67" y="26" width="102.67" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">笔/年</text>
<text x="170" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">数量</text>
<rect x="229.33" y="26" width="102.67" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="280.67" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">GB / TB</text>
<text x="280.67" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">字节</text>
<polyline points="170,70 170,90" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,90 166.8,83 173.2,83" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="90" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="108.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每一行都写：数 × 单位 ÷ 单位 = 数 单位</text>
<text x="170" y="123.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">结论放在最后一行，不在中间</text>
</svg>
白板上：四行带单位的算式，结论只在最后。
**为什么这样说。** （约 1 分钟。）面试官要的是能被检查的数字。强的回答每一行带单位，换算分开写，最后一句说它改变了什么设计；弱的回答是一个总数，加一句「所以量很大」。
**面试官可能接着问。**
- 520,000,000 行的表，查一笔交易会不会慢？ → 按主键和 (wallet_id, created_at) 索引查，不扫表；热数据是最近几个月，约 130,000,000 行。
- 索引和副本怎么算？ → 索引按 2 倍是我的假设：1.8 TB × 2 ≈ 3.6 TB；副本是可用性的账，不是容量的账。
- 7 年哪里来的？ → 是假设的保留期，财务记录要留；超过两年的按月分区归档到便宜存储。
**同类题。**
- **GoFundMe 的估算：** 同样先写单位再回算，见「范围和估算」。
- **任何给了用户数的题：** 用户数 × 频率 ÷ 时间得速率，× 大小 × 保留期得存储。
