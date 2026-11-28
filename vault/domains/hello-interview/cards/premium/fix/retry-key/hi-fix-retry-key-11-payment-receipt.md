---
id: hi-fix-retry-key-11-payment-receipt
node: fix.retry-key
type: qa
step: 11
---
## Q
**通知系统 · 支付回执的键是支付单号**｜补强

面试官：「用户付款成功，支付服务要发一张回执。支付服务可能超时重试，PSP 的成功 webhook 也可能送到两次。这张回执的 notification_id 用什么？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先给键：** 「notification_id = `receipt:` 加支付单号，例如 `receipt:P-90017`。同一个事实（P-90017 付款成功）永远算出同一个键。」
- **为什么不是随机 UUID：** 「随机 UUID 在每次调用时现生成。支付服务一重试就换了新的，唯一约束看到的是两个不同的键，发两张。键要来自业务对象，不是来自这一次调用。」
- **谁来生成：** 「支付服务，在调用之前，用自己库里已经有的 payment_order_id 算出来。超时重试、进程重启后重新算，结果相同。PSP 的 webhook 重复触发，也是同一个键。」
- **数字例子：** 「10:00:00 第一次调用，2 秒超时；10:00:03 重试同一个键；10:00:04 webhook 重复，第三次调用同一个键。三次调用，数据库里 1 行，用户收到 1 张回执。」
- **一个订单不止一张通知：** 「退款通知用 `refund:P-90017:R-3`，带退款自己的 id。同一个支付单的回执和退款是两个键。」
- **渠道：** 「邮件和推送各发一张是对的，所以唯一约束是 (notification_id, channel)。同一渠道重复才挡。」
- **保留多久：** 「键在热库里留 7 天，调用方的重试窗口不到 24 小时，所以窗口内的重放都挡得住。第 8 天分区被丢掉以后再来的重放会被当成新的，所以重试窗口要在需求里写明。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 328">
<rect x="10" y="8" width="84" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="52" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">支付服务</text>
<rect x="128" y="8" width="84" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">通知服务</text>
<rect x="246" y="8" width="84" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="288" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">通知表</text>
<text x="56" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">POST receipt:P-90017</text>
<polyline points="52,84 170,84" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="170,84 163.0,87.2 163.0,80.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="174" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT → 1 行</text>
<polyline points="170,118 288,118" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="288,118 281.0,121.2 281.0,114.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10:00:03 超时，重试</text>
<text x="56" y="168" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">POST receipt:P-90017</text>
<polyline points="52,180 170,180" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="170,180 163.0,183.2 163.0,176.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="174" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT → 0 行</text>
<polyline points="170,214 288,214" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="288,214 281.0,217.2 281.0,210.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="242" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10:00:04 webhook 重复</text>
<text x="56" y="264" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">POST receipt:P-90017</text>
<polyline points="52,276 170,276" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="170,276 163.0,279.2 163.0,272.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="174" y="298" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT → 0 行</text>
<polyline points="170,310 288,310" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="288,310 281.0,313.2 281.0,306.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="52" y1="48" x2="52" y2="324" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="48" x2="170" y2="61" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="76" x2="170" y2="135" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="150" x2="170" y2="157" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="172" x2="170" y2="231" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="246" x2="170" y2="253" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="268" x2="170" y2="324" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="288" y1="48" x2="288" y2="324" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="142" x2="100.28" y2="142" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="239.72" y1="142" x2="332" y2="142" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="238" x2="91.88" y2="238" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="248.12" y1="238" x2="332" y2="238" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 203">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">键来自业务对象，不是这一次调用</text>
<rect x="8" y="26" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="45.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">回执</text>
<text x="18" y="60.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">receipt:P-90017</text>
<rect x="8" y="80" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="99.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">退款通知（同一个支付单可以有多张）</text>
<text x="18" y="114.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">refund:P-90017:R-3</text>
<rect x="8" y="134" width="324" height="61" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="153.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">一个键，多个渠道</text>
<text x="18" y="168.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">UNIQUE (notification_id, channel)</text>
<text x="18" y="183.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">邮件一张、推送一张，重复才挡</text>
</svg>
白板上：支付服务三次调用、同一个键，数据库里只有一行；再画键的三种形状。
**为什么这样说。** （约 2 分钟。）面试官看的是键从哪里来：强的回答说键由支付单号这个业务对象决定，调用方重试时能重新算出来；弱的回答说『加个幂等键』，不说值是什么、谁生成。
**面试官可能接着问。**
- 为什么不让通知服务生成这个键？ → 通知服务收到请求才生成，响应丢了，调用方手里没有可重发的值（见重试键的机制）。键必须在调用之前就存在，并且调用方重试时能重算出同一个值。
- 营销推送没有支付单号怎么办？ → 键 = campaign_id + user_id，同一个人同一个活动只有一条；不要用时间戳。
- 同一个用户付了两次钱呢？ → 两个不同的支付单号，两个键，两张回执，都是对的。
- 为什么键里要有 `receipt:` 这样的类型？ → 同一个支付单号还会有退款通知、失败通知；类型放进键，它们才不会互相当成重复。
- PSP 的 webhook 重复送来，要不要通知服务自己去重？ → 支付服务先按 PSP 的事件 id 去重，通知服务再按 notification_id 去重，各管一道边界。
**常见失分。**
- **键用随机 UUID：** 重试一次就换一个键，唯一约束形同虚设。
- **键只用支付单号、不带类型：** 回执、退款、失败通知会互相覆盖。
- **键不带渠道：** 邮件发出去之后，推送被当成重复挡掉。
- **由通知服务造键：** 响应一丢，调用方就没有可重发的值。
- **保留期比调用方的重试窗口短：** 窗口之外的重放会再发一张。
