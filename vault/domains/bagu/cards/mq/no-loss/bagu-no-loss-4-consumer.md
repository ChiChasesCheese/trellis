---
id: bagu-no-loss-4-consumer
node: a.mq.no-loss
type: qa
step: 4
---
## Q
**消息不丢 · 消费端提交位移**｜必会

面试官：「消费者先提交 offset 再处理，还是先处理再提交？为什么？」

## A
**基本回答。** 关闭自动提交 `enable.auto.commit=false`，处理完再手动提交 offset。先提交后处理，处理失败消息就丢了。
**一句话记住。** 提交 offset 就像在书里夹书签：先夹书签再读，读到一半断电，重启后从书签往后读，中间那段就漏了；先读完再夹书签，断电最多重读一遍，但不会漏。宁可重读，不要漏读。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 240">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">先提交，后处理</text>
<rect x="8" y="24" width="96" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="56.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拉到消息</text>
<line x1="104" y1="39" x2="120" y2="39" stroke-width="1.2" stroke="currentColor"/>
<polygon points="120.0,39.0 113.0,42.2 113.0,35.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="24" width="96" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="168.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">提交 offset</text>
<line x1="216" y1="39" x2="232" y2="39" stroke-width="1.2" stroke="currentColor"/>
<polygon points="232.0,39.0 225.0,42.2 225.0,35.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="232" y="24" width="96" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="280.0" y="43.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">处理时崩溃</text>
<text x="8" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">重启后从已提交位置继续 → 这条消息丢了</text>
<text x="8" y="104" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">先处理，后提交</text>
<rect x="8" y="114" width="96" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="56.0" y="133.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拉到消息</text>
<line x1="104" y1="129" x2="120" y2="129" stroke-width="1.2" stroke="currentColor"/>
<polygon points="120.0,129.0 113.0,132.2 113.0,125.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="114" width="96" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="168.0" y="133.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">处理完成</text>
<line x1="216" y1="129" x2="232" y2="129" stroke-width="1.2" stroke="currentColor"/>
<polygon points="232.0,129.0 225.0,132.2 225.0,125.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="232" y="114" width="96" height="30" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="280.0" y="133.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">提交前崩溃</text>
<text x="8" y="166" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">重启后从旧位置重来 → 重复收到，靠幂等去重</text>
<text x="8" y="192" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">enable.auto.commit=false，处理完手动提交</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">重平衡：onPartitionsRevoked 先提交已处理的</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">以重复换不丢</text>
</svg>
第一条是先提交后处理：提交之后崩溃，那条消息永远被跳过；第二条是先处理后提交：提交前崩溃，重启后会重来，只是重复。
**讲明白。**
- **offset 是什么：** 消费者记录自己「读到分区的第几条了」。重启后，从上次提交的位置继续。
- **先提交后处理的问题：** 提交的那一刻，系统就认为这条消息已经读过了。处理失败或崩溃，重启后从下一条开始，这条消息就丢了。
- **先处理后提交：** 最坏是处理完没来得及提交就崩溃，下次重复收到，用幂等去重即可。以重复换不丢。
- **自动提交的问题：** 自动提交按时间间隔提交已拉取的位移，不管业务是否处理完：拉到消息后还没处理就提交了，处理中崩溃消息就丢。所以要关闭 `enable.auto.commit`，在处理完后手动提交。
- **所以消费端必须幂等：** 处理完但没来得及提交就崩溃，下次会重复收到。
- **不能指望「恰好一次」：** 确认消息本身可能丢，分布式里实际是至少一次加幂等。
- **重平衡时：** 重平衡会让分区换主：在 `onPartitionsRevoked` 里提交已处理完的 offset，减少重复。
**举个例子。** 积分服务消费「支付成功」事件，offset 当前是 100。
1. **先提交后处理：**读到 offset 100 的消息，先提交（下次从 101 开始），再去加积分。
2. **崩溃：**加积分时服务崩溃，积分没加成。
3. **重启：**从 101 开始，offset 100 这笔积分永久丢了。
4. **先处理后提交：**读到 100，先加积分，加完再提交。
5. **在提交前崩溃：**重启后从 100 重新开始，再收到这条消息，加积分又一次。靠幂等（按消息 ID 去重）避免重复加。
**容易错。**
- **用自动提交：** 时间到就提交，不管业务是否处理完，处理中崩溃会丢。
- **图省事先提交后处理：** 处理失败就丢，应先处理后提交。
- **以为先处理后提交不会出问题：** 会重复，要幂等。
- **追求恰好一次：** 分布式里实际是至少一次加幂等。
- **重平衡时不提交：** 新消费者会把已处理的再处理一遍，增加重复。
**业务场景。** 积分服务读到「支付成功」后先提交位移再加积分，加积分时服务崩溃，这笔积分就永久丢了。
**系统设计。** 「[[links.notification-system-scale|通知系统（支持单发与群发，百万级每秒）]]」问「消费者崩溃重启后消息会丢还是重复」，答手动提交加通知幂等。
**相关题。** 练习题 idempotent-transfer
**可能问法。**
- 先提交还是先处理？ → 先处理，处理完再手动提交 offset。先提交后处理，处理失败消息就丢了；先处理后提交，最坏是处理完没来得及提交就崩溃，下次重复收到，用幂等去重即可。以重复换不丢。
- 自动提交有什么问题？ → 自动提交按时间间隔提交已拉取的位移，不管业务是否处理完：拉到消息后还没处理就提交了，处理中崩溃消息就丢。所以要关闭 enable.auto.commit，在处理完后手动提交。
- 消费者崩溃会重复吗？ → 会。处理完但没来得及提交 offset 就崩溃，重启后从上次提交的位置继续，这批消息重新消费。重平衡时在 onPartitionsRevoked 里先提交已处理的 offset 可以减少重复，最终靠幂等兜底。
