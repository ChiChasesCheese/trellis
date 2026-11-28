---
id: bagu-why-mq-1-benefit-cost
node: b.mq.why-mq
type: qa
step: 1
---
## Q
**为什么用消息队列 · 收益与代价**｜必会

面试官：「下单后要发券、加积分、发通知，为什么不直接同步调用，要上消息队列？它有什么坏处？」

## A
**基本回答。** 三个收益：削峰（高峰请求先排队，下游按自己的速度消费）、解耦（上游不必知道有哪些下游，加下游不改上游）、异步（非核心步骤不占主链路耗时）。代价是可用性依赖 MQ、只能最终一致、复杂度上升。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同步：耗时相加，任一个挂了下单失败</text>
<rect x="10" y="22" width="60" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="40" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">下单</text>
<rect x="84" y="22" width="60" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="114" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发券</text>
<rect x="158" y="22" width="60" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="188" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">加积分</text>
<rect x="232" y="22" width="60" height="32" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="262" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发通知</text>
<line x1="70" y1="38" x2="84" y2="38" stroke="currentColor" stroke-width="1.2"/>
<polygon points="84,38 77.7,41.0 77.7,35.0" fill="currentColor"/>
<line x1="144" y1="38" x2="158" y2="38" stroke="currentColor" stroke-width="1.2"/>
<polygon points="158,38 151.7,41.0 151.7,35.0" fill="currentColor"/>
<line x1="218" y1="38" x2="232" y2="38" stroke="currentColor" stroke-width="1.2"/>
<polygon points="232,38 225.7,41.0 225.7,35.0" fill="currentColor"/>
<text x="10" y="92" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">异步：下单只发一条消息</text>
<rect x="10" y="130" width="56" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38" y="151" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">下单</text>
<rect x="96" y="130" width="60" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="126" y="151" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MQ</text>
<line x1="66" y1="147" x2="96" y2="147" stroke="currentColor" stroke-width="1.2"/>
<polygon points="96,147 89.7,150.0 89.7,144.0" fill="currentColor"/>
<rect x="226" y="100" width="90" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="271" y="119" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发券</text>
<line x1="156" y1="147" x2="226" y2="115" stroke="currentColor" stroke-width="1.2"/>
<polygon points="226,115 221.5,120.4 219.0,114.9" fill="currentColor"/>
<rect x="226" y="140" width="90" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="271" y="159" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">加积分</text>
<line x1="156" y1="147" x2="226" y2="155" stroke="currentColor" stroke-width="1.2"/>
<polygon points="226,155 219.4,157.3 220.1,151.3" fill="currentColor"/>
<rect x="226" y="180" width="90" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="271" y="199" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发通知</text>
<line x1="156" y1="147" x2="226" y2="195" stroke="currentColor" stroke-width="1.2"/>
<polygon points="226,195 219.1,193.9 222.5,188.9" fill="currentColor"/>
<text x="10" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">下游按自己的速度消费，增删下游不改上游</text>
</svg>
第一排是同步：四步串联，耗时相加，任何一步坏了下单就失败；第二排是异步：下单只发一条消息，三个下游各自消费。
**举个例子。** 下单后要发券、加积分、发通知，各自 100 毫秒：
1. **同步：** 依次调用，总耗时约 300 毫秒；通知服务挂了，下单整个失败。
2. **改成 MQ：** 下单成功后只发一条「订单已创建」消息，下单耗时只加一次发消息的时间。
3. **三个下游：** 发券、积分、通知各自订阅这条消息，按自己的速度消费，通知挂了不影响发券和积分。
4. **高峰：** 大促时每秒涌入大量订单，消息先在队列里堆着，积分服务慢慢消费，不会被压垮。
5. **代价：** 积分晚几秒到账；消息可能重复，积分服务要幂等；出问题时顺着 traceId 找消息链路。
**容易错。**
- **以为 MQ 只有好处：** 它引入可用性依赖、消息丢重乱序、最终一致和排查难度。
- **把强一致的步骤也异步化：** 扣库存、扣款需要立刻拿到结果，应走同步。
- **没做幂等就上 MQ：** 消息可能重复，不幂等会重复发券、重复加分。
- **小系统也引入 MQ：** 流量小、没有解耦和削峰需求时，多出的运维成本不值得。
