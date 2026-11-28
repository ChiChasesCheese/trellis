---
id: hi-fix-ack-point-04-say-it-and-202
node: fix.ack-point
type: qa
step: 4
---
## Q
**先说清 200 在哪一步返回 · 白板上那一句话**｜补强

面试官：「接受请求的接口返回什么？调用方怎么知道通知最后有没有送到？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **那一句话：** 「我在消息写进日志、两个以上副本确认之后，返回 202 Accepted；发送是异步的，调用方用 `notification_id` 查状态。」写在 POST 的箭头旁边，面试官就不必再问「什么时候返回」。
- **为什么是 202 不是 200：** 「200 读起来是做完了。202 的意思就是收下了，还没处理完，调用方不会把它当成已送达。」
- **响应里有什么：** 「`Location` 指向状态地址，响应体里是 notification_id 和状态 queued。」
- **状态怎么走：** 「queued、sending、sent（供应商收下）、delivered（回执确认），任一步失败是 failed，带原因。sent 和 delivered 之间靠供应商的 webhook，和定时对账补丢失的。」
- **同键重发：** 「同样的 202 和同一个 Location，不是 409，也不会再发一次。」
- **不能收下的情况：** 「日志写不进去：503，调用方用同一个键重试；超配额：429 加 `Retry-After`；请求体不合法：400，不进日志；同键不同请求体：422。」
- **只有这一个状态码是收下：** 「除了 202，都不应该让调用方以为消息已经安全。」
**白板。**
```
POST /v1/notifications
Idempotency-Key: receipt:pay_881

HTTP/1.1 202 Accepted
Location: /v1/notifications/n_7f3a
{"notification_id": "n_7f3a",
 "status": "queued"}

GET /v1/notifications/n_7f3a
{"status": "sent"}
-- queued -> sending -> sent
-- -> delivered | failed
```

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 146">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">状态：调用方用 id 查</text>
<rect x="8" y="32" width="72" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="44" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">queued</text>
<text x="44" y="63" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已入日志</text>
<rect x="92" y="32" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">sending</text>
<text x="128" y="63" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">worker 取走</text>
<rect x="176" y="32" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">sent</text>
<text x="212" y="63" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">供应商收下</text>
<rect x="260" y="32" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="296" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">delivered</text>
<text x="296" y="63" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">回执确认</text>
<polyline points="80,51 92,51" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="92,51 85,54.2 85,47.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polyline points="164,51 176,51" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="176,51 169,54.2 169,47.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polyline points="248,51 260,51" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="260,51 253,54.2 253,47.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="92" y="90" width="156" height="22" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="105.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">failed：任一步，带原因</text>
<text x="8" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">202 之后第一个状态就是 queued</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 201">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">什么时候返回什么</text>
<rect x="8" y="26" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">日志写入成功</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">202 + Location + queued</text>
<rect x="8" y="78" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="96.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">同键重发</text>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">同样的 202 和同一个 Location</text>
<rect x="8" y="130" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="148.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">不能收下</text>
<text x="18" y="163.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">日志写不进：503；超配额：429</text>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">请求体非法：400；同键不同体：422</text>
</svg>
白板上：一个请求一个响应，下面是状态链，右下角是各种返回码各管什么。
**为什么这样说。** （约 45 秒。）面试官要听到「确认」的含义被说清：收下，不是送达；调用方有办法追踪。强的回答一句话加一个状态地址，几个错误码各一句；弱的回答说「返回 200 success」，调用方无法区分已收下、已送达。
**面试官可能接着问。**
- 调用方一直轮询状态怎么办？ → 状态读是主键查询，约 1 到 5 毫秒；更好的是让调用方登记 webhook，状态变化时我们推；轮询要限速。
- 202 之后永远停在 queued？ → 监控最老 queued 的年龄，超过 1 分钟告警；扫描把还是 queued 的行重新入队。
- 为什么 503 而不是 500？ → 503 告诉调用方这是暂时的，可以用同一个键重试；500 没有这层含义。
**常见失分。**
- **返回 200 success：** 调用方把它当成已送达。
- **没有状态地址：** 调用方不知道结果，只能再发一次，变成重复。
- **日志写失败还返回 202：** 收下了却没有收下。
