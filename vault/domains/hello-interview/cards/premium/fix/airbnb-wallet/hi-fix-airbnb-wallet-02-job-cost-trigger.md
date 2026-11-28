---
id: hi-fix-airbnb-wallet-02-job-cost-trigger
node: fix.airbnb-wallet
type: qa
step: 2
---
## Q
**Airbnb Wallet · 为什么要 Kafka**｜复盘

面试官：「你说支付平台的状态更新走 Kafka。它在这个设计里解决什么问题？」

你会怎么回答？

## A
**当时的回答。**
- **Postgres 有理由：** 你说钱包和交易的更新要原子、读取要有序，这个理由很好。
- **Kafka 没有：** 它是设计后半段才加进来的，用来传状态更新；没有说它解决什么、多出多少延迟、重复消息怎么处理。
**差在哪。**
- **同一张图上两种标准：** Postgres 有作用、有取舍，Kafka 只有名字；面试官只能认为是习惯性地画上去的。
- **它在资金路径上：** 状态更新决定钱包余额，重复、乱序、延迟在这里都有后果，最该说清楚。
- **规模没支持它：** 转账约 16.5 笔/秒，峰值按 3 倍约 50 笔/秒；webhook 直接写 Postgres 完全扛得住。
**应该这样说。**
- **固定三句：** 「加 X。作用是……；代价是……；我在……时才加。」
- **Kafka 的版本：** 「Kafka 用来缓冲支付平台的更新，在它们来得比数据库写入者能安全处理的更快时。代价是多一段延迟、会重复投递、多一套要运维和监控的系统。只有当 webhook 直接写 Postgres 扛不住，或钱包更新服务宕机时不能丢平台的更新，我才加。」
- **说不全就不画：** 「这三句我现在填不全，所以先不放 Kafka，webhook 直接写 Postgres，一个事务。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 231">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">加一个组件之前，先填三句</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">作用（Job）</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">它解决的那一个具体问题</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">说不出，就不是现在要加的</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">代价（Cost）</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">多出的延迟、重复、运维</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每一项配一个处理办法</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">触发（Trigger）</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">什么数字出现时才加</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">没有触发条件，先不画</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 179">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">钱包设计里的两个组件</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">Postgres：你说清楚了</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">作用：钱包和交易要原子更新、有序读</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">代价：单主库；触发：从第一天就要</text>
<rect x="8" y="93" width="324" height="74" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">Kafka：后加的，三句缺三句</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">作用？webhook 峰值才 50 笔/秒</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">代价？延迟、重复投递、多一套运维</text>
<text x="18" y="156.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">触发？没有说</text>
</svg>
白板上：每个组件旁边写三行，作用、代价、触发；缺一行的先擦掉。
**为什么这样说。** （约 1 分钟。）面试官判断的是你是不是在用组件解决问题。强的回答每个组件带三句，并且敢说「现在不加」；弱的回答是先画一个队列，被问到才补理由。
**面试官可能接着问。**
- 不加 Kafka，更新服务宕机时平台的更新不就丢了？ → 平台的 webhook 会重发一段时间，每日扫描还会按 vendor id 补查，所以丢的是时间，不是数据；如果平台不重发，或要求几分钟内恢复，这就是加的触发。
- 什么数字出来你就加？ → webhook 峰值持续超过写库余量（例如几千次/秒），或宕机时不能丢更新（平台不重发、要求分钟级恢复），或需要多个下游订阅同一份事件。
- 加了以后重复消息怎么办？ → 按 vendor event id 去重，处理和去重记录在同一个事务里。
**同类题。**
- **GoFundMe 的队列与 Redis：** 同样先说不加的版本，再说为什么加。
- **任何后加的缓存、分片：** 开口之前先过一遍三句。
