---
id: hi-mock-donations-website-charities-05-api
node: qb.sd.donations-website-charities.mock
type: qa
step: 5
---
## Q
**限时捐款网站 · 第 5 步 · API**｜模拟面试

面试官：「好，接口怎么设计？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **三个接口：** 「对应三条功能。」
- **列表：** 「`GET /charities`，几乎静态，返回 charityId 和名称，可以缓存。」
- **提交：** 「`POST /donations`，body 是 donationId、charityId、金额（分）、币种、支付令牌、邮箱；返回 donationId 和 status。」
- **状态：** 「`GET /donations/:id`，返回当前 status，前端每 2 秒轮询，拿到终态就停。」
- **令牌从哪来：** 「浏览器先用 PSP 的前端组件（hosted fields）输入卡号，卡号只发给 PSP，PSP 回一个一次性令牌，浏览器再把令牌放进 POST 的 body。我们的服务器从没见过卡号。」
- **幂等是接口契约：** 「同一个 donationId 重复 POST，返回同一个结果，不重复扣款；同一个 id 但内容不同，返回 409。」
- **没有 webhook 端点：** 「您说不能用 webhook，所以我不开 /psp/webhook，PSP 的结果靠同步响应和我们主动查询。」
- **校验：** 「金额范围、charityId 是否存在，服务端校验，不信客户端。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 310">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">API（三个，没有 webhook 端点）</text>
<rect x="8" y="26" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="46" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">GET /charities</text>
<text x="18" y="61" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">无参数；几乎静态，可缓存</text>
<text x="18" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">返回 [{charityId, 名称}]</text>
<rect x="8" y="96" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="116" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">POST /donations</text>
<text x="18" y="131" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">donationId, charityId, 金额(分), 币种</text>
<text x="18" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">令牌, 邮箱 → {donationId, status}</text>
<rect x="8" y="166" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="186" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">GET /donations/:id</text>
<text x="18" y="201" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">无 body；前端每 2 秒轮询</text>
<text x="18" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">返回 {status}</text>
<rect x="8" y="238" width="324" height="62" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="18" y="258" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">同一个 donationId 重复 POST = 同一结果</text>
<text x="18" y="273" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">同 id 但内容不同 → 409，不扣款</text>
<text x="18" y="288" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">金额、机构以服务端校验为准</text>
</svg>
白板上新增：三张便签对应三个接口，和一块写着接口契约的虚线框。
**为什么这样说。** （约 2 分钟，累计第 11 分钟。）面试官看接口是否表达了幂等契约，以及令牌化是不是真的落到了接口上：body 里是令牌，不是卡号。强的回答把 donationId 放在 body 里并说明重复提交的结果。弱的回答让服务端生成 id，或者 body 里带卡号。
**面试官可能接着问。**
- POST 要同步返回结果吗？ → 先同步：等 PSP 返回后再响应，一般约 0.5 秒。如果超时或排队，就返回 PROCESSING，让前端用 GET 轮询。
- status 返回哪些值？前端怎么展示？ → PROCESSING 和 UNKNOWN 对用户都显示「处理中」，并提示「请勿重复付款，结果会发到邮箱」；SUCCEEDED 显示感谢，FAILED 提示换卡或换钱包。
- 银行要求额外验证（3-D Secure）怎么办？ → 前端按 PSP 组件的流程完成验证，再调我们的确认接口，我们向 PSP 查最终状态。画图时先不放进去，您追问我再展开。
**常见失分。**
- **服务端生成 id：** 用户重发时无法和上一次关联，重复扣款的第一层防线就没了。
- **body 里带卡号：** 说明没有理解令牌化。
- **依赖 webhook：** 面试官明确不让用，还画 webhook 端点，是没听限制。
