---
id: hi-mock-notification-04-api
node: fix.notification-mock
type: qa
step: 4
---
## Q
**通知系统 · 第 4 步 · API**｜模拟面试

面试官：「好，产品团队要发一条支付回执，接口怎么设计？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **形状：** 产品团队调用我们，我们负责投递；五个接口：发回执、发活动、查回执状态、查活动状态，加给供应商用的回调入口。
- **发回执：** `POST /v1/notifications`，体：notification_id、user_id、type、template_id、params；返回 **202 Accepted**，体含 notification_id、status: accepted、status_url。
- **幂等键：** notification_id 由调用方在第一次请求前生成，来自业务事件（如 `receipt:po_8841`，po_8841 是支付订单号）；同一事件每次重发用同一个 id，换随机数去重就没意义。同 id 再来仍返回 202、体与第一次相同，不再发第二条（机制见深入四）。
- **为什么 202：** 表示「已受理」不是「已送达」；只在消息写进持久日志并复制之后才返回，日志写不进就返回 503，调用方用同一个 id 重试。
- **发活动：** `POST /v1/campaigns`（campaign_id、audience_id、template_id、send_at、expires_at），同样 202；扇出异步，进度从 `GET /v1/campaigns/{id}` 读。
- **查状态：** `GET /v1/notifications/{id}` 只读本地状态库，不调供应商；状态 accepted、sent、delivered、failed、suppressed。
- **其他：** 正文最大 4 KB；每个产品团队有配额，超了 429 加 Retry-After；偏好由用户自己改，在偏好服务里。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 231">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">返回码</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">202 Accepted</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">已写入日志并复制；不是已送达</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同 notification_id 重发：再返回 202</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">4xx</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">400 参数错 · 401/403 无权限</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">413 正文超 4 KB · 429 超配额</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">503</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">日志写不进去：不回 202</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">调用方拿同一个 id 重试</text>
</svg>
白板上新增：五个接口，和三类返回码。

**常见失分。**
- **返回 200 却说不清含义：** 被问「此刻送达了吗」才讲到异步。
- **没有幂等键，或键由服务端生成：** 超时重试发出第二张回执。
- **活动当作一万次请求：** 受理接口被压垮，也没处续跑。
- **应用服务器直接连用户：** 跳过通知服务；调用方只该把请求交给通知服务。

**面试官可能接着问。**
- 同 id 内容不同？ → 以第一次为准，后到的忽略并记告警；那是调用方 bug。
- 为什么不让服务端生成 id？ → 请求超时调用方没拿到 id，重发就是新请求，会出第二张回执。
- 活动为什么不循环调 1,000 万次回执接口？ → 压垮受理接口、占配额；服务内部展开可限速、暂停、续跑。
