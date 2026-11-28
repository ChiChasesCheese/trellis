---
id: hi-fix-apply-once-07-ticketmaster
node: fix.apply-once
type: qa
step: 7
---
## Q
**Ticketmaster 支付确认 · 只应用一次**｜补强

面试官：「支付服务的回调会重发，而且可能在座位保留过期之后才到。支付成功的事件怎么只确认一次，晚到的怎么办？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **回调里带 booking id：** 「创建支付时我把 `booking_id` 放进 metadata；回调回来，我靠它找到预订。」
- **状态迁移就是已应用记录：** 「确认是一次迁移：`UPDATE bookings SET status = 'CONFIRMED' WHERE id = :b AND status = 'PENDING'`。影响 1 行，我是赢家；影响 0 行，说明已经处理过。」
- **赢家继续做事：** 「同一个事务里 `UPDATE tickets SET status = 'SOLD' WHERE id = :t AND status = 'AVAILABLE'`，然后提交，再发邮件和电子票。输家直接返回 200，什么也不做。」
- **为什么不只记事件 id：** 「事件 id 只挡同一条消息的重发。状态迁移还挡住不同事件对同一个预订的重复通知，而且发邮件这类副作用只由赢得迁移的一次触发。」
- **晚到的支付：** 「锁过期、座位被别人买走之后，付款才到。座位的条件更新影响 0 行：我回滚确认，把预订记为 REFUND_NEEDED，调退款，退款的幂等键用 `refund:{booking_id}`。」
- **回调失败了怎么办：** 「返回非 2xx，支付服务会重试；因为处理是幂等的，重试无害。」
- **漏掉回调怎么办：** 「定期扫长时间 PENDING 的预订，用 booking_id 去支付服务查结果，走同一个迁移。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 356">
<rect x="18" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="54" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Stripe</text>
<rect x="134" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">webhook</text>
<rect x="250" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="286" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<text x="58" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">支付成功 {booking B}</text>
<polyline points="54,84 170,84" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="170,84 163.0,87.2 163.0,80.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="282" y="106" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">UPDATE bookings → CONFIRMED</text>
<polyline points="170,118 286,118" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="286,118 279.0,121.2 279.0,114.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="191.68" y="132" width="144.32" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="263.84" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">WHERE PENDING：1 行</text>
<text x="58" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">200</text>
<polyline points="170,180 54,180" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="54,180 61.0,176.8 61.0,183.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="208" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Stripe 重发同一个事件</text>
<text x="58" y="230" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">支付成功 {booking B}</text>
<polyline points="54,242 170,242" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="170,242 163.0,245.2 163.0,238.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="174" y="264" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">UPDATE（同一个条件）</text>
<polyline points="170,276 286,276" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="286,276 279.0,279.2 279.0,272.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="239.64" y="290" width="92.72" height="20" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="286" y="304" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0 行：已处理</text>
<text x="58" y="326" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">200，什么也不做</text>
<polyline points="170,338 54,338" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="54,338 61.0,334.8 61.0,341.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="54" y1="48" x2="54" y2="352" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="48" x2="170" y2="61" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="76" x2="170" y2="95" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="110" x2="170" y2="197" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="212" x2="170" y2="219" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="234" x2="170" y2="352" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="48" x2="286" y2="130" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="154" x2="286" y2="253" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="268" x2="286" y2="288" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="286" y1="312" x2="286" y2="352" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="204" x2="94.28" y2="204" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="245.72" y1="204" x2="332" y2="204" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上：第一次回调赢得 PENDING 到 CONFIRMED 的迁移，重发的回调得到 0 行。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 254">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">确认是一次状态迁移</text>
<rect x="8" y="26" width="100" height="36" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="58" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PENDING</text>
<rect x="232" y="26" width="100" height="36" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="282" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CONFIRMED</text>
<rect x="100" y="96" width="150" height="36" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="175" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">REFUND_NEEDED</text>
<polyline points="108,44 232,44" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="232,44 225.0,47.2 225.0,40.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="118" y="38" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">WHERE PENDING</text>
<polyline points="58,62 58,114 100,114" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="100,114 93.0,117.2 93.0,110.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="160" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">座位 UPDATE tickets WHERE AVAILABLE</text>
<text x="8" y="178" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">影响 0 行（锁过期，被别人买走）：</text>
<text x="8" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">回滚确认，走 REFUND_NEEDED，</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">退款幂等键 = refund:B</text>
<text x="8" y="242" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">邮件、电子票只由赢得迁移的那次发出</text>
</svg>
白板上：确认是一次状态迁移，晚到的支付走退款。

**为什么这样说。** 面试官在检查：回调重发时，你的处理是不是有副作用，以及晚到事件怎么处理。弱的回答是「webhook 要幂等」，没有说具体怎么判断；强的回答把判决放在条件更新的影响行数上，并把邮件等副作用只挂在赢家身上。
**面试官可能接着问。**
- 回调和支付失败的回调乱序到达？ → 迁移都带起始状态条件：PENDING 才能变 CONFIRMED 或 FAILED，终态不可再改。
- 邮件发送失败怎么办？ → 邮件由赢家通过 outbox 发出，发不出去由重试补；邮件服务自己再按 booking_id 去重。
- 同时有两个实例收到同一条回调？ → 数据库行锁让它们串行，一个得到 1 行，另一个得到 0 行。
- 为什么要二次确认金额？ → 回调里的金额和预订的金额不一致就不确认，走人工处理。
**常见失分。**
- **先查状态再更新：** 两个并发回调都查到 PENDING，都确认。
- **只存事件 id 去重：** 不同事件对同一预订的重复通知挡不住。
- **重复回调返回错误：** 支付服务继续重试，没有尽头。
- **晚到的支付硬确认：** 同一个座位卖给两个人。
