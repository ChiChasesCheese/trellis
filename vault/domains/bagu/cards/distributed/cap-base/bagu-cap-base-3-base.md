---
id: bagu-cap-base-3-base
node: a.distributed.cap-base
type: qa
step: 3
---
## Q
**BASE · 三个要素与 ACID 的关系**｜必会

面试官：「BASE 理论是什么？它和 ACID 是什么关系？」

## A
**基本回答。** BASE 有三个要素：基本可用（Basically Available），故障时允许损失部分可用性，如响应从 0.5 秒变 3 秒、大促时关评论和推荐保下单支付，但不是整体不可用；软状态（Soft state），允许存在中间态；最终一致（Eventually consistent），没有新更新后，各副本或各状态最终收敛。ACID 要求事务一执行完就进入终态；BASE 在分布式下接受中间态，靠补偿和重试收敛，是 ACID 在分布式场景下的工程折中。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ACID：单库事务，要么全成要么全不成</text>
<rect x="8" y="24" width="96" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">扣库存</text>
<text x="56" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">建订单</text>
<line x1="104" y1="44" x2="115.0" y2="44.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="122,44 115.0,47.2 115.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="122" y="24" width="96" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">一起提交</text>
<line x1="218" y1="44" x2="229.0" y2="44.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="236,44 229.0,47.2 229.0,40.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="236" y="24" width="96" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="284" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">终态</text>
<text x="284" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">没有中间态</text>
<text x="8" y="92" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">BASE：跨服务，中间态客观存在</text>
<rect x="8" y="104" width="108" height="48" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="62" y="124.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">库存已预扣</text>
<text x="62" y="139.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">订单未创建</text>
<line x1="116" y1="120" x2="143.2" y2="113.6" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150,112 143.9,116.7 142.5,110.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="116" y1="136" x2="143.2" y2="142.4" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150,144 142.5,145.5 143.9,139.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="150" y="100" width="182" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="241" y="117" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">重试成功 → 订单建好</text>
<rect x="150" y="130" width="182" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="241" y="147" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">超时 → 库存回补</text>
<text x="8" y="180" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">中间态必须能收敛，不能永远停在中间</text>
</svg>
第一行是单库事务，一步到终态；第二行是跨服务，库存已扣、订单没建就是一个中间态，重试或超时回补让它走到终态。
**容易错。**
- **以为 BASE 就是不要一致性：** 它要的是最终一致，只是允许中间过程里有不一致。
- **以为最终一致是「迟早会好」不用管：** 必须有重试、补偿、超时回补和对账，主动把中间态推到终态。
- **以为基本可用是整体不可用：** 基本可用是只损失部分可用性，如变慢或关闭非核心功能。
- **把 BASE 当成 ACID 的反义词：** 它是分布式下的折中，核心资金账务照样要强一致。
**业务场景。** 抢票座位 A1 库存 1，先预扣再建订单：预扣后库存 0、订单没建，是中间态；订单服务暂不可用就重试，用户看到「处理中」；用户一直不支付，超时关单并把库存加回 1，没有回补座位永远被占住。
