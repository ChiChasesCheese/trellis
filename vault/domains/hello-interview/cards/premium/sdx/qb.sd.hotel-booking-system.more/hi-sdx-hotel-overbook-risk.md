---
id: hi-sdx-hotel-overbook-risk
node: qb.sd.hotel-booking-system.more
type: qa
step: 1
---
## Q
**超订比例按池大小算**｜补充 · 酒店预订系统 · 追问

面试官：「酒店允许超订，因为总有人不来。历史未到店率是 6%，产品想统一设成『超订 2%』。对 50 间房的小池子和 500 间房的大池子，这个比例各自合适吗？如果把『到店人数超过房数』的风险控制在 1% 以内，怎么定？」

## A
**结论。** 统一的百分比不对。到店人数近似服从二项分布（binomial），池越大相对波动越小，所以安全的超订比例随池大小变化：50 间的池订 51 间（+2%）风险已是 4.26%，超出预算；500 间的池可以订到 519 间（+3.8%）。

**要点。**
- **建模：** 每个订单以 94% 的概率到店，到店人数服从 Binomial(订单数, 0.94)，风险是到店人数超过房数的概率。
- **小池子：** 50 间房订 51 间，要 51 人全部到店才超员：0.94 的 51 次方 ≈ 4.26%，超出 1% 预算，所以几乎没有安全的超订空间。
- **大池子：** 500 间房订 519 间，超员概率约 0.64%；订 520 间升到 1.12%，越过预算。
- **按池计算：** 以房型加日期为单位，用历史未到店率求出满足风险预算的最大订单数，写进库存行的超订上限。
- **落地：** 库存条件更新里把 `reserved < total` 换成 `reserved < overbook_limit`，事务逻辑不变。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<rect x="10" y="8" width="155" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="87.5" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">50 间的池</text>
<text x="87.5" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">订 51 间 (+2%)</text>
<rect x="175" y="8" width="155" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="252.5" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">500 间的池</text>
<text x="252.5" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">订 519 间 (+3.8%)</text>
<rect x="10" y="62" width="155" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="87.5" y="80.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">到店超过房数的概率</text>
<text x="87.5" y="95.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4.26%，超出 1% 预算</text>
<rect x="175" y="62" width="155" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="252.5" y="80.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">到店超过房数的概率</text>
<text x="252.5" y="95.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0.64%，仍在 1% 内</text>
<text x="8" y="128" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">未到店率 6%，到店人数 ~ Binomial(订单数, 0.94)</text>
<text x="8" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">池越大，相对波动越小（大数定律），</text>
<text x="8" y="162" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">所以安全的超订比例随池大小变化。</text>
</svg>

**为什么。** 每个订单到不到店相互独立时，到店人数的标准差随池大小的平方根增长，相对波动随之变小，大池可以多超订一些。更完整的做法是比较被挤走客人的赔偿成本和空一间房的损失，求总成本最低的超订量。

**面试里这样说。** 「超订上限我按房型和日期单独算：用历史未到店率建二项分布，找出到店人数超过房数的概率不超过 1% 的最大订单数，写成库存行的超订上限。比如 6% 未到店，50 间房订 51 间风险就有 4.26%，500 间房可以订到 519 间。」

**易错。**
- **全站一个固定比例：** 小池子会超员，大池子浪费收入。
- **假设未到店相互独立：** 团队订单、天气和活动会让未到店同涨同落，实际方差更大，要留余量。
- **只看概率不看代价：** 超员一次要赔偿和转送，成本远高于空一间房。
