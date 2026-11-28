---
id: bagu-like-leaderboard-4-persist-recover
node: a.scenario.like-leaderboard
type: qa
step: 4
---
## Q
**榜单落库与恢复 · Redis 崩溃后怎么办**｜必会

面试官：「榜单落在 Redis 里，Redis 崩溃重启后榜单没了，怎么恢复？」

## A
**基本回答。** Redis 是实时视图，数据库才是真相；榜单分数是明细聚合出的派生数据，可重建。事件进消息队列，消费者批量落库：明细表记每个事件并用唯一索引防重，累计表存每个对象总数。Redis 崩溃后先从累计表批量 `ZADD` 重建，再从 MQ 位点回放之后的增量。回放要幂等：用事件 ID 去重，或 `ZADD key GT`（6.2 起）只在新分数更大时更新，旧快照不会把新分数覆盖回去。AOF（追加写命令）或 RDB（定期快照）只减少重建次数，丢最近几秒数据、整机丢失时仍要靠数据库。重建期间先返回上一份快照并标注更新时间，用户不会看到空榜。再定期用数据库聚合值对账，发现漂移就修正；榜单允许几秒最终一致，账务以数据库为准。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<rect x="8" y="24" width="96" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">点赞、打赏</text>
<text x="56" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">事件</text>
<line x1="104" y1="44" x2="111.0" y2="44.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118,44 111.0,47.2 111.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="118" y="24" width="70" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="153" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MQ</text>
<line x1="188" y1="44" x2="195.0" y2="44.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="202,44 195.0,47.2 195.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="202" y="24" width="130" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="267" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<text x="267" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">明细 + 累计表</text>
<line x1="267" y1="64" x2="166.6" y2="97.8" stroke-width="1.2" stroke="currentColor"/>
<polygon points="160,100 165.6,94.7 167.7,100.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="100" width="84" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="116.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis 崩溃</text>
<text x="50" y="131.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">榜单没了</text>
<line x1="92" y1="120" x2="97.0" y2="120.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="104,120 97.0,123.2 97.0,116.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="104" y="100" width="112" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160" y="116.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">累计表</text>
<text x="160" y="131.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">批量 ZADD</text>
<line x1="216" y1="120" x2="221.0" y2="120.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="228,120 221.0,123.2 221.0,116.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="228" y="100" width="104" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="280" y="116.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MQ 位点后</text>
<text x="280" y="131.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回放增量</text>
<text x="8" y="170" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">数据库是真相，榜单是可重建的视图</text>
<text x="8" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">回放要幂等：ZADD GT 只在新分数更大时更新</text>
<text x="8" y="208" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">重建期间先返回上一份快照</text>
</svg>
上一行是事件落库的正常路径；下一行是崩溃后重建：先用累计表批量写回，再补队列位点之后的增量。
**举个例子。** 打赏榜 Redis 故障重启：客户端先拿上一份快照；从累计表 `ZADD` 主播 x 为 100；回放 MQ 里这几分钟的打赏，已有 100 分时，旧快照里的 `ZADD GT 80` 不更新，更新的 `ZADD GT 120` 更新为 120。主播收益的账务走数据库，不受榜单影响。
**容易错。**
- **用普通 `ZADD` 回放旧数据：** 会把新分数改回去，要用 `GT`。
- **把榜单当账务：** 榜单可丢弃可重建，钱的真相在数据库。
