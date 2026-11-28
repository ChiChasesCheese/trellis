---
id: bagu-backlog-2-diagnose
node: a.mq.backlog
type: qa
step: 2
---
## Q
**消息积压 · 判断生产突增、消费变慢还是下游故障**｜必会

面试官：「lag 一直在涨，你怎么区分是生产突增、消费变慢，还是下游出了问题？」

## A
**基本回答。** 比较生产速率和消费速率；再看每个分区的 lag 是否均匀，以及消费者的单条耗时和错误。
**一句话记住。** 排查积压像医生看体检单：先量总体（生产、消费哪边变了），再看分项（哪个分区不对），最后看有没有反复发作（重平衡），三步就能分出病因。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">各分区的 lag（条数）</text>
<rect x="24" y="112" width="24" height="12" rx="2" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="36" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="62" y="106" width="24" height="18" rx="2" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="74" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="100" y="110" width="24" height="14" rx="2" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="112" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="138" y="104" width="24" height="20" rx="2" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="150" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="176" y="114" width="24" height="10" rx="2" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="188" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="214" y="108" width="24" height="16" rx="2" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="226" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="252" y="111" width="24" height="13" rx="2" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="264" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<rect x="290" y="32" width="24" height="92" rx="2" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="302" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<line x1="18" y1="124" x2="332" y2="124" stroke-width="1.2" stroke="currentColor"/>
<text x="168" y="60" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">分区 7 卡住不动</text>
<line x1="276" y1="56" x2="288" y2="56" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="288.0,56.0 281.0,59.2 281.0,52.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="162" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">整体都涨 → 比生产和消费速率</text>
<text x="8" y="182" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">单分区高 → 毒消息或热点分区</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">消费忽停忽走 → 重平衡</text>
</svg>
八个分区的 lag 柱子，分区 0 到 6 都很低，只有分区 7 很高：整体消费没问题，是这一个分区里有东西卡住，多半是毒消息。如果八根柱子一起长高，才是整体的生产与消费失衡。
**讲明白。**
- **先比两个速率：** 生产速率翻倍而消费速率不变，是生产突增；消费速率下降，是消费变慢。
- **消费变慢看三处：** 单条耗时有没有变长，线程是不是卡住了，下游调用的响应时间是不是变慢。
- **再看分区是否均匀：** 整体都涨和只有个别分区涨，是两类不同的问题。只有某个分区 lag 不动，多半是毒消息（反复处理失败的消息）卡住了这个分区，也可能是热点分区（某个 key 的消息特别多）。
- **毒消息怎么卡住分区：** 一个分区里的消息要按顺序处理。第一条坏消息一直失败、一直重试，后面的消息都排在它后面，整个分区就停了。
- **频繁重平衡也会停顿：** 消费者频繁崩溃重启，会触发重平衡（rebalance，消费组重新分配分区）。重分配期间消费暂停，lag 就涨。
- **毒消息走死信：** 不要让一条坏消息阻塞整个分区，限制重试次数，超限就送进死信队列。
- **下游慢先限流降级：** 如果是下游慢，就先对下游调用限流或降级，别让消费者线程都挤在那里等。
**举个例子。** 视频发布后转码事件积压，8 个分区：
1. **看整体：** 生产速率和平时差不多，说明不是生产突增。
2. **看分区：** 分区 0 到 6 的 lag 都只有几百条，分区 7 有五万条而且一直没动。
3. **看分区 7 的消费者日志：** 同一条消息反复解析失败，一直在重试，这是一条格式错误的毒消息。
4. **处理：** 限制重试次数，超限后把它送进死信队列并告警，分区 7 立刻恢复消费；修好解析逻辑后再从死信重放。
**容易错。**
- **以为 lag 涨就是消费者不够：** 只有一个分区涨，加消费者也没用，因为一个分区同一时刻只会被组里的一个消费者读。
- **以为重试越多越稳：** 对毒消息无限重试会把分区堵死，要限制次数并送死信。
- **忘了重平衡：** 消费者反复重启时，消费一直在被打断，光看单条耗时看不出来。
**业务场景。** 视频发布后转码事件积压，发现只有分区 7 的 lag 不动：一条格式错误的消息让消费者一直重试。
**系统设计。** [[links.youtube|视频平台（YouTube）]]：上传处理流水线里面试官问「某个视频一直转码不出来」，先看是不是只有一个分区卡住（毒消息），再看下游转码集群是不是慢。
**可能问法。**
- 怎么定位积压原因？ → 先比生产速率和消费速率：生产翻倍而消费不变是生产突增；消费速率下降就看单条耗时、线程是否卡住、下游响应时间；只有个别分区 lag 不动，是毒消息或热点分区。再看消费者是否频繁崩溃重启触发重平衡。
- 单分区 lag 不动怎么办？ → 多半是一条毒消息让消费者在该分区上反复失败重试。限制重试次数，超限就把消息送进死信队列并告警，主流程继续往下消费。然后修复解析逻辑后重放死信。同时要排除该分区的消费线程卡在下游调用上。
- 消费者频繁重平衡怎么办？ → 原因通常是处理一批消息超过 max.poll.interval.ms 被判定离线，或心跳超时、长 GC。对策：减小 max.poll.records，加快单批处理或把耗时逻辑异步化，适当调大间隔；用静态成员（group.instance.id）减少重启触发，用协作式再平衡降低影响。
