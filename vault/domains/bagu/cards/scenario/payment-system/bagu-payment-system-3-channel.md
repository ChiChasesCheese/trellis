---
id: bagu-payment-system-3-channel
node: a.scenario.payment-system
type: qa
step: 3
---
## Q
**渠道对接 · 请求号、验签、重复回调、超时查询**｜必会

面试官：「调第三方渠道下单，请求超时了，或者渠道把同一笔回调了三次，你怎么处理？」

## A
**基本回答。** 四个固定动作。下单带我方生成的商户请求号（一次支付尝试一个），超时重试原样复用，渠道见过只返回第一次的结果。超时有三种可能：没到渠道、渠道还在处理、渠道已成功但响应丢了，分不清，所以不算失败也不换单重发：支付单留在 `PROCESSING`，按退避间隔（5 秒、30 秒、5 分钟）查询，超过窗口仍未知交给日终对账；切换渠道前必须先终结旧尝试，否则两个渠道都可能扣款。收到回调先验签（回调地址公开，任何人都能 POST「支付成功」），签名只证明出自渠道，金额、币种、订单号还要与我方记录一致才入账，可再限制来源 IP。渠道没收到成功应答会重发多次，靠渠道交易号唯一索引加状态机条件更新挡住，处理过的返回成功（按渠道格式，如支付宝回 success，意思是「别再发了」），验签失败或金额不一致才返回失败；必须落库成功后再应答，否则应答后进程崩了这笔回调就丢了。查询和回调同时到，走同一个条件更新，谁先到谁生效。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<rect x="10" y="4" width="100" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="60.0" y="21.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">我方</text>
<rect x="230" y="4" width="100" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="280.0" y="21.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">渠道</text>
<line x1="60" y1="30" x2="60" y2="226" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<line x1="280" y1="30" x2="280" y2="226" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<text x="170" y="56" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 下单，请求号 R1</text>
<line x1="60" y1="62" x2="274.0" y2="62.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="280.0,62.0 274.0,65.0 274.0,59.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="94" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">② 已扣款，但响应丢了</text>
<line x1="280" y1="100" x2="66.0" y2="100.0" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="60.0,100.0 66.0,97.0 66.0,103.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">等到超时：结果未知，不当失败</text>
<text x="170" y="158" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">③ 同一个请求号 R1 查询</text>
<line x1="60" y1="164" x2="274.0" y2="164.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="280.0,164.0 274.0,167.0 274.0,161.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="198" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">④ 查到成功 → 入账</text>
<line x1="280" y1="204" x2="66.0" y2="204.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="60.0,204.0 66.0,201.0 66.0,207.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
</svg>
超时时我方只知道没收到响应；用同一个请求号去查，才知道渠道其实已经成功。
**举个例子。** 订单 A 付 100 元：生成 R1 调渠道，`INIT` 变 `PROCESSING`；5 秒无响应，不改失败；用 R1 查到「已成功，交易号 T9」，条件更新改 `SUCCESS` 影响 1 行，订单 `PAID`。随后迟到的回调来三次，验签通过、金额一致，但状态已是 `SUCCESS`，更新 0 行，返回成功，渠道不再重发。有人伪造 POST「订单 A 已支付」，签名不对直接拒绝。
**容易错。**
- **超时就换新请求号重发：** 渠道可能已扣款，会扣第二次。
- **重复回调返回失败：** 渠道会一直重发。
