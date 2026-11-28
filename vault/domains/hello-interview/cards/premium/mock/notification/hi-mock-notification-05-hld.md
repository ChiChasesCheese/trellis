---
id: hi-mock-notification-05-hld
node: fix.notification-mock
type: qa
step: 5
---
## Q
**通知系统 · 第 5 步 · 高层设计**｜模拟面试

面试官：「好，现在画高层设计：一条回执从产品团队到用户手机，经过哪些组件？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先说最小版，再用数字推翻它：** 「最小版是两个盒子：无状态的通知 API，加一个 SQL 状态库，中间一组 worker。我拿数字检验：峰值 83k 行/秒，单个主库按约 2 万行/秒算，差 4 倍，所以写入口前面要加东西。」
- **日志，作用、代价、触发：** 「我加一个持久的日志（Kafka）。作用：吸收峰值，并把受理和发送拆开，崩溃后消息不丢。代价：多一跳约 5 到 10 毫秒，消息会重复，多一套要运维的集群。触发条件：峰值写是单库的 4 倍。」
- **按优先级拆成两个主题：** 「tx 放回执，bulk 放活动，各自有自己的积压、自己的消费者。分区键用 notification_id，同一个 id 的两份重复消息会落在同一个分区、由同一个消费者按顺序处理。回执一天 1 亿条，峰值 3.5k/秒，8 个分区；活动 64 个分区：每个消费者按 1,000 条/秒算，要 40 个消费者，留出余量。」
- **worker 做什么：** 「读一条消息，查偏好，渲染模板，向限流器取令牌，调供应商，写状态。」
- **限流器：** 「每个供应商一个令牌桶，放在 Redis 里；它保护供应商，也保护我们的账号不被封。额度怎么在回执和活动之间分，深入三讲。」
- **状态库：** 「分片的 SQL，每条消息一行，notification_id 上有唯一约束。它回答『这条发了没有』，也是去重的最后一道防线。」
- **一条回执走一遍：** 「产品团队 POST，API 校验、写日志、回 202；tx 的 worker 读到、查偏好、取令牌、调苹果；状态库里记 sent；苹果或邮件供应商之后通过回调告诉我们结果。」
- **现在不画的：** 「重试主题、死信、熔断、活动的扇出作业、对账。我讲到那个问题时再加，并且说作用、代价、触发。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 366">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">高层设计：先最小，再加</text>
<rect x="8" y="26" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">产品团队 → 通知 API（无状态）</text>
<text x="170" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">校验 · 配额 · 写日志 · 回 202</text>
<polyline points="90,70 90,100" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="90,100 86.8,93 93.2,93" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="96" y="89" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">append（acks=all）</text>
<rect x="8" y="100" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="118.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">日志（Kafka，分区键 notification_id）</text>
<text x="170" y="133.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">tx：回执　bulk：活动</text>
<polyline points="90,144 90,174" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="90,174 86.8,167 93.2,167" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="96" y="163" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">两类各自消费</text>
<rect x="8" y="174" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="192.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">worker（回执池 · 活动池各一组）</text>
<text x="170" y="207.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">偏好 → 模板 → 取令牌 → 发送 → 写状态</text>
<polyline points="87,218 87,248" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="87,248 83.8,241 90.2,241" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="93" y="237" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">取令牌</text>
<polyline points="253,218 253,248" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="253,248 249.8,241 256.2,241" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="259" y="237" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">写状态</text>
<rect x="8" y="248" width="158" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="87" y="266.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">限流器</text>
<text x="87" y="281.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个供应商一个令牌桶</text>
<rect x="174" y="248" width="158" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="253" y="266.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">状态库</text>
<text x="253" y="281.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">分片 SQL · 唯一键</text>
<polyline points="87,292 87,318" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="87,318 83.8,311 90.2,311" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="318" width="200" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="108" y="336.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">供应商</text>
<text x="108" y="351.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">APNs · FCM · Email · SMS</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 231">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">日志：作用 · 代价 · 触发</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">作用</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">吸收 83k/秒的峰值；崩溃后不丢</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">把受理和发送拆开：先落日志再慢慢发</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">代价</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">多一跳，约 5–10 ms；消息会重复</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">多一套要运维、要监控滞后的集群</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">触发</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">峰值写 83k/秒 ≫ 单库约 2 万/秒（4 倍）</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没有这个差距就不加</text>
</svg>
白板上新增：七个盒子，从产品团队一路到供应商，以及日志的作用、代价、触发。
**为什么这样说。** （约 7 分钟，累计第 19 分钟。）面试官看第一版是不是最小的、能跑通的，以及每一个盒子有没有理由。他当时先画了 SQL 状态库，被问「一个库扛得住 10 万次每秒写吗」才加了 Kafka，而且没有说出代价。强的回答先自己用数字推翻最小版，再加组件；弱的回答是等着被追问。
**面试官可能接着问。**
- 为什么用 Kafka，不用数据库当队列？ → 数据库做队列要靠轮询和行锁，83k/秒会把主库打满；日志是顺序追加，单个 broker 约 100 万条/秒，83 MB/秒对它是小数目。
- 为什么拆两个主题，不用一个主题加优先级字段？ → Kafka 没有优先级队列；一个主题里回执会排在活动后面。拆开之后，回执的积压只取决于回执自己的到达速率。
- 限流器的 Redis 挂了呢？ → 每个 worker 退回本地保守的令牌桶：额度按 worker 数均分；宁可慢，不能超额。
- 状态库可不可以不要，只靠日志？ → 日志保留几天，回答不了「一个月前那张回执发了没有」，也做不了去重的最后一道防线，所以要有。
**常见失分。**
- **一上来画 Kafka，说不出理由：** 没有数字证明写不动。
- **先画库再被迫加日志：** 他当时就是这样，也没有说出代价。
- **回执和活动同一个主题：** 后面讲隔离没有地方落脚。
- **应用服务器直接连用户：** 他当时画了一条直连线，漏掉了通知服务。
