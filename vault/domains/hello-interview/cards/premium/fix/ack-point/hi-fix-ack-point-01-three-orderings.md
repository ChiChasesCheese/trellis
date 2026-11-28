---
id: hi-fix-ack-point-01-three-orderings
node: fix.ack-point
type: qa
step: 1
---
## Q
**先说清 200 在哪一步返回 · 三种顺序**｜补强

面试官：「你的通知服务什么时候返回 200？是写日志之后、写库之后，还是调用供应商之后？每种顺序，服务崩了会丢什么？你选哪一种？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先说规则：** 「200 的意思是：我收下了，我崩了它也还在。所以我对每种顺序只看一件事：崩在哪里，丢什么。」
- **A，日志写入之后：** 「日志三副本，`acks=all`，`min.insync.replicas=2`，要两个同步副本确认才返回。崩在返回之前：调用方没收到，用同一个 id 重发，库里去重。崩在返回之后：消息已在两个副本里，worker 继续。丢 0 条，可能重复，唯一约束吸收。多等 1 至 5 毫秒。」
- **B，库提交之后：** 「也不丢。但库每秒写约 20,000，尖峰是 83,000：提交排队，返回变慢，调用方超时重试，尖峰变得更大。平均 5,800 写/秒的时候这种顺序可以用，尖峰时不行。」
- **C，供应商调用之后：** 「崩在调用之后、返回之前：调用方重发，用户收到两封。另外供应商慢几百毫秒到几秒，接受路径等着它；供应商挂了，我们的 API 也挂了。」
- **第 0 种不选：** 「在内存里就返回，或者 `acks=1` 只等 leader：返回之后 leader 崩了，这条消息没有任何副本，是真的丢。」
- **我选 A：** 「回执要 5 秒内；尖峰 83,000/秒只有日志吃得下；而且它不依赖任何供应商。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 132">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">200 可以放在三处：看崩在哪里</text>
<rect x="8" y="30" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">收到</text>
<text x="44" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">请求</text>
<rect x="92" y="30" width="72" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="128" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">日志</text>
<text x="128" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">append</text>
<rect x="176" y="30" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">库</text>
<text x="212" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">提交</text>
<rect x="260" y="30" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="296" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">供应商</text>
<text x="296" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">调用</text>
<polyline points="80,49 92,49" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="92,49 85,52.2 85,45.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polyline points="164,49 176,49" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="176,49 169,52.2 169,45.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<polyline points="248,49 260,49" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="260,49 253,52.2 253,45.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="128" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">A 之后</text>
<text x="212" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">B 之后</text>
<text x="296" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">C 之后</text>
<text x="8" y="110" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第 0 种：内存里就返回（acks=1）：</text>
<text x="8" y="126" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">返回后崩，这条没有任何副本，真丢</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 231">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每种顺序崩溃时丢什么</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">A 日志 acks=all 之后</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">丢 0 条；可能重复，唯一键吸收</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">多等 1 至 5 毫秒</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">B 库提交之后</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">丢 0 条；尖峰 83,000/秒 &gt; 库 20,000</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">提交排队 → 超时 → 重试风暴</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">C 供应商调用之后</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">崩在调用后：重发，用户收到两封</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">供应商慢，接受路径跟着慢</text>
</svg>
白板上：四个框一条线，A、B、C 三个位置，下面是各自崩溃时丢什么。
**为什么这样说。** （约 1 分钟。）面试官看你能不能把「确认」放在一个具体步骤之后，并说出每种放法的崩溃窗口。强的回答三种各一句，最后选一个并给三个理由（延迟、尖峰、不依赖供应商）；弱的回答说「先确认再异步」，不说确认在哪一步之后。
**面试官可能接着问。**
- `acks=all` 为什么还要 `min.insync.replicas=2`？ → 只有一个副本在同步时，`acks=all` 等于只等一个；设成 2，副本不够时写入失败，我返回 503，而不是悄悄降级。
- 返回之前崩，调用方重发，会收两封吗？ → 不会：同一个 notification_id，worker 的 INSERT 在唯一约束上返回 0 行，丢掉。
- 低流量系统（每秒 100 条）用 B 行吗？ → 行：库吃得下，一次提交就是持久，比 A 少一个组件。顺序的选择由尖峰和库的上限决定。
**常见失分。**
- **只说「先确认」：** 没有说确认在哪一步之后。
- **在内存里返回：** 返回之后的崩溃会丢消息。
- **把 C 当成「最可靠」：** 慢和重复都在这里。
