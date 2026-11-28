---
id: hi-fix-component-cost-04-ticketmaster-seat-hold
node: fix.component-cost
type: qa
step: 4
---
## Q
**Ticketmaster · 加组件：Redis 占座**｜补强

面试官：「用户选好座位到付完款，要好几分钟。这段时间怎么不让别人买走？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先说最简单的：** 「在数据库里给座位行上锁，直到付款完成。」
- **为什么不行：** 「付款要几分钟，行锁和连接一直被占着；用户走开了，锁也不放。」
- **职责：** 「我加 Redis 里的占座键：SET seat NX EX 600，占 10 分钟，不锁数据库行。」
- **新问题：** 「锁会过期：用户付款拖过 10 分钟，别人拿到了同一个座位，两个人都以为自己占着。」
- **处理：** 「Redis 只管体验上的占座，最终判定在数据库：付款后 UPDATE seats SET status = 'sold' WHERE id = s1 AND status = 'available'。影响 1 行才算买到；0 行就退款或让用户重选。」
- **TTL 的取值：** 「大于付款超时；进入付款后再续一次期。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 354">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">用户 A</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="262" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="298" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">用户 B</text>
<text x="48" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SET s1=A NX EX 600</text>
<polyline points="44,84 128,84" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,84 121.0,87.2 121.0,80.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">OK：占座 10 分钟</text>
<polyline points="128,118 44,118" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,118 51.0,114.8 51.0,121.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">A 付款拖到锁过期</text>
<text x="132" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SET s1=B NX EX 600</text>
<polyline points="298,180 128,180" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,180 135.0,176.8 135.0,183.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="294" y="202" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">付款后 UPDATE … WHERE 可售</text>
<polyline points="298,214 212,214" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,214 219.0,210.8 219.0,217.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="216" y="236" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1 行：B 买到</text>
<polyline points="212,248 298,248" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,248 291.0,251.2 291.0,244.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="270" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">付款后 UPDATE … WHERE 可售</text>
<polyline points="44,282 212,282" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,282 205.0,285.2 205.0,278.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="304" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0 行：已售</text>
<polyline points="212,316 44,316" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,316 51.0,312.8 51.0,319.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="342" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">A 被退款或重新选座；座位不会卖两次</text>
<line x1="44" y1="48" x2="44" y2="331" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="346" x2="44" y2="350" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="61" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="76" x2="128" y2="95" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="110" x2="128" y2="135" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="150" x2="128" y2="191" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="206" x2="128" y2="259" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="274" x2="128" y2="331" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="346" x2="128" y2="350" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="135" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="150" x2="212" y2="157" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="172" x2="212" y2="191" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="206" x2="212" y2="259" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="274" x2="212" y2="331" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="346" x2="212" y2="350" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="48" x2="298" y2="225" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="240" x2="298" y2="350" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="142" x2="111.68" y2="142" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="228.32" y1="142" x2="332" y2="142" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 112">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">我要写在组件旁边的四行</text>
<rect x="8" y="26" width="324" height="76" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">加：Redis 里的座位占用</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">为了：付款期间不锁数据库行</text>
<text x="18" y="75.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">新问题：锁会过期，A 还在付款</text>
<text x="18" y="90.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">处理：数据库条件更新才是最终判定</text>
</svg>
白板上：占座在 Redis，最终判定在数据库；A 的锁过期后，两条 UPDATE 只有一条影响 1 行。
**为什么这样说。** （约 1 分钟。）面试官看你把锁当成体验还是当成保证。强的回答明说锁会过期，并让数据库的条件更新做最终判定。弱的回答是「Redis 锁保证不会卖两次」。
**面试官可能接着问。**
- Redis 丢了锁呢？ → 占座只是体验层。丢了顶多两个人同时在付款，数据库的条件更新保证只有一个买到，另一个被退款。代价是体验，不是超卖。
- 要不要用分布式锁算法（Redlock）？ → 这里不需要强互斥，因为最终判定在数据库；单个实例的 SET NX EX 就够。
- 怎么减少被退款的人？ → 付款前再确认一次占座仍然有效，付款过程中续期，并在页面上倒计时。
**常见失分。**
- **把 Redis 锁当最终保证：** 过期、主从切换都会让它失效。
- **TTL 没有依据：** 为什么是 10 分钟，没有解释。
- **不说过期之后怎么办：** 面试官追问时才想起来。
