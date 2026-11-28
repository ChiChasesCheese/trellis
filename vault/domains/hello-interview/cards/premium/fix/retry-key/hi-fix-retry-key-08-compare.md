---
id: hi-fix-retry-key-08-compare
node: fix.retry-key
type: qa
step: 9
---
## Q
**重试键｜补强 · 跨题对照**

同一个模式放进六道题：每道题的键是什么、在哪一刻、由谁生成，谁来裁决重复，重试得到什么？

## A
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 434">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一个模式，六道题里的键</text>
<rect x="8" y="26" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="46" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">GoFundMe 捐款</text>
<text x="18" y="61" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">checkout_attempt_id：结账页打开时浏览器生成</text>
<text x="18" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">UNIQUE (user_id, 键)：重试得到已有捐款</text>
<rect x="8" y="94" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="114" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Ticketmaster 占座</text>
<text x="18" y="129" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">hold_attempt_id：点座位时浏览器生成</text>
<text x="18" y="144" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SET NX 的值：重试认出自己，TTL 不动</text>
<rect x="8" y="162" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="182" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Uber 叫车 / 接单</text>
<text x="18" y="197" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">fare_id（服务端估价时发）· (ride, 司机)</text>
<text x="18" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">UNIQUE / 条件更新：读到赢家是自己</text>
<rect x="8" y="230" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="250" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">支付 API</text>
<text x="18" y="265" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Idempotency-Key：商户先存进订单行</text>
<text x="18" y="280" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">UNIQUE (商户, 键) + 请求哈希</text>
<rect x="8" y="298" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="318" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Robinhood 下单</text>
<text x="18" y="333" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">client_order_id：Review 页生成</text>
<text x="18" y="348" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">UNIQUE (用户, 键)；交易所有 clientOrderId</text>
<rect x="8" y="366" width="324" height="62" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="386" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">广告点击</text>
<text x="18" y="401" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">impression_id：展示时服务端签名发出</text>
<text x="18" y="416" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SET NX：第二次丢弃</text>
</svg>
白板上：六道题的键，一行一题。

**同一套三问。** 遇到任何会重发的写请求，先答这三个问题：
- **键是什么：** 说出请求里的那个字段，而不是「幂等」两个字。
- **什么时候生成：** 必须在第一次发送之前：打开结账页、点座位、进入 Review 页、广告渲染、估价。
- **谁裁决重复：** 数据库的唯一约束（捐款、订单、支付）、Redis 的 `SET NX`（占座、点击）、条件更新加一次读（接单）。

**重试得到什么。** 不是一个错误：是第一次的结果。捐款返回同一笔，占座返回同一个 booking，接单返回同一个成功，支付返回存好的结果，广告点击被安静地丢弃。

**什么时候要新键。** 用户刻意再来一次：再捐一笔、再买一单、再叫一辆车。判断标准：「这是同一次意图的重发，还是新的意图」。

**一句话版本。** 「重试靠一个键，它在第一次发送之前生成，每次重发都带上；服务端对它有唯一约束，重试拿到第一次的结果；每道外部边界各有一个稳定的键。」
