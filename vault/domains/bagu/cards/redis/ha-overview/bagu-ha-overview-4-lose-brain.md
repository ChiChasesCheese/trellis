---
id: bagu-ha-overview-4-lose-brain
node: a.redis.ha-overview
type: qa
step: 4
---
## Q
**异步复制 · 切换会丢哪些写，脑裂是什么**｜必会

面试官：「主从是异步复制，切换后会丢数据吗？什么是脑裂？怎么减少损失？」

## A
**基本回答。** 会丢：主库执行完立刻回复客户端，复制异步，宕机时没传出去的写，从库升主后就不存在了。脑裂：主库只是被网络隔离、仍接受写，哨兵把从库升为新主，出现两个主库；网络恢复后旧主降为从库并全量同步，先清空自己的数据，隔离期间写进它的全部丢失。缓解：主库配 `min-replicas-to-write 1` 和 `min-replicas-max-lag 10`（旧名 `min-slaves-*`），联系不上从库或延迟超 10 秒就拒绝写，用可用性换一致性，把丢失窗口压到约 10 秒内，但只是缩小窗口，不能消除。`WAIT numreplicas timeout` 让关键写等至少 N 个从库确认，但新主不一定是确认过的那个，仍非强一致，超时后返回的是实际确认数，调用方要自己检查。切换后新主不知道旧主刚授出的锁，两个客户端可能同时持锁，要靠围栏令牌（fencing token，单调递增，存储层拒绝带旧数字的写）兜底。根本办法：不能丢的数据放数据库，Redis 只放可重建的数据。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 276">
<rect x="8" y="14" width="74" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="45" y="32.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端 A</text>
<line x1="82" y1="29" x2="108" y2="29" stroke-width="1.2" stroke="currentColor"/>
<polygon points="108,29 101.0,32.2 101.0,25.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="108" y="8" width="104" height="42" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="160" y="25" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">旧主</text>
<text x="160" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">仍在接受写</text>
<line x1="8" y1="76" x2="332" y2="76" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="170" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">网络隔离</text>
<rect x="8" y="98" width="74" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="45" y="116.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">哨兵</text>
<line x1="82" y1="113" x2="108" y2="113" stroke-width="1.2" stroke="currentColor"/>
<polygon points="108,113 101.0,116.2 101.0,109.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="108" y="92" width="104" height="42" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="160" y="109" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">从库升主</text>
<text x="160" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">= 新主</text>
<rect x="258" y="98" width="74" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="295" y="116.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端 B</text>
<line x1="258" y1="113" x2="212" y2="113" stroke-width="1.2" stroke="currentColor"/>
<polygon points="212,113 219.0,109.8 219.0,116.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="156" width="324" height="46" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="175" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网络恢复：旧主降为从库，全量同步</text>
<text x="170" y="190" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">隔离期间写进旧主的数据全部丢失</text>
<text x="8" y="226" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">缓解：主库配 min-replicas-to-write 1</text>
<text x="8" y="244" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">和 min-replicas-max-lag 10</text>
<text x="8" y="264" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">联系不上从库就停写，窗口压到约 10 秒</text>
</svg>
虚线是网络隔离：上半旧主还被客户端 A 写着，下半哨兵已把从库升为新主、客户端 B 在写它；恢复后旧主的数据被清掉。
**业务场景。** 一主一从加哨兵：10:00:00 M 与 R、哨兵网络断了但客户端 A 仍能连 M；10:00:30 哨兵把 R 升主，B 开始写 R；10:00:30–10:05:00 A 继续往 M 写；10:05:00 恢复后 M 降为从库全量同步，A 那批全丢。配了 min-replicas 后 M 超 10 秒联系不上从库就拒写。用户余额缓存同理：切换丢了最后两秒的扣减，所以扣币以账务库事务为准，Redis 余额只展示并定时对账。
**容易错。**
- **以为配了就不会丢。**
- **以为 WAIT 就是强一致。**
- **以为旧主降级后保留自己的数据。**
