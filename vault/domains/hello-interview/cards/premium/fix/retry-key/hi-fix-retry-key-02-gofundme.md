---
id: hi-fix-retry-key-02-gofundme
node: fix.retry-key
type: qa
step: 2
---
## Q
**GoFundMe 捐款 · 重试键**｜补强

面试官：「捐款人点了 Donate，请求发出去了，可手机进了电梯，响应没回来。他回到有信号时页面自动重试，他自己也可能再点一次。你的系统怎么保证他只被扣一次？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **键写进请求：** 重试靠 `checkout_attempt_id`：捐款人一打开结账页，浏览器就生成这个 UUID，第一次 `POST /donations {campaign_id, amount, checkout_attempt_id, payment_token}` 就带上，之后每次重发都是同一个。卡号不进我们的系统，只收 PSP 前端换来的 token。
- **先写库再扣款：** 先 `INSERT` 一行 PENDING，`UNIQUE (user_id, checkout_attempt_id)` + `ON CONFLICT DO NOTHING`，提交后才调 PSP，行锁不会被拖过 PSP 的 0.5 秒。
- **同键重来：** INSERT 冲突就读已有那行：SUCCESS/FAILED 原样返回，PENDING 返回 PENDING 让前端轮询，不再调 PSP。
- **PSP 一侧：** `donation_id` 同时当订单号和幂等键，由 attempt 唯一决定；换卡或换 PSP 才是新尝试、换新键。
- **刻意再捐：** 重新打开结账，生成新 attempt id，就是新的一笔；不用「这个用户有没有 pending」判重，它分不清重试和第二笔。
- **同键不同内容：** 金额变了是客户端 bug，返回 409，不扣款。
- **崩在 PENDING 提交后、调 PSP 前：** 结算任务扫 PENDING，用 `donation_id` 去 PSP 查；查不到就用同一个幂等键再调，仍然安全。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 302">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">donations 表</text>
<rect x="8" y="26" width="324" height="78" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="54" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">id · user_id · campaign_id · amount</text>
<text x="18" y="69" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">status · checkout_attempt_id · created_at</text>
<text x="18" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">UNIQUE (user_id, checkout_attempt_id)</text>
<text x="8" y="128" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">三种来请求的方式，三种结果</text>
<rect x="8" y="138" width="324" height="46" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="157.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">同一个 K 再来（重试）</text>
<text x="18" y="172.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">返回已有的 d1，不碰 PSP</text>
<rect x="8" y="192" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="211.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">新的 K（重新打开结账）</text>
<text x="18" y="226.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新建 d2：一笔新的捐款</text>
<rect x="8" y="246" width="324" height="46" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="265.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">同一个 K，金额变了</text>
<text x="18" y="280.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">409，不进入扣款</text>
</svg>
白板上：donations 表带一个唯一约束；同一个 K 回到同一笔，新的 K 才是新的一笔。

**常见失分。**
- **只说服务端幂等：** 没说出重试时客户端发什么值。
- **id 在响应里才出现：** `donation.id` 由服务端返回，响应一丢客户端没东西可重发。
- **「查任意 pending」判重：** 混淆重试和刻意的第二笔。
- **事务包住 PSP 调用：** 未提交的行挡住所有重试，尖峰时连接池耗尽。

**面试官可能接着问。**
- 页面刷新后 UUID 去哪了？ → 存 `sessionStorage`，刷新读回同一个；换设备丢了就是新意图，会出两笔，只能靠结算任务和「你几分钟前捐过同一活动」提示兜底，是残余风险。
- 唯一约束要带 `user_id` 吗？ → 带，免得别人用你的键读到你的捐款；匿名时退回 `UNIQUE (checkout_attempt_id)`，UUID v4 不可猜。
- PSP 幂等键保存多久？ → 常见 PSP 只保留一段时间（看所用 PSP 文档），PENDING 要在窗口内被结算任务查清；我们的 `donations` 行永久保留键。
- 为什么不用 (用户, 活动, 金额) 当键？ → 同一人同一天给同一活动捐两次 25 美元是合法的。
