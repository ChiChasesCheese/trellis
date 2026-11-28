---
id: hi-sdx-email-smtp-delivery
node: more.email-service
type: qa
step: 1
---
## Q
**邮件怎么投递：信封、MX 与退信**｜补充 · 邮件服务（Gmail） · 必会

Alice 在自己的邮件服务里给 bob@example.org 发了一封信。发信服务器怎么找到 Bob 的收信服务器？对话里的「信封」和用户看到的 From 是一回事吗？对方回 4xx 和回 5xx，发信一方分别该怎么做？对方回「已接受」又意味着什么？

## A
**结论。** 发信服务器先查 example.org 的 MX 记录找到收信服务器，再用 SMTP 的几条命令把信交过去。信封（MAIL FROM、RCPT TO）是给服务器看的投递信息，信里的 From 头是给人看的，两者可以不同。对方回 4xx 是临时失败，稍后重试；回 5xx 是永久失败，不再重试，改给信封发件人发一封退信（bounce）。回 250 表示接受，从这一刻起投递责任归对方。

**要点。**
- **MX 记录：** 域名在 DNS 里登记「谁来收这个域的信」，可以有多台、带优先级；发信方连它们的 25 端口。
- **信封与信头：** MAIL FROM 是信封发件人，退信发给它；DATA 里的 From 头才是用户看到的发件人。就像寄实体信，信封上的回邮地址和信纸落款可以不同。
- **4xx 临时失败：** 例如 450、451（对方忙、限流）。发信方把信留在队列里退避重试；标准建议重试间隔至少 30 分钟，放弃时间通常 4 到 5 天。
- **5xx 永久失败：** 例如 550（无此用户）。重试也不会成功，立即停止，给信封发件人发退信。
- **接受即移交：** 回 250 之后信由对方负责。接受后再想拒绝，只能事后发退信，而信封发件人可能是伪造的，退信会砸到无辜的人，所以拒绝要在对话里当场做。

**为什么。** 邮件是一跳一跳转交的存储转发（store-and-forward），每一跳的应答都是责任交接的信号。4xx 与 5xx 的分工，让发信方不用猜该重试还是放弃。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 326">
<rect x="22" y="8" width="96" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="70.0" y="27.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发信服务器</text>
<rect x="222" y="8" width="96" height="30" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="270.0" y="27.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">收信服务器</text>
<polyline points="70,38 70,322" fill="none" stroke-width="1" stroke-dasharray="2 4" stroke="currentColor"/>
<polyline points="270,38 270,322" fill="none" stroke-width="1" stroke-dasharray="2 4" stroke="currentColor"/>
<polyline points="70,70 270,70" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="270,70 263,66.8 263,73.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="170.0" y="64" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">MAIL FROM（信封发件人）</text>
<polyline points="70,108 270,108" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="270,108 263,104.8 263,111.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="170.0" y="102" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">RCPT TO（收件人）</text>
<polyline points="70,146 270,146" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="270,146 263,142.8 263,149.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="170.0" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">DATA：From 头 + 正文</text>
<text x="170" y="190" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">收信方三选一回复</text>
<polyline points="270,224 70,224" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="70,224 77,220.8 77,227.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="170.0" y="218" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">250 接受：责任移交</text>
<polyline points="270,264 70,264" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="70,264 77,260.8 77,267.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="170.0" y="258" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4xx 临时失败：稍后重试</text>
<polyline points="270,304 70,304" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="70,304 77,300.8 77,307.2" style="fill:var(--accent,#3b6fd4)"/>
<text x="170.0" y="298" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">5xx 永久失败：退信</text>
</svg>

**面试里这样说。** 「入站我们是接收方：在 SMTP 对话里就决定接受还是拒绝，回 250 就等于承诺投递；拒绝用 5xx 当场说，临时过载用 4xx 让对方重试。出站按 MX 找目的服务器，收到 4xx 退避重试，收到 5xx 给信封发件人退信。」

**易错。**
- **接受后再退信：** 信封发件人常被伪造，退信变成骚扰无辜的人。
- **把 5xx 当临时错误重试：** 永远不会成功，白占队列。
- **一遇 4xx 就退信：** 对方只是忙，合法邮件被白白退掉。
- **混淆信封与 From 头：** 验证了信封发件人，不等于验证了用户看到的发件人。
