---
id: hi-fix-component-cost-03-gofundme-queue
node: fix.component-cost
type: qa
step: 3
---
## Q
**GoFundMe · 加组件：队列**｜补强

面试官：「捐款成功之后，总额怎么更新到 Redis？为什么要用队列？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先说不加的版本：** 「规模小的话，可以在把状态改成 Success 的同一个事务里累加总额，不需要队列。」
- **职责：** 「我加队列，是为了让支付路径不等总额更新，也让通知、对账可以订阅同一个事件。」
- **新问题：** 「队列至少投递一次：会重发、会重放，还可能乱序。」
- **处理：** 「事件只在状态变成 Success 时，经 outbox 发出。工作进程先往 applied 插入 donation_id，唯一键；插入成功才累加；顺序不重要，因为每个事件只加自己的金额。」
- **防丢：** 「Success 和 outbox 行在同一个事务里写，投递器扫没发出去的行。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 378">
<rect x="8" y="8" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库 · Success 和 outbox 同一事务</text>
<text x="170" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">状态变成 Success 才有事件</text>
<rect x="8" y="100" width="324" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="16" y="131" width="58.6" height="7" fill="none" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="77.6" y="131" width="58.6" height="7" fill="none" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="139.2" y="131" width="58.6" height="7" fill="none" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="200.8" y="131" width="58.6" height="7" fill="none" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="262.4" y="131" width="58.6" height="7" fill="none" stroke-width="1" style="stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="119" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列 · 完成事件</text>
<rect x="8" y="192" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="210.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">工作进程</text>
<text x="170" y="225.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">消费、去重、累加</text>
<rect x="8" y="284" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="302.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">campaign_total_applied + campaign_totals</text>
<text x="170" y="317.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一个事务；唯一键挡重复</text>
<polyline points="90,52 90,100" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="90,100 86.8,93.0 93.2,93.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="96" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">投递器扫未发行</text>
<polyline points="90,144 90,192" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="90,192 86.8,185.0 93.2,185.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="96" y="174" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">至少一次</text>
<polyline points="90,236 90,284" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="90,284 86.8,277.0 93.2,277.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="96" y="266" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">先插 applied</text>
<text x="8" y="348" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新问题：重发、乱序。顺序不重要，</text>
<text x="8" y="366" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">因为每个事件只看自己的 donation_id</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 112">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">我要写在组件旁边的四行</text>
<rect x="8" y="26" width="324" height="76" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">加：队列，装成功的捐款事件</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">为了：支付路径不等总额更新</text>
<text x="18" y="75.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">新问题：会重发、会重放</text>
<text x="18" y="90.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">处理：applied 表唯一键；outbox 防丢</text>
</svg>
白板上：数据库到队列到工作进程到 applied；每条箭头旁写它的特性。
**为什么这样说。** （约 1 分钟。）面试官看你有没有把「至少一次」当成事实，而不是魔法。强的回答说出重发，并给出 applied 表这一个具体的记录。弱的回答是「用 Kafka，保证不丢」。
**面试官可能接着问。**
- 事件乱序会怎样？ → 总额的加法可以交换，每个事件只加自己的金额，所以不需要顺序。如果要按完成时间排最近 100 笔，就用事件里的完成时间，而不是到达的先后。
- 为什么不让支付服务直接去更新 Redis？ → 它可能崩在写库之后、调 Redis 之前，更新就丢了。outbox 把「写库」和「要发的事件」放进同一个事务。
- 队列堆积了呢？ → 总额落后几秒，支付路径不受影响，这正是加队列的目的；我监控堆积量。
**常见失分。**
- **当队列不会重复：** 没有 applied，重发就多加。
- **把「精确一次」当魔法：** 说不出记录在哪里。
- **双写：** 写库和发消息不在同一个事务里，崩一下就丢。
