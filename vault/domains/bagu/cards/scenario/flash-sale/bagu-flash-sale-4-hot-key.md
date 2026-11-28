---
id: bagu-flash-sale-4-hot-key
node: a.scenario.flash-sale
type: qa
step: 4
---
## Q
**热点库存与一致性 · key 怎么打散、两边不一致怎么办**｜必会

面试官：「所有请求都打同一个库存 key，Redis 单分片扛不住怎么办？Redis 和数据库的库存不一致又怎么处理？」

## A
**基本回答。** 库存 key 是写热点：只在一个分片上，该分片命令串行，CPU 打满后同分片其他业务也变慢；本地缓存吸收不了写，只能把 key 拆成多个子库存（如 `stock:1:{0..9}`）落到不同分片并行，请求随机挑一个扣，扣不到再试别的桶，一次买多件时在 Lua 里跨桶凑数。桶会不均匀，不能一个桶空了就告诉用户售罄；全部桶空后实例在本地内存标记已售罄，后续请求本地拒绝。不一致以数据库为准：Redis 预扣成功但订单没建成（服务崩、消息丢），Redis 少了库存，就发补偿消息或由死信队列触发归还；再配定时对账，两个方向都查：Redis 比数据库订单少的补回，订单有而 Redis 没扣的要扣，异常记录告警。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 184">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">拆之前：所有请求打一个 key</text>
<rect x="8" y="24" width="324" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">stock:1 → 一个分片，CPU 打满</text>
<text x="8" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">拆之后：随机挑一个子库存 stock:1:{0..9}</text>
<rect x="8" y="86" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="22" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="40" y="86" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="72" y="86" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="104" y="86" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="118" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="136" y="86" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="168" y="86" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="182" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="200" y="86" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="214" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="232" y="86" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="246" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="264" y="86" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="278" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="296" y="86" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="310" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<text x="8" y="140" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">某个桶先空了 → 重试别的桶</text>
<text x="8" y="160" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">两边不一致 → 以数据库为准，补偿 + 对账</text>
</svg>
第一行是一个 key 把压力全压在一个分片上；第二行拆成十个子库存，分到不同分片并行处理。
**举个例子。** 总库存 1000 拆 10 桶、每桶 100：请求随机挑 3 号桶扣成功剩 99；挑到已空的 7 号就重试别的桶。某用户在 3 号桶预扣成功但订单没建成，Redis 总库存比订单数少 1，补偿消息把 1 件归还 3 号桶，对账也会发现并告警。
**业务场景。** 爆款每秒 10 万次抢购都打同一个库存 key，所在分片 CPU 打满、同分片其他 key 变慢；拆成 10 个子库存后压力分摊到多个分片。
**容易错。**
- **不一致时以 Redis 为准：** Redis 可能丢数据，真相是数据库里的订单。
