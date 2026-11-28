---
id: bagu-no-loss-1-three-ends
node: a.mq.no-loss
type: qa
step: 1
---
## Q
**消息不丢 · 三个环节**｜必会

面试官：「支付成功事件发给积分服务不能丢。消息从发出到处理完，会在哪几个环节丢？」

## A
**基本回答。** 三个环节：生产端发出去没确认、Broker 收到后还没复制就宕机、消费端先提交位移后处理失败。三端一起配齐，得到至少一次（at-least-once）：不丢，但可能重复。
三端配置：生产端 `acks=all` 并等确认、失败重试（`acks=1` 时 leader 一挂，没复制出去的消息就丢）；Broker 端副本数不少于 3、`min.insync.replicas` 不少于 2、关闭 unclean leader 选举；消费端关闭自动提交，处理完再提交位移。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="16" y="6" width="80" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="56.0" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">生产端</text>
<rect x="4" y="56" width="104" height="62" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="56.0" y="76.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发出去没确认</text>
<text x="56.0" y="91.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">或 acks=1</text>
<text x="56.0" y="106.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">leader 一挂就丢</text>
<line x1="56" y1="34" x2="56" y2="56" stroke-width="1.2" stroke="currentColor"/>
<polygon points="56.0,56.0 52.8,49.0 59.2,49.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="56" y1="118" x2="56" y2="142" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="56.0,142.0 52.8,135.0 59.2,135.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="4" y="142" width="104" height="62" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="56.0" y="162.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">acks=all</text>
<text x="56.0" y="177.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">幂等 + 重试</text>
<text x="56.0" y="192.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">带回调发送</text>
<rect x="130" y="6" width="80" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Broker</text>
<rect x="118" y="56" width="104" height="62" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="76.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">副本太少</text>
<text x="170.0" y="91.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">或落后副本</text>
<text x="170.0" y="106.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">当了 leader</text>
<line x1="170" y1="34" x2="170" y2="56" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,56.0 166.8,49.0 173.2,49.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="118" x2="170" y2="142" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170.0,142.0 166.8,135.0 173.2,135.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="118" y="142" width="104" height="62" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="162.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3 副本</text>
<text x="170.0" y="177.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">min.insync=2</text>
<text x="170.0" y="192.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">关 unclean</text>
<rect x="244" y="6" width="80" height="28" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="284.0" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消费端</text>
<rect x="232" y="56" width="104" height="62" rx="3" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="284.0" y="76.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">先提交 offset</text>
<text x="284.0" y="91.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">后处理失败</text>
<text x="284.0" y="106.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">消息就丢了</text>
<line x1="284" y1="34" x2="284" y2="56" stroke-width="1.2" stroke="currentColor"/>
<polygon points="284.0,56.0 280.8,49.0 287.2,49.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="284" y1="118" x2="284" y2="142" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="284.0,142.0 280.8,135.0 287.2,135.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="232" y="142" width="104" height="62" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="284.0" y="169.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">手动提交</text>
<text x="284.0" y="184.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">处理完再提交</text>
<line x1="96" y1="20" x2="130" y2="20" stroke-width="1.2" stroke="currentColor"/>
<polygon points="130.0,20.0 123.0,23.2 123.0,16.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="210" y1="20" x2="244" y2="20" stroke-width="1.2" stroke="currentColor"/>
<polygon points="244.0,20.0 237.0,23.2 237.0,16.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">三端配齐 = 至少一次：不丢，可能重复</text>
<text x="8" y="252" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">重复靠消费端幂等去重</text>
</svg>
上排是三个环节，中间一排是每一环怎么丢，下排高亮的是对应的配置。三排对应起来看。
**举个例子。** 支付成功事件发给积分服务。
1. **生产端：**`acks=all`，等 Broker 确认才算发送成功；没确认就重试。
2. **Broker：**3 个副本，`min.insync.replicas=2`，一台宕机还有数据。
3. **消费端：**积分服务收到消息，先加积分，加完再提交位移。
4. **意外：**加完积分、没提交位移时服务崩溃。
5. **重启后：**这条消息重新到来，再加一次积分。靠幂等（按消息 ID 去重）避免重复加。
**容易错。**
- **只配生产端 acks=all 就以为不丢：** Broker 和消费端任何一端漏配都会丢。
- **以为配齐就是恰好一次：** 得到的是至少一次，会重复。
- **把重复当成 bug 去消除：** 重复是为了不丢付出的代价，在消费端用幂等处理。
- **先提交位移再处理：** 处理失败消息就丢了。
