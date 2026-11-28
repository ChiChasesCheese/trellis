---
id: bagu-key-design-1-key-naming-structure
node: b.redis.key-design
type: qa
step: 1
---
## Q
**Redis Key 设计 · 命名与结构选择**｜追问

面试官：「缓存订单、购物车这类对象，key 怎么命名？用 String 还是 Hash？为什么要避免大 key 和永不过期的 key？」

## A
**基本回答。** key 按「业务:对象:id」分层，如 `order:1001:info`，短而可读（key 名本身占内存，数量多时累积）；前缀便于按业务监控内存、批量清理、避免重名。整体读写用 String 存 JSON；经常只改某几个字段用 Hash：`HSET` 只改一个字段、省带宽，而 String 存 JSON 改一个字段要整串读出再写回，两个客户端各改一个字段时后写的覆盖先写的。Hash 代价：字段多了变大 key，字段不能单独设 TTL（字段级过期 7.4 才有）。所有缓存 key 都设过期并加随机抖动，永不过期的让内存只增不减、最终被迫淘汰；同一刻过期的一批 key 会同时回源。大 key（String 超 10KB、集合超 5000 个元素）会阻塞单线程；无限增长的集合（某用户名下全部设备）别塞一个 key，要分页或按页拆分。购物车：`cart:{uid}` 一个 Hash，field 是商品 ID、value 是数量，加购用递增。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 216">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">key = 业务 : 对象 id : 用途</text>
<rect x="8" y="22" width="72" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="44" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">order</text>
<text x="91" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">:</text>
<rect x="102" y="22" width="72" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="138" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1001</text>
<text x="185" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">:</text>
<rect x="196" y="22" width="72" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="232" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">info</text>
<text x="44" y="66" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">业务前缀</text>
<text x="138" y="66" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">对象 id</text>
<text x="232" y="66" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">用途</text>
<text x="8" y="94" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">要改订单的 status 字段</text>
<rect x="8" y="102" width="152" height="62" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="84" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">String 存 JSON</text>
<text x="84" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">改一个字段要</text>
<text x="84" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">整个 JSON 重写</text>
<rect x="172" y="102" width="160" height="62" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="252" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Hash：每字段一格</text>
<text x="252" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">HSET 只改 status</text>
<text x="252" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">字段不能单独设 TTL</text>
<text x="8" y="188" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">所有缓存 key 设过期时间，并加随机抖动</text>
<text x="8" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">大 key：String &gt;10KB、集合 &gt;5000 个元素</text>
</svg>
上半是 key 的三段命名；下半比较改订单状态：String 要整串重写，Hash 只改一个字段但字段不能单独设 TTL。
**业务场景。** 订单缓存把整个 JSON 放 String，改一个状态要整体重写；改成 Hash 后只更新 `status`，同时 key 带业务前缀、统一 TTL。
**容易错。**
- **以为 Hash 一定比 String 好。**
- **以为 Hash 字段能单独过期：** 7.4 之前不行。
- **把无限增长的数据放进一个 key。**
