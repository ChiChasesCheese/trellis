---
id: bagu-backlog-1-judge-first
node: a.mq.backlog
type: qa
step: 1
---
## Q
**消息积压 · 先判断还是先止血**｜必会

面试官：「大促后订单事件积压了 2 亿条，你第一步做什么？」

## A
**基本回答。** 先看消费组延迟（lag，也就是还没消费的消息条数）是在涨还是稳定，判断根因到底是生产突增、消费变慢还是下游故障；同时止血，不是盲目加机器。
**一句话记住。** 消息队列就像一个水池：进水是生产，出水是消费，水位就是 lag。水位在涨，先看是水龙头开大了、出水口堵了，还是下游排水管坏了；不看原因就多开几个出水口，下游堵着时一点用都没有。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<rect x="8" y="8" width="70" height="34" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="43" y="29.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">生产者</text>
<rect x="98" y="8" width="76" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="136" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列</text>
<text x="136" y="37" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">lag 在涨</text>
<rect x="194" y="8" width="70" height="34" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="229" y="29.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消费者</text>
<rect x="284" y="8" width="48" height="34" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="308" y="29.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">下游</text>
<line x1="78" y1="25" x2="98" y2="25" stroke-width="1.2" stroke="currentColor"/>
<polygon points="98.0,25.0 91.0,28.2 91.0,21.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="174" y1="25" x2="194" y2="25" stroke-width="1.2" stroke="currentColor"/>
<polygon points="194.0,25.0 187.0,28.2 187.0,21.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="264" y1="25" x2="284" y2="25" stroke-width="1.2" stroke="currentColor"/>
<polygon points="284.0,25.0 277.0,28.2 277.0,21.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="68" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">① 生产突增 → 限流、削峰、扩容</text>
<text x="8" y="90" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">② 消费变慢 → 查线程和单条耗时</text>
<text x="8" y="112" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">③ 下游故障 → 加机器没用，先修下游</text>
<line x1="8" y1="128" x2="332" y2="128" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="8" y="148" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同时止血：限流，或降级低价值消息</text>
<text x="8" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">保住核心链路，再按根因修</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">lag = 分区最新位点 − 已提交位点</text>
</svg>
从左到右是一条消息的路：生产者写进队列，消费者读出来，再去调下游。队列这一格的 lag 在涨，说明后面至少有一格跟不上；三种根因各对应一格，对策也不同。
**讲明白。**
- **为什么先判断：** 积压 2 亿条时最想做的就是加机器，但根因不同，对策完全不同。判断错了，机器加了也没用，还白白占资源。
- **生产突增：** 上游一下子写得比平时多很多。对策是限流、削峰（把尖峰摊平）、扩容。
- **消费变慢：** 消费者自己处理得慢，比如线程卡住、单条耗时变长。对策是去查消费者。
- **下游故障：** 消费者线程都卡在等下游（比如库存服务）响应。这时加机器没用，新加的线程也会一起卡住，还可能把本来就慢的下游压得更垮，要先修下游。
- **lag 稳定和上涨：** lag 稳定说明生产和消费速度平衡，只是有一批存量；lag 持续上涨说明消费能力小于生产，积压会越来越大，要立刻处理。
- **止血和查根因同时做：** 不要等查完根因再动手。先限流，或者降级低价值消息，保住核心链路，再按根因去修。
- **lag 怎么算：** 消费组延迟 = 分区最新的 offset（位点）减去消费者已提交的 offset，也就是还没消费的条数。它是积压告警的核心指标。
**举个例子。** 大促后订单事件积压了 2 亿条，按顺序排查：
1. **看 lag 趋势：** 曲线一直往上，说明消费能力小于生产，不是单纯的存量。
2. **比较速率：** 生产速率和平时差不多，消费速率却掉到了平时的一小部分，说明不是生产突增，问题在消费这一侧。
3. **看消费者线程：** 线程栈都卡在调用下游库存服务上，说明是下游慢。
4. **决定动作：** 不加消费者（加了也是一起卡住），先修库存服务，同时给低价值消息降级，保住下单核心链路。
**容易错。**
- **积压了就加机器：** 机器只解决「消费者算得慢」这一种根因。生产突增要限流削峰，下游故障加机器没用，甚至会压垮下游。
- **lag 大就一定出问题：** 要看趋势。lag 稳定只是有存量，持续上涨才是消费跟不上。
- **先查清根因再止血：** 查根因要花时间，这段时间积压还在涨。止血和排查要同时进行。
**业务场景。** 大促后订单事件积压 2 亿条：先看 lag 在涨，再看消费者线程卡在下游库存服务，说明该先修下游而不是扩消费者。
**系统设计。** [[links.notification-system-scale|通知系统（支持单发与群发，百万级每秒）]]：峰值流量时面试官问「消息积压怎么办」，先说判断（lag 趋势、三种根因），再说扩容和降级。
**相关题。** 练习题 bounded-blocking-queue
**可能问法。**
- 消息积压怎么处理？ → 先判断再止血：看消费组 lag 是在涨还是稳定，区分生产突增（限流、削峰、扩容）、消费变慢（查消费者）、下游故障（加机器没用，先修下游）；同时限流或降级低价值消息保住核心链路，再按根因修。
- 积压了第一步做什么？ → 看消费组延迟（lag）的趋势，判断根因，同时止血，不是盲目加机器。lag 持续涨说明消费能力小于生产，稳定则只是有存量。
- lag 是什么？ → 消费组延迟：分区最新的 offset 减去消费者已提交的 offset，即还没消费的消息条数。持续上涨说明消费慢于生产，稳定说明生产和消费平衡但有存量，它是积压告警的核心指标。
