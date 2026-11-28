---
id: hi-mock-gofundme-05-api
node: fix.gofundme-mock
type: qa
step: 5
---
## Q
**GoFundMe · 第 5 步 · API**｜模拟面试

面试官：「好，接口怎么设计？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **三个接口：** 「对应三条功能：看活动页、捐款、看结果。创建活动的接口我不列，已经在线外。」
- **先写捐款请求：** 「POST /donations，请求体四个字段：campaign_id、amount、checkout_attempt_id、payment_token。返回 {donation_id, status}。」
- **键在请求里：** 「checkout_attempt_id 是客户端在打开结算页、第一次扣款之前生成的 UUID。同一次点击的每次重发都带同一个，新的一笔捐款换新的。」
- **为什么重发安全：** 「数据库对 checkout_attempt_id 有唯一约束。同一个键再来，服务端返回已有的那笔捐款，不再调 PSP。第一次的响应丢了也没关系，客户端手里有这个键，可以原样重发。」
- **内容不同：** 「同一个键但金额或活动变了，返回 409，不扣款。」
- **没有卡号：** 「请求里没有 card_details。卡号只在 PSP 的前端组件里，换成 payment_token 才到我们这里。」
- **用户身份：** 「user_id 取自登录态，不由客户端传。」
- **返回 Pending 是正常的：** 「status 可能是 Pending，意思是行已提交、结果还没出来，前端显示『处理中，请勿重复付款』。」
- **另外两个：** 「GET /donations/{id} 返回状态，前端每 2 秒轮询；GET /campaigns/{id} 返回已募金额、最近 100 笔、最大 10 笔，可以缓存几秒。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 388">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">API（三个，没有创建活动的接口）</text>
<rect x="8" y="26" width="324" height="78" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="54" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">GET /campaigns/{id}</text>
<text x="18" y="69" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">无 body，可缓存几秒</text>
<text x="18" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">返回 已募金额 · 最近 100 笔 · 最大 10 笔</text>
<rect x="8" y="112" width="324" height="92" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="139.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">POST /donations</text>
<text x="18" y="154.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">body：campaign_id · amount</text>
<text x="18" y="169.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">checkout_attempt_id · payment_token</text>
<text x="18" y="184.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">→ {donation_id, status}</text>
<rect x="8" y="212" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="239.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">GET /donations/{id}</text>
<text x="18" y="254.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">返回 {status}；前端每 2 秒轮询</text>
<rect x="8" y="284" width="324" height="92" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="18" y="311.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">同一个 checkout_attempt_id = 同一笔捐款</text>
<text x="18" y="326.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">同 id 但内容不同 → 409</text>
<text x="18" y="341.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">新的一次捐款 = 新的 id</text>
<text x="18" y="356.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">卡号字段不存在；用户身份取自登录态</text>
</svg>
白板上新增：三张便签对应三个接口，和一块写着接口契约的虚线框。
**为什么这样说。** （约 4 分钟，累计第 16 分钟。）面试官看接口有没有把重试身份和令牌边界落到字面上：请求体里是 checkout_attempt_id 和 payment_token，没有 card_details；而且你是先写出键，再解释为什么重发安全。弱的回答是 POST 只返回 donation.id，或者说「服务端检查有没有 Pending 的捐款」，这样第一次响应一丢，客户端就没有可重发的东西，也分不清重试和故意再捐一笔。
**面试官可能接着问。**
- 为什么不用『这个用户在这个活动有没有 Pending』来判断重复？ → 它分不清两种情况：重试应该得到同一笔，故意再捐一笔应该得到新的一笔。键对应的是一次点击，所以能区分。
- 同一个人想再捐一次怎么办？ → 再打开一次结算页，客户端生成新的 checkout_attempt_id，所以是新的一笔。
- 同一个键对应的捐款已经 Failed，用户想换一张卡重试呢？ → 同一个键永远返回那个 Failed 结果。换卡是新的一次结算，新的键。
- 用户关了标签页再回来呢？ → 客户端在结算页打开时把键存在本地，直到拿到终态；回来后用同一个键重发或直接查状态。
**常见失分。**
- **POST 只返回服务端 id：** 第一次响应丢了，客户端没有可重发的键，重试对不上同一笔。
- **请求里带卡号：** 说明没有理解令牌化，面试官给出边界之后还留着，是最明显的失分。
- **为创建活动设计接口：** 范围已经划掉，再花时间就是没有记住约束。
- **『检查 Pending』代替键：** 分不清重试和再捐一笔。
