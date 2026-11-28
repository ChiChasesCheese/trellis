---
id: bagu-ordering-5-version-other
node: a.mq.ordering
type: qa
step: 5
---
## Q
**消息顺序 · 业务兜底与其他 MQ**｜追问

面试官：「能不能让业务不依赖顺序？RabbitMQ、RocketMQ 怎么保证顺序？」

## A
**基本回答。** 更好的办法是让消费端对乱序也安全：消息带版本号或走状态机，发现状态非法或版本落后就丢弃或延后。RabbitMQ 是单队列单消费者；RocketMQ 是队列内顺序消息。
**一句话记住。** 保证消息「绝不乱序」是在给路修护栏，成本高；让业务「乱序也不出事」是给车装安全带，成本低还兜底。就像退货单永远不能比收货单先生效：收到不合理的就退回去。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 248">
<rect x="8" y="24" width="88" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="52.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">已创建</text>
<line x1="96" y1="39" x2="126" y2="39" stroke-width="1.2" stroke="currentColor"/>
<polygon points="126.0,39.0 119.0,42.2 119.0,35.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="126" y="24" width="88" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">已支付</text>
<line x1="214" y1="39" x2="244" y2="39" stroke-width="1.2" stroke="currentColor"/>
<polygon points="244.0,39.0 237.0,42.2 237.0,35.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="244" y="24" width="88" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="288.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">已发货</text>
<rect x="214" y="96" width="118" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="273.0" y="115.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">迟到消息：已支付</text>
<line x1="273" y1="96" x2="273" y2="56" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="273.0,56.0 276.2,63.0 269.8,63.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">当前状态已是「已发货」</text>
<text x="8" y="114" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">状态回退 → 丢弃</text>
<text x="8" y="156" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">状态机：已支付才能发货，非法流转丢弃或延后</text>
<text x="8" y="176" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">消息带版本号：版本落后就丢弃</text>
<text x="8" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">RabbitMQ：单队列单消费者</text>
<text x="8" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">RocketMQ：同 key 发往同一队列，队列内顺序消费</text>
</svg>
订单正常的状态流转是已创建、已支付、已发货。当前状态已是「已发货」，又收到一条迟到的「已支付」消息，状态机发现状态回退，直接丢弃。
**讲明白。**
- **为什么业务要兜底：** 即使分区内有序，失败重试也可能让后续消息先被处理。只靠消息队列保序，总有漏洞，业务层仍要靠状态机或版本号兜底。
- **版本号怎么用：** 消息带版本号或事件序号；收到比当前状态旧的版本，就丢弃或延后重试。这样旧消息不会覆盖新状态。
- **状态机怎么用：** 为业务实体定义合法的状态流转，如已支付才能发货。收到的消息若让状态回退或跳变，例如已发货的订单收到已支付，就直接丢弃或延后重试；合法的才更新。
- **条件更新：** 更新用 `WHERE status = 旧状态`，数据库层面保证只有当前状态对得上才改。
- **RabbitMQ 怎么保序：** 它保证的是单队列内按序，所以要单队列单消费者；一个队列多个消费者会乱序。要并行就拆成多个队列、每队列一个消费者，或一个消费者内部按 key 哈希到内存队列分发。
- **RocketMQ 怎么保序：** 同 key 发往同一队列，消费端按队列顺序消费，也就是队列内的顺序消息。
**举个例子。** 订单 100 的状态消息：创建、支付、发货。
1. **正常：**状态依次是 已创建 → 已支付 → 已发货。
2. **意外：**「已发货」处理完了，一条因重试迟到的「已支付」才到。
3. **状态机判断：**当前是已发货，而已支付是更早的状态，属于回退。
4. **处理：**直接丢弃（或延后重试），状态仍然是已发货。
5. **SQL 层面：**`UPDATE orders SET status='已支付' WHERE id=100 AND status='已创建'`，当前不是已创建，更新 0 行，什么都没改。
**容易错。**
- **以为 MQ 保序业务就不用管：** 重试和多线程都会破坏顺序，业务要兜底。
- **一个 RabbitMQ 队列配多个消费者还想保序：** 会乱序，要拆多队列，每队列一个消费者。
- **状态机只检查不合法流转，却不用条件更新：** 并发时仍可能覆盖，更新要带旧状态条件。
- **丢弃迟到消息前不确认：** 要看业务能否丢，有些场景是延后重试而不是直接丢。
**业务场景。** 订单状态消息迟到：已「已发货」的订单收到「已支付」消息，状态机发现状态回退，直接丢弃。
**系统设计。** 「[[links.ticketmaster|票务预订（Ticketmaster）]]」订单状态流转问「消息乱序时座位状态会不会错」，答状态机拒绝非法流转。
**可能问法。**
- 不依赖顺序怎么设计？ → 让消费端对乱序也安全：消息带版本号或事件序号，或走状态机；收到比当前状态旧的版本，或状态流转非法的消息，就丢弃或延后重试。这样即使失败重试让后面的消息先处理，状态也不会被旧消息覆盖。
- RabbitMQ 怎么保证顺序？ → RabbitMQ 保证的是单队列内按序，所以要单队列单消费者；一个队列多个消费者会乱序。要并行就拆成多个队列、每队列一个消费者，或一个消费者内部按 key 哈希到内存队列分发。
- 状态机怎么挡乱序？ → 为业务实体定义合法的状态流转，如已支付才能发货。收到的消息若让状态回退或跳变，例如已发货的订单收到已支付，就直接丢弃或延后重试；合法的才更新，更新用条件更新 WHERE status = 旧状态。
