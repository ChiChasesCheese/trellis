---
id: hi-mock-notification-08-dive-two-classes
node: fix.notification-mock
type: qa
step: 8
---
## Q
**通知系统 · 第 8 步 · 深入三：回执和活动共用一个供应商额度**｜模拟面试

面试官：「一个 1,000 万人的活动正在全速发送，这时一张支付回执来了。它怎么不排在活动后面？你们共用苹果同一份额度。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先给结论：** 「三层隔离，缺一层都不行：主题、消费者、供应商额度。」
- **第一层，主题：** 「回执在 tx，活动在 bulk，各有各的积压。回执的等待只取决于回执自己的到达速率，和活动堆了多少无关。」
- **第二层，消费者：** 「两组 worker、两个消费组。活动再忙，回执的 worker 线程不会被占用，这叫舱壁（bulkhead）。」
- **第三层，供应商额度：** 「这是他当时被追问才补上的那一层。两个池共用苹果同一份额度，如果只分主题，活动照样把额度吃光。苹果给我们的额度按 50,000 条/秒算（合同数，我假设）：回执桶 10,000 条/秒，活动桶 40,000 条/秒。回执峰值只有 3.5k/秒，留约 3 倍余量。」
- **借用规则：** 「回执桶满了，溢出的令牌流给活动桶，回执用不完的额度不浪费；活动永远拿不到回执桶里的令牌。」
- **怎么实现：** 「令牌桶放在 Redis 里，用 Lua 脚本保证原子；worker 每次取 100 个令牌，40,000 条/秒 ÷ 100 = 400 次/秒的 Redis 访问，很轻。」
- **算一遍活动的时间：** 「10,000,000 ÷ 40,000 条/秒 = 250 秒，约 4 分钟；500 万条的峰值积压 5,000,000 ÷ 40,000 = 125 秒清空。都在『10 分钟发完』的目标之内。」
- **怎么知道隔离在起作用：** 「监控 tx 主题最老消息的年龄，超过 5 秒就告警，并且自动把活动桶降速。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 192">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">推送额度 50,000/秒（合同，假设）</text>
<rect x="8" y="54" width="64.8" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="72.8" y="54" width="259.2" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="40.4" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">回执</text>
<text x="202" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">活动 40,000/秒</text>
<text x="8" y="46" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">回执 10,000/秒</text>
<polyline points="72,112 130,112" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="130,112 123,115.2 123,108.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="78" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">回执桶满了，溢出的令牌给活动</text>
<text x="8" y="170" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">活动拿不到回执桶里的令牌，反过来可以</text>
<text x="8" y="186" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">回执峰值 3.5k/秒，预留 10,000/秒，约 3 倍余量</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 256">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">三层隔离</text>
<rect x="8" y="26" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">① 主题</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">tx 与 bulk 各自积压，不排在一起</text>
<rect x="8" y="78" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="96.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">② 消费者</text>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">两个 worker 池、两个消费组</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">活动再忙，回执的线程不被占用</text>
<rect x="8" y="145" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="163.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">③ 供应商额度</text>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">令牌桶按类别预留；溢出才借</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每次取 100 个令牌：400 次/秒访问 Redis</text>
<text x="8" y="234" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">监控：tx 最老消息年龄 &gt; 5 秒告警；</text>
<text x="8" y="250" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">告警时自动把活动桶降速</text>
</svg>
白板上新增：额度条（回执 10,000/秒，活动 40,000/秒，溢出箭头），和三层隔离。
**为什么这样说。** （约 3 分钟，累计第 30 分钟。）面试官要看你能不能把「回执不被活动饿死」落到三处具体机制，每一处都能说出数字。他当时先讲到分区和分开的消费者，面试官指出两者共用同一份额度，才补上「每类一个令牌桶」；而且当时说的是「各取前 10」，没有说清预留和借用。强的回答直接说三层。
**面试官可能接着问。**
- 为什么不是严格的优先级：回执先，活动用剩下的？ → 严格优先在回执到达率意外飙高时会饿死活动；预留加溢出保证了两边都有下限。
- 如果回执突然涨到 20,000 条/秒呢？ → 回执桶只有 10,000/秒，超出的回执在 tx 里排队，延迟上升，监控告警。这时要把回执的预留调大，调的代价是活动变慢。这是配置，不是改架构。
- 活动能暂停吗？ → 能：把活动桶设为 0，活动停在 bulk 里，保留进度；恢复后接着发。
- 邮件和短信也是这样分吗？ → 同样每个供应商一个桶，按类别预留。短信贵又慢，额度小得多，预留比例更要谨慎。
**常见失分。**
- **只拆主题，不拆额度：** 活动照样把共享的供应商额度吃光。
- **说「取前 10」：** 没有预留，也没有借用，说不出数字。
- **严格优先级：** 会饿死另一类。
- **没有监控：** 隔离失效时没有人知道。
