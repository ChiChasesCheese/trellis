---
id: bagu-delayed-task-1-order-timeout
node: b.scenario.delayed-task
type: qa
step: 1
---
## Q
**延时任务 · 订单超时自动取消**｜追问

面试官：「订单 30 分钟未支付要自动取消，怎么设计？怎么避免和支付成功撞车？分布式定时任务怎么保证准时且只执行一次？」

## A
**基本回答。** 下单时发一条延迟消息，30 分钟后投递，消费者查订单仍待支付就取消；再加定时扫表兜底，防消息丢失。取消和支付成功抢同一行，用状态机条件更新，只有一方改成功：`UPDATE orders SET status = 'CLOSED' WHERE id = ? AND status = 'UNPAID'`，影响行数 0 即已被处理（支付同理 `WHERE status = 'UNPAID'` 改 `PAID`）。不能先查状态再取消：查和改之间用户可能付款。任务调用超时不代表没执行，重试要带幂等键或靠条件更新让重复无害；多实例靠唯一键、条件更新或租约抢占保证只执行一次。
**对比。**
- MQ 延迟消息：RocketMQ 4.x 只有 18 个固定级别、最长 2 小时；5.x 起支持任意时间点，开源版默认最长 3 天。
- Redis ZSet：score 存到期时间，`ZRANGEBYSCORE` 取到期的，多消费者领取要用 Lua 保证原子。
- 时间轮：预读加时间轮，每秒拉未来 5 秒到期的任务进内存，少查库又精准。
- 数据库轮询：量小加索引，简单可靠。
- 不要依赖 Redis 过期事件：key 真正删除时才发布，可能很晚；发布订阅不持久化，宕机期间丢；广播给所有实例会重复处理。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 266">
<rect x="6" y="20" width="60" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="36.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">下单</text>
<rect x="86" y="20" width="120" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="146.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">延迟消息 30 分钟</text>
<rect x="226" y="20" width="108" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="280.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">到点投递</text>
<line x1="66" y1="35" x2="84" y2="35" stroke-width="1.2" stroke="currentColor"/>
<polygon points="84.0,35.0 77.0,38.2 77.0,31.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="206" y1="35" x2="224" y2="35" stroke-width="1.2" stroke="currentColor"/>
<polygon points="224.0,35.0 217.0,38.2 217.0,31.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="70" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">实现：延迟消息 / Redis ZSet / 时间轮</text>
<text x="8" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">到点瞬间：取消和支付回调抢同一行</text>
<rect x="6" y="108" width="140" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="76.0" y="125.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">取消任务</text>
<text x="76.0" y="140.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">UNPAID → CLOSED</text>
<rect x="194" y="108" width="140" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="264.0" y="125.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">支付回调</text>
<text x="264.0" y="140.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">UNPAID → PAID</text>
<line x1="76" y1="148" x2="130" y2="174" stroke-width="1.2" stroke="currentColor"/>
<polygon points="130.0,174.0 122.3,173.8 125.1,168.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="264" y1="148" x2="210" y2="174" stroke-width="1.2" stroke="currentColor"/>
<polygon points="210.0,174.0 214.9,168.1 217.7,173.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="60" y="176" width="220" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170.0" y="195.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单这一行：只有一方改成功</text>
<text x="8" y="230" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">输的一方影响行数 = 0，什么都不改</text>
<text x="8" y="250" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">兜底：定时扫表；别依赖 Redis 过期事件</text>
</svg>
上半部分是时间线：下单发延迟消息，30 分钟后到点投递。下面是到点瞬间：取消任务和支付回调改同一行，条件更新让只有一方成功，输的一方影响行数为 0。
**举个例子。** 订单 O1 10:00:00 下单，状态 `UNPAID`，同时发 30 分钟后的延迟消息。平稳时 10:30:00 消费者条件更新成 `CLOSED`、释放库存。撞车时 10:29:59.9 支付回调先到并改成 `PAID`，0.1 秒后取消任务的条件不成立、影响行数 0，什么也不做；反过来取消先成功，支付回调走退款或拒绝。消息丢了，定时扫表每隔几分钟补取消「创建超 30 分钟仍是 UNPAID」的订单。
**容易错。**
- **只用延迟消息不兜底：** 消息丢了订单永远不取消。
