---
id: hi-mock-uber-05-api
node: sd.problem-breakdowns.uber.mock
type: qa
step: 5
---
## Q
**网约车 · 第 5 步 · API**｜模拟面试

面试官：「好，接着定义接口吧。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **一共四个：** 「估价、叫车、司机上报位置、司机接单。匹配发生在后台，没有对外接口。」
- **估价：** 「`POST /fare`，body 是起点和终点，返回 Fare，里面有估价和 ETA。用 POST，因为会新建一条 Fare。」
- **叫车：** 「`POST /rides`，body 只有 fareId，返回 Ride，状态是 requested。」
- **上报位置：** 「`POST /drivers/location`，body 是 lat 和 long，返回成功或失败。」
- **司机接单：** 「`PATCH /rides/:rideId`，body 是 accept 或 deny，返回 Ride，里面有上车点和目的地，司机端靠它导航。」
- **身份和时间：** 「用户身份取自令牌（JWT）或会话，不放在 body 里；时间戳由服务端生成；价格从库里读，不信客户端传来的值。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 380">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">API（四个，匹配在后台，无对外接口）</text>
<rect x="8" y="26" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="46" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">POST /fare</text>
<text x="18" y="61" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">body：pickup, destination</text>
<text x="18" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">返回 Fare（估价 + ETA）</text>
<text x="324" y="41" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">乘客</text>
<rect x="8" y="96" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="116" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">POST /rides</text>
<text x="18" y="131" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">body：fareId（只有这一项）</text>
<text x="18" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">返回 Ride，状态 requested</text>
<text x="324" y="111" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">乘客</text>
<rect x="8" y="166" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="186" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">POST /drivers/location</text>
<text x="18" y="201" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">body：lat, long</text>
<text x="18" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">返回 成功 / 失败</text>
<text x="324" y="181" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">司机</text>
<rect x="8" y="236" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="256" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">PATCH /rides/:rideId</text>
<text x="18" y="271" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">body：accept 或 deny</text>
<text x="18" y="286" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">返回 Ride（含上车点）</text>
<text x="324" y="251" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">司机</text>
<rect x="8" y="308" width="324" height="62" rx="6" stroke-width="1.2" stroke-dasharray="4 3" fill="none" stroke="currentColor"/>
<text x="18" y="328" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">身份取自令牌（JWT），不放 body</text>
<text x="18" y="343" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">时间戳由服务端生成</text>
<text x="18" y="358" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">价格从库里读，不信客户端传的</text>
</svg>
白板上新增：四个接口，每个写出路径、body、返回值，右上角标是乘客还是司机调用；底部一框写安全规则。
**为什么这样说。** （约 3 分钟，累计第 10 分钟。）面试官看接口是否覆盖三条功能、资源命名是否合理，以及有没有安全意识。很多人会把 userId、时间戳甚至估价放进 body，这是明显的红旗：客户端传来的任何值都能被篡改。强的回答一边写接口，一边顺口说出身份来自令牌、价格来自库。
**面试官可能接着问。**
- 叫车为什么只传 fareId？ → 价格、起终点都在服务端的 Fare 里，客户端只指一下是哪条。客户端不能决定价格。
- 位置上报一直用 HTTP 吗？ → 先用，简单。每秒 200 万次的压力是后端存储问题，放到深入一解决；以后也可以换成长连接减少握手开销。
- 司机怎么收到订单？ → 不是靠接口轮询，匹配之后由通知服务推送（APNs、FCM），高层设计里会画。
**常见失分。**
- **body 里传身份：** 把 userId、driverId 放在 body，等于让客户端自己声明是谁。
- **客户端传价格：** 估价、费用都不能由客户端提交，必须读库。
- **接口过细：** 为匹配单独设一个对外接口，其实它只发生在后台，多此一举。
