---
id: hi-sdx-ecom-read-heavy-numbers
node: more.e-commerce
type: qa
step: 1
---
## Q
**电商估算：瓶颈在读不在写**｜补充 · 电商平台（Amazon） · 必会

面试官：「5000 万日活浏览商品页，每天约 85 万笔订单，平均每单 2.3 件商品。黑色星期五订单量是平时的 5 倍，其中 60% 集中在 4 小时里，再留 2 倍突发余量。算一下读和写的峰值，说说该重点扩哪里，库存扣减要不要上 Redis？」

## A
**结论。** 读写比约 1400:1，读峰值约 20 万 QPS，而下单峰值只有 354 笔/秒、扣库存约 814 次/秒。要扩的是读路径（缓存、CDN 预热）；普通商品用关系库的一条条件 UPDATE 就够，不上 Redis。只有促销爆款这一个商品要单独做准入控制。

**要点。**
- **读写比：** 每人每天约 24 次浏览，12 亿次 ÷ 85 万单 ≈ 1400:1。
- **读峰值：** 12 亿 ÷ 86400 ≈ 1.39 万/秒；日内峰值按 3 倍、黑五按 5 倍，约 20 万/秒。
- **写峰值：** 85 万 × 5 = 425 万单，60% 即 255 万单落在 14400 秒里，是 177 笔/秒，再乘 2 得 354 笔/秒。
- **库存扣减：** 354 × 2.3 ≈ 814 次/秒，低于单主库每秒数千次条件更新的量级；平日 22.6 次/秒乘 6 也只有 136 次/秒。
- **例外是爆款：** 一个 SKU 的竞争集中在一行，只有它走秒杀式准入和 Redis 脚本，其余不动。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<rect x="10" y="8" width="320" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读 ≈ 20 万/s（1400:1）</text>
<text x="170.0" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">CDN + 缓存，开卖前预热</text>
<rect x="10" y="62" width="320" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="80.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">下单 ≈ 354 笔/s</text>
<text x="170.0" y="95.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">普通单主库，不必特殊扩容</text>
<rect x="10" y="116" width="320" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="134.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">扣库存 ≈ 814 次/s</text>
<text x="170.0" y="149.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一条条件 UPDATE，不上 Redis</text>
<rect x="10" y="170" width="320" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="188.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">单个爆款 SKU：竞争集中在一行</text>
<text x="170.0" y="203.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">秒杀式准入控制 + Redis 脚本</text>
<text x="8" y="238" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">单主库对不同行的条件更新：每秒数千次</text>
</svg>

**为什么。** Redis 原子扣减多维护一份库存，主从切换还可能丢扣减，代价要用余量不够来换；关系库还有一两个数量级的余量时，加 Redis 只增加复杂度。

**面试里这样说。** 「读写比大约 1400 比 1，所以我先挡读：CDN 加缓存，开卖前预热。黑五下单峰值我算下来 354 笔/秒，扣库存约 800 次/秒，普通库存用一条 `UPDATE ... WHERE stock >= qty` 就够；只有爆款商品单独走准入控制。」

**易错。**
- **一上来就给库存加 Redis：** 数字没算，就引入了双写不一致。
- **只算平均不算峰值：** 平均 10 笔/秒的写入看着轻松，黑五的 354 笔/秒才是设计值。
- **把爆款也混在普通路径里：** 单行竞争不会被平均吞吐稀释。
