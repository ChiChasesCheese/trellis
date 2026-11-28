---
id: hi-fix-notification-05-when-200
node: fix.notification
type: qa
step: 5
---
## Q
**通知系统 · 200 在哪一步返回**｜复盘

面试官：「响应返回的那一刻，通知已经送到手机了吗？如果通知服务在返回之后立刻崩溃，会怎样？」

你会怎么回答？

## A
**当时的回答。**
- **说了「先确认、再异步」：** 「our notification server will acknowledge this request and then have workers send the notifications」（10:03）。顺序是对的。
- **没说确认放在哪一步之后：** 白板上写的是「response: 200」。是日志写完之后？库提交之后？发送之后？整场没有说出来。
- **崩溃的问题绕到了数据库：** 面试官在 10:07 问「what if the notification server crashes right after it acknowledged」，你答「we need some database to store all the request」（11:28），后面换成日志（13:51），但没有把「200 在日志写入之后」这一句说出来。
**差在哪。**
- **这是整题的核心：** 「崩溃后会不会丢」只由一件事决定：200 返回的时刻，消息是否已经在一个崩了也还在的地方。没说，面试官只能猜。
- **200 的含义不清：** 面试官在 09:14 问「has the notification actually been delivered」，答案应该是「没有，只是我收下了」，也就是 202 Accepted，而不是 200 成功。
- **同一件事换了三种说法：** 数据库、日志、状态，每次都没有落到「在返回之前」这个顺序上。
**应该这样说。**
- **先说那一句：** 「我在消息写进日志、两个以上副本确认之后返回 202 Accepted，发送是之后异步做的。」
- **配置：** 「日志三副本，`acks=all`，`min.insync.replicas=2`：写入要等同步副本确认才算成功。多等 1 至 5 毫秒（同区域一次日志写）。」
- **崩在返回之前：** 「调用方没有收到 202，用同一个 notification_id 重发，库里的唯一约束去重。」
- **崩在返回之后：** 「消息已经在两个副本里，worker 从偏移量继续读，不丢。」
- **日志写不进去：** 「返回 503，不返回 200：说「收下了」就要真的收下了。」
- **202 不是「送到了」：** 「状态是 queued；调用方用 notification_id 查状态。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 268">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">产品团队</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">通知服务</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">日志</text>
<rect x="260" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="296" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">worker</text>
<text x="48" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">POST（带 id）</text>
<polyline points="44,84 128,84" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,84 121,87.2 121,80.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">append，acks=all</text>
<polyline points="128,118 212,118" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,118 205,121.2 205,114.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2 个副本已确认</text>
<polyline points="212,152 128,152" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,152 135,155.2 135,148.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="174" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">202 Accepted</text>
<polyline points="128,186 44,186" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,186 51,189.2 51,182.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="208" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">此后才异步发送</text>
<line x1="8" y1="204" x2="122" y2="204" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="218" y1="204" x2="332" y2="204" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<text x="216" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">取消息，发送</text>
<polyline points="296,244 212,244" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,244 219,247.2 219,240.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="44" y1="48" x2="44" y2="266" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="61" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="75" x2="128" y2="197" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="211" x2="128" y2="266" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="95" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="109" x2="212" y2="129" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="143" x2="212" y2="197" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="211" x2="212" y2="266" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="296" y1="48" x2="296" y2="266" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 186">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">崩在 202 的前后，各丢什么</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">202 之前崩</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">客户端没收到响应</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">用同一个 id 重发，库里去重</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">202 之后崩</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">消息已在 2 个副本里</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">worker 从偏移量继续，不丢</text>
<text x="8" y="180" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">日志写失败或超时：返回 503，不返回 200</text>
</svg>
白板上：四条竖线，202 画在 append 确认之后；下面两格是崩在两侧的结果。
**为什么这样说。** （约 1 分钟。）面试官在测你是否清楚「确认」和「持久」的先后。强的回答用一句话指出确认放在哪一步之后，两种崩溃各一句；弱的回答说「先确认，之后异步」，顺序里缺那一步。
**面试官可能接着问。**
- 为什么不等库提交再返回？ → 库每秒只写约 20,000，尖峰 83,000 会让返回变慢、超时、重试，更大的尖峰；见下一组「三种顺序」。
- 为什么不等供应商返回？ → 供应商慢几百毫秒到几秒，会占满接受路径，重试还会造成两封。
- `acks=all` 之后日志一定不丢吗？ → 在 `min.insync.replicas=2` 下，同步副本只剩一个时写入会失败而不是悄悄降级；三个副本同时坏才会丢。
**常见失分。**
- **只说「先确认」：** 不说确认之后什么已经落地。
- **用 200 表示送达：** 实际只是收下。
- **日志写失败还返回 200：** 这就是丢消息。
**同类题。**
- **下单、上传：** 同一条规则，见「先说清 200 在哪一步返回」。
