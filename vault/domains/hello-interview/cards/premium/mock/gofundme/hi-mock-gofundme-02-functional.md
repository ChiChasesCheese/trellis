---
id: hi-mock-gofundme-02-functional
node: fix.gofundme-mock
type: qa
step: 2
---
## Q
**GoFundMe · 第 2 步 · 功能需求**｜模拟面试

面试官：「好。那你先说说功能需求，准备做哪几条？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先给三条：** 「线内我做三件事。」
- **第一条，看活动页：** 「打开一个活动，看到已募金额、最近 100 笔捐款、金额最大的 10 笔。」
- **第二条，捐款：** 「登录的捐款人输入金额，付款组件给出支付令牌，服务端用令牌向 PSP 扣款。卡号永远不到我们这里。」
- **第三条，看支付结果：** 「捐款人要看到三种结果之一：成功、失败，或者处理中（Pending）。结果还没出来时，必须明确告诉他『处理中』，而不是让他再点一次。」
- **线外，说一次：** 「创建和编辑活动、向组织者放款、退款、评论、审核后台，您已经划掉了。我就把它们当作『活动已经存在』，后面不再提，也不列接口。」
- **点出难点：** 「这三条看着简单，难在三处：捐款一旦重试就可能扣两次；已募金额只能算成功的捐款，而且每笔只能算一次；爆红活动的活动页读很多。后面的需求和深入都围绕这三处。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 362">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">功能需求（线内 3 条）</text>
<rect x="8" y="26" width="324" height="50" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="47.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">1  看活动页</text>
<text x="18" y="62.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已募金额 · 最近 100 笔捐款 · 最大 10 笔</text>
<rect x="8" y="86" width="324" height="50" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="107.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">2  捐款</text>
<text x="18" y="122.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">金额 + 支付令牌；卡号只到支付服务商</text>
<rect x="8" y="146" width="324" height="50" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="167.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">3  看支付结果</text>
<text x="18" y="182.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">成功 / 失败 / 处理中（Pending）</text>
<line x1="8" y1="212" x2="332" y2="212" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">线外（面试官已划掉，不再回头）</text>
<rect x="8" y="252" width="324" height="28" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="18" y="270" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">创建 / 编辑活动</text>
<rect x="8" y="288" width="324" height="28" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="18" y="306" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">向组织者放款 · 退款 · 评论</text>
<rect x="8" y="324" width="324" height="28" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="18" y="342" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">审核与风控后台</text>
</svg>
白板上新增：三张便签（线内三条）和一块虚线框（线外）。
**为什么这样说。** （约 2 分钟，累计第 5 分钟。）面试官看你能不能把需求收到三条，并且把被划掉的范围真正放下。强的回答顺带点出难点在哪里，让面试官知道你已经看到了重点。弱的回答是在划掉之后仍然回头去讲创建活动的接口，或者列一长串登录、分享、评论。
**面试官可能接着问。**
- 三条里为什么把『处理中』单独写出来？ → 因为 PSP 会超时，我们可能没拿到结果。如果只有成功和失败，超时那一刻系统只能二选一，选错就是重复扣款或者丢一笔捐款。
- 为什么不做放款？ → 您划掉了。如果要做，它是另一个有状态的资金流：账本、持有期、幂等键、对账，我会另开一轮讲。
- 已募金额算不算 Pending 的捐款？ → 不算。Pending 之后可能失败，算进去总额会偏大。只有 Success 才算。
**常见失分。**
- **回头讲创建：** 面试官划掉之后还花时间在创建活动的接口上，会被记成没把范围钉住。
- **漏掉『处理中』：** 只写成功和失败，后面的 Pending 和对账就没有来由。
- **列太多：** 登录、评论、分享一起上，等于没有取舍。
