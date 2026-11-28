---
id: hi-fix-component-cost-02-gofundme-redis
node: fix.component-cost
type: qa
step: 2
---
## Q
**GoFundMe · 加组件：Redis 里的总额**｜补强

面试官：「页面上要显示累计金额，热门活动每秒几千次读。你打算怎么做？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先说不加的版本：** 「最简单是每次对捐款表做 SUM。读每秒几千次，每次都扫，主库扛不住，所以要一个副本。」
- **职责：** 「我加 Redis，是为了让页面只读一个数，不碰主库。」
- **新问题：** 「Redis 里的数和真相可能不一致：事件重放会多加，重启会丢，崩在更新之前会落后。」
- **处理：** 「我不用 INCR，只用 SET，设成持久化的 campaign_totals 的值；丢了就读 campaign_totals 回填；对账时用 SUM 校正。」
- **说出边界：** 「落后几秒可以接受，多算不可以。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 229">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Redis 总额和真相分歧的三种情形</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">多了：事件重放，加了两次</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">修复：只 SET 成持久化的值</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一个值设几次都一样</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">没了：重启或被淘汰，读到空</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">修复：读 campaign_totals 回填</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">页面不直接去 SUM</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">旧了：崩在 SET 之前</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">修复：下一次刷新补上</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">允许几秒的落后，不允许多算</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 112">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">我要写在组件旁边的四行</text>
<rect x="8" y="26" width="324" height="76" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">加：Redis 里的总额</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">为了：页面每秒几千次读不碰主库</text>
<text x="18" y="75.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">新问题：副本可能和真相不一致</text>
<text x="18" y="90.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">处理：SET 成持久化值；丢了重建</text>
</svg>
白板上：三种分歧各有一个修复；旁边的四行是组件便签。
**为什么这样说。** （约 1 分钟。）面试官看你是不是把 Redis 当成账本。强的回答说清它只是副本，分歧的三种方式各有收口。弱的回答是「加 Redis 缓存加速」，被问重放时才想起来。
**面试官可能接着问。**
- Redis 整个挂了，页面怎么办？ → 回退读 campaign_totals：每个活动一行，按主键读。按主键读单行，每秒几千次主库顶得住一阵；同时对回填加单飞（single flight），避免大量请求同时打过去。
- 为什么不用 INCR？ → INCR 不记得谁加过；事件一重放就多加。SET 成持久化的值，设几次都一样。
- 要不要给键设 TTL？ → 可以设较长的 TTL 兜底。键过期的瞬间会有大量请求同时回填，所以回填只让一个请求去做，其余等它。
**常见失分。**
- **只说加速：** 没有说新问题，面试官会替你追问。
- **用 INCR 当总额：** 重放就多算。
- **说「定时同步一下」：** 同步什么、怎样不重复，都没说。
