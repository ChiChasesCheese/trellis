---
id: bagu-sharding-2-shard-key
node: a.mysql.sharding
type: qa
step: 2
---
## Q
**分库分表 · 垂直、水平拆分与分片键**｜必会

面试官：「要拆了，垂直拆和水平拆有什么区别？订单表的分片键选什么？」

## A
**基本回答。** 垂直拆分是按业务把表拆到不同的库，或者把大字段拆成扩展表；水平拆分是把同一张表按分片键拆到多个库、多张表里。分片键选「查询最常带的列」，让绝大多数查询只落在一个分片上，订单表按 `user_id` 分。其他维度的查询，用异步同步的副本解决。
**一句话记住。** 垂直拆像把一家大超市按部门拆成「生鲜店」「日用品店」；水平拆像把同一家店复制成十家分店，按顾客手机尾号决定去哪家。选尾号还是选购买时间当依据，决定了顾客以后是只去一家店，还是要把十家店都问一遍。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="8" y="10" width="128" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="72" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单查询</text>
<text x="72" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">带 user_id</text>
<rect x="8" y="100" width="128" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="72" y="116.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">商家查订单</text>
<text x="72" y="131.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不带 user_id</text>
<rect x="240" y="14" width="92" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="286" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片 0</text>
<rect x="240" y="58" width="92" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="286" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片 1</text>
<rect x="240" y="102" width="92" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="286" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分片 2</text>
<line x1="136" y1="30" x2="234.474" y2="71.6622" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="240.0,74.0 232.3,74.2 234.8,68.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="136" y1="120" x2="235.463" y2="33.9263" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="240.0,30.0 236.8,37.0 232.6,32.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="136" y1="120" x2="234.513" y2="76.427" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="240.0,74.0 234.9,79.8 232.3,73.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="136" y1="120" x2="234.001" y2="118.115" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="240.0,118.0 233.1,121.3 232.9,114.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">user_id 查询只落一个分片；商家查询要扫全部分片</text>
<text x="8" y="188" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">解法：另建一份按 merchant_id 分的副本，异步同步</text>
<text x="8" y="208" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">时间做分片键：新数据全压在最后一片，写热点</text>
<text x="8" y="226" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">垂直拆分：按业务拆库、大字段拆扩展表</text>
</svg>
用户按 `user_id` 查订单，只会找到一个分片（深色高亮）；商家查自己的订单不带 `user_id`，路由不到具体分片，只能去扫全部分片（虚线），所以要另建副本。
**讲明白。**
- **垂直拆分：** 按业务把不同的表放到不同的库（订单库、用户库、商品库），或者把一张表里的大字段（如商品详情的长文本）拆到扩展表。它能隔离业务，互不拖累，但解决不了单表行数太多的问题。
- **水平拆分：** 同一张表的行，按分片键分到多个库表里。这才是真正分摊行数和写入压力的做法。
- **分片键怎么选：** 选查询最常带的列。订单表里，用户查「我的订单」最常见，所以按 `user_id` 分，这样绝大多数查询只落在一个分片，不用扫全部。
- **选完要验证：** 看数据分布是否均匀，有没有热点分片。
- **其他维度的查询：** 商家查自己的订单不带 `user_id`，会扫全部分片，代价很高。做法是另建一份按 `merchant_id` 分的副本，异步同步；运营「按时间查全部订单」同理，改查异步同步的汇总副本。
- **为什么不用时间做分片键：** 新数据都是最近的时间，全部压到最后一个分片，形成写热点；历史分片几乎闲置，写入能力并没有被分摊。
**举个例子。** 订单按 `user_id` 分片，假设 3 个分片，按 `user_id` 取模：
1. **用户 7 查订单：** 7%3=1，只访问分片 1，一次查询搞定。
2. **商家 A 查自己的订单：** 不带 `user_id`，不知道订单在哪个分片，只能 3 个分片都查，再合并。
3. **建副本：** 另建一份订单副本，按 `merchant_id` 分片，由异步同步写入，商家查询改走它，只落一个分片。
4. **运营按时间查全部订单：** 改查异步同步的汇总副本，不去扫线上分片。
5. **反例：** 如果用下单时间做分片键，今天的所有订单都进同一个分片，它扛全部写入，其他分片闲着。
**容易错。**
- **以为垂直拆能解决行数：** 它只拆业务和大字段，单表行数没变。
- **按时间分片：** 新数据全压到最后一个分片，形成写热点。
- **选分片键不看查询：** 分片键要是查询里常带的列，否则大量查询要扫全部分片。
- **忘了其他维度：** 商家、运营的查询要靠异步同步的副本解决，不能硬扫。
**业务场景。** 订单按 `user_id` 分片后，运营「按时间查全部订单」要扫所有分片，改查异步同步的汇总副本。
**系统设计。** [[links.payment-batch-processing|支付处理系统（授权冻结 + 每日批量结算）]]：画完订单与流水表后，问「按什么分片」，再追问「商户对账按商户查怎么办」。
**可能问法。**
- 分片键怎么选？ → 选查询最常带的列，让绝大多数查询只落一个分片，订单表按 user_id 分。选完要验证数据分布均匀、没有热点，其他维度的查询用异步同步的副本解决。
- 为什么不用时间分片？ → 新数据全压在最后一个分片，形成写热点，历史分片却几乎闲置，写入能力并没有被分摊。
- 按用户分了，商家怎么查订单？ → 商家查自己的订单不带 user_id，会扫全部分片，所以另建一份按 merchant_id 分的副本，异步同步；运营按时间查全部订单同理，改查异步同步的汇总副本。
