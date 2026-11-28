---
id: hi-fix-gofundme-07-apply-once
node: fix.gofundme
type: qa
step: 7
---
## Q
**GoFundMe · 第 37:03 分 · 总额只在成功时算、只算一次**｜复盘

面试官：「总额放在 Redis 里。如果工作进程崩了、事件被重放，同一笔捐款会被加几次？」

你会怎么回答？

## A
**当时的回答。**
- **增加的时机：** 你在捐款创建时就给 Redis 加了。
- **追问之后：** 你提到了 Redis 的原子自增、队列、事务和复制。
**差在哪。**
- **创建时就加：** 挂起的、后来被拒绝的捐款也进了「已筹金额」。
- **没有记「谁加过」：** 自增、队列、事务、复制都不记录哪一笔已经应用过；重放一次就多加一次。
**应该这样说。**
- **只有成功才发事件：** 「状态变成 Success 的同一个事务里写一条 outbox 行，发出 DonationCompleted(donation_id, campaign_id, amount)。」
- **应用要记账：** 「工作进程开一个事务，先往 campaign_total_applied 插入 donation_id，这一列是唯一键。」
- **插入成功才累加：** 「插入成功，才 total += amount；唯一冲突说明加过了，直接跳过。」
- **Redis 用 SET：** 「提交之后把 Redis SET 成持久化的值。崩在 SET 之前也没关系，下一次刷新还是同一个值，不会多加。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 388">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队列</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">工作进程</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="262" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="298" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<text x="48" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Completed(d42, 25)</text>
<polyline points="44,84 128,84" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,84 121.0,87.2 121.0,80.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">BEGIN; INSERT applied(d42)</text>
<polyline points="128,118 212,118" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,118 205.0,121.2 205.0,114.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">插入成功</text>
<polyline points="212,152 128,152" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,152 135.0,148.8 135.0,155.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="174" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">total += 25; COMMIT</text>
<polyline points="128,186 212,186" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,186 205.0,189.2 205.0,182.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="214" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">崩溃，没来得及确认 · 队列重发</text>
<text x="48" y="236" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Completed(d42, 25)</text>
<polyline points="44,248 128,248" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,248 121.0,251.2 121.0,244.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="270" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT applied(d42)</text>
<polyline points="128,282 212,282" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,282 205.0,285.2 205.0,278.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="304" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">唯一冲突：已应用</text>
<polyline points="212,316 128,316" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,316 135.0,312.8 135.0,319.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="342" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">跳过，total 不变</text>
<text x="132" y="358" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SET total = 持久化值</text>
<polyline points="128,370 298,370" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,370 291.0,373.2 291.0,366.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="44" y1="48" x2="44" y2="331" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="346" x2="44" y2="384" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="61" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="76" x2="128" y2="203" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="218" x2="128" y2="225" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="240" x2="128" y2="384" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="95" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="110" x2="212" y2="163" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="178" x2="212" y2="203" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="218" x2="212" y2="259" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="274" x2="212" y2="293" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="308" x2="212" y2="347" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="362" x2="212" y2="384" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="48" x2="298" y2="95" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="110" x2="298" y2="384" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="210" x2="69.32" y2="210" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="270.68" y1="210" x2="332" y2="210" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 229">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">两处修正</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">什么时候发事件</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">只有变成 Success 才发 Completed</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Pending、Failed 不进总额</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">谁记得「加过了」</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">applied(donation_id) 唯一键</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">和总额同一个事务；冲突就跳过</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Redis 怎么写</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">SET 成持久化值，不用 INCR</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">重放多少次，结果都一样</text>
</svg>
白板上：队列到工作进程到数据库的时序；重放那一轮在 applied 的唯一键上被挡住。
**面试官可能接着问。**
- 事件丢了怎么办？ → outbox 行和 Success 在同一个事务里写，投递器扫没发出去的行；至少一次投递，重复由 applied 表吸收。
- applied 表会不会无限长？ → 一笔捐款一行。按每行约 50 字节算，1 亿笔约 5 GB，一台库放得下；也可以按活动归档。
- 退款怎么办？ → 退款是另一个事件 DonationRefunded，同样先记 applied（主键加上事件类型），再减去金额。
**同类题。**
- **Ad Click Aggregator：** 重复点击不能重复计数。
- **YouTube Top K、Leaderboard：** 分数更新被重放。
- **Flash Sale：** 库存回写和订单事件。
