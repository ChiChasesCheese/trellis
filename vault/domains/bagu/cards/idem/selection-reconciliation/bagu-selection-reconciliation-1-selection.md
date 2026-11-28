---
id: bagu-selection-reconciliation-1-selection
node: a.idem.selection-reconciliation
type: qa
step: 1
---
## Q
**分布式事务选型 · 2PC、TCC、Saga、本地消息表、事务消息各适合什么**｜必会

面试官：「一次下单要改订单库、库存库，还要给用户加积分。这几个服务的一致性你怎么选方案？2PC、TCC、Saga、本地消息表、事务消息分别什么时候用？」

## A
**基本回答。** 先想能不能不做跨服务事务（把相关数据放同一个库）。必须做时按需求选：强一致、参与者少、低并发用 2PC（协调者故障时参与者卡在准备状态，会阻塞）；要资源预留（冻结、预占）用 TCC（Try 预留、Confirm、Cancel 三个接口，代码要写三套）；流程长、跨多个服务用 Saga；只要「提交后下游一定收到」用 outbox 或事务消息加幂等消费；代码改不动用 Seata AT（框架在业务 SQL 前后记数据快照，失败按快照回滚）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 268">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">先问：能不能把数据放进同一个库？</text>
<rect x="8" y="28" width="176" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="96" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">强一致、参与者少、低并发</text>
<line x1="184" y1="42" x2="197" y2="42" stroke-width="1.2" stroke="currentColor"/>
<polygon points="204.0,42.0 197.0,45.2 197.0,38.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="204" y="28" width="128" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="268" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2PC</text>
<rect x="8" y="66" width="176" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="96" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">要预留资源（冻结、预占）</text>
<line x1="184" y1="80" x2="197" y2="80" stroke-width="1.2" stroke="currentColor"/>
<polygon points="204.0,80.0 197.0,83.2 197.0,76.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="204" y="66" width="128" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="268" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">TCC</text>
<rect x="8" y="104" width="176" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="96" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">流程长、跨多个服务</text>
<line x1="184" y1="118" x2="197" y2="118" stroke-width="1.2" stroke="currentColor"/>
<polygon points="204.0,118.0 197.0,121.2 197.0,114.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="204" y="104" width="128" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="268" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Saga</text>
<rect x="8" y="142" width="176" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="96" y="163" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">提交后下游一定收到</text>
<line x1="184" y1="159" x2="197" y2="159" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="204.0,159.0 197.0,162.2 197.0,155.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="204" y="142" width="128" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="268" y="155.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">outbox / 事务消息</text>
<text x="268" y="170.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">+ 幂等消费</text>
<rect x="8" y="186" width="176" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="96" y="204" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">代码改不动</text>
<line x1="184" y1="200" x2="197" y2="200" stroke-width="1.2" stroke="currentColor"/>
<polygon points="204.0,200.0 197.0,203.2 197.0,196.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="204" y="186" width="128" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="268" y="204" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Seata AT</text>
<text x="8" y="238" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">几乎都是：至少一次 + 幂等 + 补偿或重试</text>
</svg>
左边是你的需求，右边是对应的方案。最下面一行是它们的共同底色：不管选哪个，最终都是「至少一次 + 幂等 + 补偿或重试」。
**容易错。**
- **一上来就说 2PC 或 Seata：** 先要说清能不能避开跨服务事务，以及业务到底要多强的一致。
- **以为 Saga 有隔离性：** 每步直接提交，中间状态别人看得见，要靠业务设计（预占状态、状态机）兜住。
- **选了最终一致却不说兜底：** 没有幂等、补偿、对账，最终一致只是「可能最终不一致」。
- **把方案当互斥：** 同一次下单里，不同环节可以用不同方案（库存用预占，积分用 outbox）。

**业务场景。** 订单、库存、积分三个服务：订单与库存用「预占 + 超时释放」，积分走 outbox 事件异步加，不进同步链路；积分晚几秒不影响下单，库存要求立刻确定。
