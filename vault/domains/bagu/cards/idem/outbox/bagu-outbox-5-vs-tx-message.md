---
id: bagu-outbox-5-vs-tx-message
node: a.idem.outbox
type: qa
step: 5
---
## Q
**本地消息表（Outbox）· 和事务消息（半消息）怎么选**｜追问

面试官：「RocketMQ 有事务消息，直接用它不就行了，为什么还要自己建 outbox 表？两者怎么选？」

## A
**基本回答。** 事务消息：先发半消息（half message，消费者看不到），再执行本地事务，最后提交或回滚；Broker（消息服务器）长时间没收到结果就回查生产者。outbox 不依赖具体 MQ，靠本地事务落库。换 MQ 或 MQ 不支持（如 Kafka）选 outbox；用 RocketMQ 又不想建表选事务消息。只需通知对方、对方有自己的幂等时，更轻的是最大努力通知：按间隔重试对方接口，超过次数转人工或对账。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">事务消息（RocketMQ）</text>
<text x="184" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Outbox 表</text>
<rect x="8" y="28" width="150" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="43.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发半消息</text>
<text x="83" y="58.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消费者看不见</text>
<line x1="83" y1="66" x2="83" y2="73" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83.0,80.0 79.8,73.0 86.2,73.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="80" width="150" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="103" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">执行本地事务</text>
<line x1="83" y1="118" x2="83" y2="125" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83.0,132.0 79.8,125.0 86.2,125.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="132" width="150" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="155" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">提交或回滚</text>
<line x1="83" y1="170" x2="83" y2="177" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83.0,184.0 79.8,177.0 86.2,177.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="184" width="150" height="38" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83" y="199.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没收到结果</text>
<text x="83" y="214.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Broker 回查生产者</text>
<rect x="184" y="28" width="148" height="38" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="258" y="43.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">业务更新 + outbox</text>
<text x="258" y="58.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">同一个本地事务</text>
<line x1="258" y1="66" x2="258" y2="73" stroke-width="1.2" stroke="currentColor"/>
<polygon points="258.0,80.0 254.8,73.0 261.2,73.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="184" y="80" width="148" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="258" y="95.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">中继发送</text>
<text x="258" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">轮询或 CDC</text>
<line x1="258" y1="118" x2="258" y2="125" stroke-width="1.2" stroke="currentColor"/>
<polygon points="258.0,132.0 254.8,125.0 261.2,125.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="184" y="132" width="148" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="258" y="155" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发成功后标记</text>
<text x="184" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">MQ 挂了业务照常提交</text>
<text x="8" y="244" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Broker 不可用，半消息发不出 → 业务被卡住</text>
<text x="8" y="258" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">两者都是至少一次，消费端都要幂等</text>
</svg>
左边：消息放在 Broker，靠半消息和回查保证一致。右边：消息放在自己的库里，靠同一个本地事务保证一致。最下面两行是它们的代价和共同点。
**容易错。**
- **以为 Kafka 事务能代替 outbox：** Kafka 事务只覆盖 Kafka 内部读写，不能和业务库原子提交，也没有半消息回查；Kafka 上做可靠事件用 outbox 加中继或 CDC，至少一次，消费端幂等。
- **以为事务消息不用幂等：** 回查和重投都可能带来重复，消费端仍要幂等。
- **忘了回查接口：** 事务消息一定要实现，用业务数据判断本地事务是否已提交，否则半消息悬着。
- **只看有没有表：** 事务消息省了表，但把业务的可用性绑在了 Broker 上。

**业务场景。** 支付结果通知商户：把回调任务存进 outbox，商户接口挂了就按退避重试并保留每次记录；用事务消息的话，回调状态和重试次数还得另存一份。
