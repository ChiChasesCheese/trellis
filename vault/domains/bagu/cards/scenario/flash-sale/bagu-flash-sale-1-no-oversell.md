---
id: bagu-flash-sale-1-no-oversell
node: a.scenario.flash-sale
type: qa
step: 1
---
## Q
**秒杀整体方案 · 库存怎么扣才不超卖**｜必会

面试官：「设计一个秒杀系统，零点 10 件库存来了 1 万 QPS，库存怎么扣才不超卖？」

## A
**基本回答。** 不超卖的根本是「判断库存大于 0」和「扣减」必须是一个原子操作：先 `SELECT` 再 `UPDATE` 是两步，两个请求同时读到 1、各扣一次，库存变 -1。所以分层过滤加内存预扣加异步落库加数据库兜底：前端倒计时、置灰、验证码拦机器人；网关走 CDN 并按用户、IP 限流；服务层库存为 0 后直接返回「已售罄」，99% 请求在此结束；Redis 用 Lua 原子「判断加扣减」决定谁有资格（同一商品打在数据库同一行扛不住，Redis 内存串行快几个数量级）；抢到的写入 MQ，订单服务按自己的速度异步建单，削峰；数据库条件更新是最后一道保险：`UPDATE stock SET n = n - 1 WHERE id = ? AND n > 0`，影响行数 0 即没抢到。Redis 预扣放行量要比库存略多，因为有人不付款，库存靠超时回补放回去。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">零点 1 万个请求抢 10 件，层层过滤</text>
<rect x="8" y="24" width="324" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">前端 + 网关：置灰、验证码、限流</text>
<rect x="8" y="66" width="324" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="85" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务层：库存为 0 直接返回已售罄</text>
<line x1="170" y1="54" x2="170.0" y2="59.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,66 166.8,59.0 173.2,59.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="108" width="324" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="127" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis + Lua 原子预扣：只有 10 个成功</text>
<line x1="170" y1="96" x2="170.0" y2="101.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,108 166.8,101.0 173.2,101.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="150" width="324" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="169" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消息队列：异步创建订单</text>
<line x1="170" y1="138" x2="170.0" y2="143.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,150 166.8,143.0 173.2,143.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="192" width="324" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="211" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库：条件更新 WHERE n > 0 兜底</text>
<line x1="170" y1="180" x2="170.0" y2="185.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,192 166.8,185.0 173.2,185.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
</svg>
请求一层层往下走，每层挡掉一大批，最后只有抢到的少数人到达数据库；高亮的那一层决定谁有资格。
**举个例子。** 库存剩 1 件，A、B 同时点：先查再改时两人都读到 `n = 1`，各扣一次得 -1，一件卖给两个人；条件更新时 A 影响 1 行，B 此时 `n > 0` 不成立、影响 0 行，被告知没抢到。全量：零点 1 万请求抢 10 件，Redis 只放行 10 个，其余 9990 个在服务层返回售罄，数据库只处理 10 个订单。
**容易错。**
- **以为 Redis 预扣了就不用数据库兜底：** Redis 可能丢数据、与数据库不一致，条件更新是最后一道保险。
- **以为分层是重复劳动：** 每层挡不同的流量（机器人、超量、售罄后），缺一层压力就落到下一层。
