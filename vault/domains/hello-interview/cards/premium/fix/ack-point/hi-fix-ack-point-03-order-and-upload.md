---
id: hi-fix-ack-point-03-order-and-upload
node: fix.ack-point
type: qa
step: 3
---
## Q
**先说清 200 在哪一步返回 · 下单和上传**｜补强

面试官：「同样的问题换两道：用户下单，你什么时候返回？用户上传一个 500 MB 的视频，你什么时候说上传成功？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **规则一句话：** 「200 放在「崩了也还在」的那一步之后，在「慢的、能重做的」那一步之前。」
- **下单：** 「订单行（状态 `PENDING_PAYMENT`）和一条 outbox 行在同一个库事务里提交，然后返回 201 和 order_id。库存确认、扣款、发确认邮件在返回之后，由 outbox 驱动，每一步可重做。」
- **下单崩在哪：** 「提交之前崩：没有订单，调用方带同一个 Idempotency-Key 重试，就是第一次。提交之后崩：订单在，relay 继续发事件。」
- **如果必须同步扣款：** 「那是另一个需求，要先问：用户要不要立刻知道扣款成功。如果要，返回等的是扣款结果；这是产品决定，不是持久化要求。」
- **上传：** 「客户端用预签名 URL 直传对象存储。存储返回 200 时对象已经在多个可用区里，这就是落地。然后客户端调 `complete`，服务记元数据行，返回 202：病毒扫描、缩略图、转码都是之后异步做的，状态用 id 查。」
- **上传崩在哪：** 「存储已成功、`complete` 还没调：对象没有元数据行。存储的事件通知兜底，或者定时任务清理孤儿对象。大文件分块上传，只有 `CompleteMultipartUpload` 成功才算落地，中断后用 `ListParts` 续传。」
- **通知也是这一条：** 「日志写入之后，才限流、发送。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 231">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一条规则：先落地，再返回，慢的放后面</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">通知</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">落地：日志 append，acks=all</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">之后：限流、发送、重试</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">下单</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">落地：订单行 + outbox，一个事务</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">之后：库存确认、扣款、发邮件</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">上传</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">落地：对象存储返回 200</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">之后：病毒扫描、缩略图、转码</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 164">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">崩在落地前后</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">落地之前崩</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">调用方没收到，用同一个键重试</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">还没写下任何东西，重做就是第一次</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">落地之后崩</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">东西已在，后面的步骤由 outbox 或</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">事件继续，每一步都可重做</text>
</svg>
白板上：三道题三行，每行「落地」「之后」；下面一格说崩在两侧各是什么。
**为什么这样说。** （约 1 分钟。）面试官看的是你有没有一套能搬的规则，而不是通知系统的一个特例。强的回答每换一个题，句式不变，只换「落地」是什么；弱的回答每道题发明一种新说法，说不清返回的含义。
**面试官可能接着问。**
- 订单返回 201 还是 202？ → 订单行已经建好，是 201；如果创建本身也是异步的（订单要排队处理），用 202 加状态地址。
- 上传 500 MB，为什么不经过我的服务？ → 经过的话，一个 500 MB 请求占着一个连接几分钟，并发 1,000 人就是 500 GB 在途；直传存储，我的服务只管元数据。
- 订单事务里能不能直接扣库存？ → 同库可以：一条条件 UPDATE 在同一个事务里；库存在别的服务就不行，走 outbox 与预留。
**常见失分。**
- **等所有步骤做完再返回：** 一个慢步骤拖住所有调用，重试变重复。
- **落地之前就返回：** 返回之后崩，用户以为成功，东西没了。
- **只会说通知的特例：** 换题就说不清。
