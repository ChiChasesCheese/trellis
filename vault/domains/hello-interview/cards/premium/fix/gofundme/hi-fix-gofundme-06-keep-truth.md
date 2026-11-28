---
id: hi-fix-gofundme-06-keep-truth
node: fix.gofundme
type: qa
step: 6
---
## Q
**GoFundMe · 第 35:37 分 · 保持：捐款行是真相**｜复盘

面试官：「热门活动的每一笔捐款都在更新活动行上的总额字段，这一行会成为瓶颈。怎么办？」

你会怎么回答？

## A
**当时的回答。**
- **不依赖可变总额行：** 你意识到热点行上有丢失更新，不想只靠它。
- **回到捐款记录：** 总额应当能从唯一的捐款记录得出，Redis 只是服务用的副本。
**差在哪。**
- **方向是对的：** 真相和副本分开，这一点已经让面试官放心。
- **层次没画全：** 三层各是什么没有写出来，后面追问「重放会不会多加」时，就没有地方放「已经加过」的记录。
**应该这样说。**
- **说三层：** 「真相是 donations，每笔一行；派生值是 campaign_totals，每个活动一行；展示副本是 Redis。」
- **说规则：** 「只有 Success 的行才算；总额永远能用 SUM 重建。」
- **说读路径：** 「页面读 Redis；Redis 没有就读 campaign_totals；对账时用 SUM 校正。」
- **说热点在哪：** 「热点不在 donations，那里每笔插一行，互不冲突；热点在总额行。所以总额由工作进程按事件累加，不由每个请求去改。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 306">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">三层：谁是真相，谁是副本</text>
<rect x="8" y="28" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="48" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Redis · 展示副本</text>
<text x="18" y="63" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">campaign:{id}:total</text>
<text x="18" y="78" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">可丢、可重建；页面先读它</text>
<rect x="8" y="120" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="140" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">campaign_totals · 持久化总额</text>
<text x="18" y="155" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个活动一行；只在应用事件时加</text>
<text x="18" y="170" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Redis 没有或可疑时读它</text>
<rect x="8" y="212" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="232" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">donations · 真相</text>
<text x="18" y="247" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每笔一行；status = Success 才算</text>
<text x="18" y="262" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SUM 可以重建上面两层</text>
<polyline points="60,120 60,90" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="60,90 63.2,97.0 56.8,97.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="66" y="108" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SET = 持久化值</text>
<polyline points="250,212 250,182" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="250,182 253.2,189.0 246.8,189.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="244" y="200" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SUM 重建</text>
<text x="8" y="296" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">副本出错就丢掉重建，真相出错才是事故</text>
</svg>
白板上：从上到下三层，向上的两条箭头是「SET 成持久化值」和「SUM 重建」。
**面试官可能接着问。**
- SUM 每次都算会不会慢？ → 读路径上不算；只在对账或重建时跑，有 (campaign_id, status) 索引。
- 为什么不直接用 Redis 当总额？ → Redis 可能丢数据或被淘汰，它是副本，不是账。
- 总额行真会成为瓶颈吗？ → 按前面的估算，峰值写每秒 150 笔，即使一个活动独占全部，单行更新也扛得住；真超过了，再拆成 N 个子计数行，读时求和。
**同类题。**
- **Ad Click Aggregator：** 点击明细是真相，聚合是派生。
- **YouTube Top K、Leaderboard：** 排名由事件算出，随时能重建。
- **FB Live Comments：** 点赞数、评论数的计数。
