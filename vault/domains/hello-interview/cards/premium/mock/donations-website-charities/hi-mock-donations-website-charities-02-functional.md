---
id: hi-mock-donations-website-charities-02-functional
node: qb.sd.donations-website-charities.mock
type: qa
step: 2
---
## Q
**限时捐款网站 · 第 2 步 · 功能需求**｜模拟面试

面试官：「好。那你先说说功能需求，准备做哪几条？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先给三条：** 「线内我做三件事。」
- **第一条，看机构列表：** 「预先写死几家慈善机构，用户选一家，不需要登录。」
- **第二条，提交捐款：** 「用户填金额、选机构，给出付款令牌和邮箱，系统要么扣款成功，要么明确告诉他失败。结果还不知道时，也要告诉他『处理中』，而不是让他干等。」
- **第三条，发收据：** 「成功之后给邮箱发一封收据。邮件发不出去，不能影响已经成功的捐款。」
- **线外：** 「累计金额展示您说不需要；登录与账户、定期捐款、退款、税务票据 PDF、后台管理，我都先不做，想要随时挪进来。」
- **一句话点题：** 「业务很简单，难点全在和 PSP 打交道时的不确定性：点两次、超时、PSP 挂了、结果没拿到。后面的需求和深入都围绕这个。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 362">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">功能需求（线内 3 条）</text>
<rect x="8" y="26" width="324" height="50" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="47.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">1  看慈善机构列表</text>
<text x="18" y="62.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">预先写死几家，用户选一家（不用登录）</text>
<rect x="8" y="86" width="324" height="50" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="107.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">2  提交捐款</text>
<text x="18" y="122.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">金额 + 机构 + 付款令牌 + 邮箱；成功或明确失败</text>
<rect x="8" y="146" width="324" height="50" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="167.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">3  成功后发收据</text>
<text x="18" y="182.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">邮件；发不出去也不影响已成功的捐款</text>
<line x1="8" y1="212" x2="332" y2="212" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">线外（先不做，想要随时挪进来）</text>
<rect x="8" y="252" width="324" height="28" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="18" y="270" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">累计金额展示（面试官说不需要）</text>
<rect x="8" y="288" width="324" height="28" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="18" y="306" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">登录与账户 · 定期捐款 · 退款</text>
<rect x="8" y="324" width="324" height="28" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="18" y="342" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">税务票据 PDF · 后台管理</text>
</svg>
白板上新增：三张便签（线内三条）和一块虚线框（线外）。
**为什么这样说。** （约 2 分钟，累计第 4 分钟。）面试官看你能不能把需求收紧到三条，并且主动划出线外，而不是把能想到的功能全列上。强的回答顺便点出这题的难点在哪里，让面试官知道你已经看到了重点。弱的回答是列一长串：登录、积分、排行榜、分享，结果时间花光了，支付流程还没画。
**面试官可能接着问。**
- 为什么不做登录？ → 题目说不要求。没有登录意味着没有用户 id 可用来识别重复提交，所以后面我让浏览器在捐款页加载时生成一个 donationId。
- 面试官改主意要总额怎么办？ → 可以加。不要在一行上 UPDATE total = total + 10，5 家机构就是 5 个热点行；我会用分片计数器，或者消费捐款成功事件累加到 Redis。我放在最后再讲，因为它不影响支付正确性。
- 退款要不要做？ → 线外。要做的话，退款也是一笔有状态的资金操作：同样要幂等键、状态机和对账。
**常见失分。**
- **列太多：** 登录、积分、排行榜一起上，等于没有取舍。
- **漏掉「结果未知」：** 只写成功和失败，后面的 UNKNOWN 就没有来由。
- **不划线外：** 面试官不知道你是忘了还是故意不做。
