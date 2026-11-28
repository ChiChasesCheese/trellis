---
id: hi-mock-gofundme-08-dive-retry-settlement
node: fix.gofundme-mock
type: qa
step: 8
---
## Q
**GoFundMe · 第 8 步 · 深入一：响应丢了，捐款人重试**｜模拟面试

面试官：「捐款人点了捐款，服务端扣款成功了，但响应在路上丢了，浏览器超时。你的系统现在怎么办？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **重试请求：** 浏览器原样重发 POST /donations（campaign_id、amount、checkout_attempt_id = K1、payment_token），键就是 K1。第一次响应丢了，客户端不知道 D1，所以键必须是第一次扣款前由客户端生成的 K1。
- **为什么安全：** 服务端 `INSERT … ON CONFLICT (checkout_attempt_id) DO NOTHING`；没插进去说明已有一行，读出返回 {D1, Success}，不调 PSP；只有插入成功的那个请求才调 PSP。同一个 K1 两个请求并发，唯一约束只放一个进去。
- **重试 vs 再捐一笔：** 同一次点击重发带同一个 K1；故意再捐要重新打开结算页，生成 K2，是新的一行。「检查有没有 Pending」分不出这两种。
- **PSP 没回答：** 行留 Pending 返回 Pending；重发同一个 K1 也只读到 Pending，不再扣。
- **对账任务：** 收尾长时间 Pending 的行；新问题是和在线请求可能同时改同一行、不能凭空再扣。只做两件事：按 ref = D1 向 PSP 查询，再 `UPDATE … WHERE status='Pending'`。每分钟扫超过 2 分钟的 Pending：PSP 说已扣改 Success；说失败改 Failed；查无此笔且超过宽限期，先在 PSP 取消 D1 再记 Failed，迟到的扣款就进不来。
- **回调：** 若 PSP 有回调只当加速，走同一个条件更新；它可能丢，对账兜底。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 360">
<rect x="12" y="8" width="140" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="82" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">浏览器 · App</text>
<text x="82" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">checkout_attempt_id</text>
<rect x="188" y="8" width="140" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="258" y="26.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">PSP 前端组件</text>
<text x="258" y="41.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">收卡号 · 换令牌</text>
<polyline points="152,22 188,22" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="188,22 181.0,25.2 181.0,18.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polyline points="188,40 152,40" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="152,40 159.0,36.8 159.0,43.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="17" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">卡号</text>
<text x="170" y="55" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">令牌</text>
<polyline points="140,52 140,150" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="140,150 136.8,143.0 143.2,143.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="140,52 143.2,59.0 136.8,59.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="148" y="82" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">POST /donations</text>
<text x="148" y="98" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">GET /donations/{id}</text>
<text x="148" y="114" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">GET /campaigns/{id}</text>
<rect x="12" y="150" width="316" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="168.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关 + 应用服务</text>
<text x="170" y="183.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">无状态 · 多实例 · 三类服务合一</text>
<path d="M8,242 a89,6 0 0 1 178,0 v76 a89,6 0 0 1 -178,0 z" stroke-width="1.2" fill="none" stroke="currentColor"/>
<path d="M8,242 a89,6 0 0 0 178,0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<text x="97" y="260" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库 Postgres</text>
<rect x="16" y="274" width="162" height="22" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="97" y="289" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">donations</text>
<rect x="16" y="300" width="162" height="22" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="97" y="315" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">campaigns</text>
<polyline points="96,194 96,236" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="96,236 92.8,229.0 99.2,229.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="96,194 99.2,201.0 92.8,201.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="102" y="216" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">INSERT / UPDATE</text>
<rect x="196" y="236" width="132" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="262" y="254.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">支付服务商 PSP</text>
<text x="262" y="269.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ref = donation_id</text>
<polyline points="262,194 262,236" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="262,236 258.8,229.0 265.2,229.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="268" y="220" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">charge</text>
<rect x="204" y="300" width="124" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="266" y="318.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">对账任务</text>
<text x="266" y="333.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每分钟扫 Pending</text>
<polyline points="262,300 262,280" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="262,280 265.2,287.0 258.8,287.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="268" y="294" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">查</text>
<polyline points="204,330 186,330" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="186,330 193.0,326.8 193.0,333.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polygon points="204,330 197.0,333.2 197.0,326.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
</svg>
白板上新增：对账任务（右下），它向 PSP 查询并回写数据库；前两张时序图是重发和对账。

**常见失分。**
- **说不出重发的值：** 「server 和 PSP 都幂等」没指出客户端重发的是哪个值。
- **键由服务端创建后返回：** 响应一丢客户端没有键，只能发新请求，可能扣第二次。
- **检查 Pending 代替键：** 要么重复扣款，要么拒绝合法的第二笔。
- **对账靠重扣：** 重扣是新的副作用，应先查询。

**面试官可能接着问。**
- 对账为什么查询而不是重发 charge？ → 查询无副作用，直接回答「扣没扣」；重发要保存一次性、可能过期的令牌，而且只让 PSP 去重，不说明第一次发生了什么。
- 对账和在线请求同时改同一行？ → 都用 `WHERE status='Pending'`，一个赢，另一个影响 0 行放弃。
- 同一个 K1 内容变了？ → 409，不扣款；键标识的是一次请求。
