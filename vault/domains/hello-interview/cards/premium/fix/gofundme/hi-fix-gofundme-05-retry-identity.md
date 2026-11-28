---
id: hi-fix-gofundme-05-retry-identity
node: fix.gofundme
type: qa
step: 5
---
## Q
**GoFundMe · 第 33:22 分 · 重试身份**｜复盘

面试官：「PSP 扣款成功了，但回给你的响应在路上丢了，捐款人又点了一次。会发生什么？」

你会怎么回答？

## A
**当时的回答。**
- **两层幂等：** 你说服务端和 PSP 都有重复请求保护，之后还有结算任务。
- **怎么找回：** 服务端检查有没有挂起的捐款，再用 donation UUID，或者用户加活动的 ID 去匹配。
**差在哪。**
- **客户端没有可重发的值：** 第一次 POST 要等服务器建好行才返回 donation.id；响应丢了，客户端手里没有这个 id，重试没有东西可带。
- **「有没有挂起的」把两件事混了：** 同一次点击的重试应当返回同一笔；刻意再捐一次应当是新的一笔。凭用户、活动、金额去猜，两种情况都会判错。
- **只说「幂等」没说值：** 面试官听不到重发的到底是哪个字段。
**应该这样说。**
- **先写请求：** 「结账页一打开，浏览器就生成 checkout_attempt_id，放进 POST /donations，和 campaign_id、amount、payment_token 一起发。」
- **唯一约束：** 「donations 表在 (user_id, campaign_id, checkout_attempt_id) 上唯一。第一次请求创建 Pending 行并调 PSP，调用时带同一个 donation_id 做幂等键。」
- **重试原样返回：** 「同一个 key 再来，插入冲突，我读出已有的行原样返回，不再调 PSP。」
- **刻意再捐：** 「用户刻意再捐一次，是新的结账、新的 key、新的一笔。」
- **同 key 不同金额：** 「返回 409，不扣款。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 442">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">捐款服务</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="262" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="298" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PSP</text>
<text x="8" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">K1：结账页打开时，浏览器自己生成</text>
<text x="48" y="92" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">POST key=K1</text>
<polyline points="44,104 128,104" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,104 121.0,107.2 121.0,100.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="126" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT Pending(K1)</text>
<polyline points="128,138 212,138" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,138 205.0,141.2 205.0,134.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="160" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">charge(ref = id)</text>
<polyline points="128,172 298,172" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,172 291.0,175.2 291.0,168.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">成功</text>
<polyline points="298,206 128,206" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,206 135.0,202.8 135.0,209.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">UPDATE Success</text>
<polyline points="128,240 212,240" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,240 205.0,243.2 205.0,236.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="268" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">响应在路上丢了 · 浏览器超时</text>
<text x="48" y="290" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">POST key=K1（重试）</text>
<polyline points="44,302 128,302" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,302 121.0,305.2 121.0,298.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="324" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">INSERT … K1 → 唯一冲突</text>
<polyline points="128,336 212,336" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,336 205.0,339.2 205.0,332.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="358" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">已有行：Success</text>
<polyline points="212,370 128,370" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,370 135.0,366.8 135.0,373.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="392" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">返回同一笔 Success</text>
<polyline points="128,404 44,404" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,404 51.0,400.8 51.0,407.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="430" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">重试没有再碰 PSP</text>
<line x1="44" y1="48" x2="44" y2="65" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="80" x2="44" y2="419" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="434" x2="44" y2="438" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="65" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="80" x2="128" y2="257" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="272" x2="128" y2="279" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="294" x2="128" y2="381" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="396" x2="128" y2="438" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="65" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="80" x2="212" y2="115" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="130" x2="212" y2="149" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="164" x2="212" y2="217" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="232" x2="212" y2="257" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="272" x2="212" y2="313" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="328" x2="212" y2="347" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="362" x2="212" y2="438" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="48" x2="298" y2="438" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="264" x2="75.8" y2="264" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="264.2" y1="264" x2="332" y2="264" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 296">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">键由客户端造，放进请求；每次点击一个键</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">POST /donations</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">{campaign_id, amount,</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">checkout_attempt_id, payment_token}</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">同一次点击的所有重试</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">同一个 key → 返回同一笔捐款</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">唯一 (user_id, campaign_id, key)</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">刻意再捐一次</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">新 key → 新的一笔捐款</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不是重试，不能合并成一笔</text>
<rect x="8" y="227" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="245.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">同 key 但金额不同</text>
<text x="18" y="260.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">返回 409，不扣款</text>
<text x="18" y="275.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">说明客户端有 bug，别悄悄改单</text>
</svg>
白板上：请求里多了 checkout_attempt_id；时序里，丢了响应之后的重试在数据库那一步就被挡下。
**面试官可能接着问。**
- 刷新页面后 key 丢了怎么办？ → key 存在 sessionStorage，随这一次结账页保留；刷新同一个结账页继续用它，关掉重开才算新结账。
- key 要全局唯一吗？ → 用 UUID，碰撞可以忽略。唯一约束带上 user_id，是为了别人拿不到我的捐款。
- 有了我们的 key，还要 PSP 的幂等键吗？ → 要。我们的 key 防重复建行；PSP 的键防「调用超时后我们自己重发」。两把键各管一段。
**同类题。**
- **限时捐款网站：** 同一个键贯穿浏览器、数据库、PSP。
- **Payment System、钱包转账：** 转账请求的重试键。
- **Uber 叫车、Ticketmaster 订票：** 下单请求重复提交。
