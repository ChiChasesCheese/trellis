---
id: hi-mock-notification-06-dive-ack
node: fix.notification-mock
type: qa
step: 6
---
## Q
**通知系统 · 第 6 步 · 深入一：什么时候回 202，崩溃之后丢什么**｜模拟面试

面试官：「你的接口回 202。如果服务器在回了 202 之后立刻崩溃，会发生什么？202 到底是在哪一步之后返回的？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先给结论：** 「202 在消息写进日志、并且复制到至少 2 个副本之后返回；在那之前我不返回。」
- **三种顺序，各丢什么：** 「A：日志写成之后回。崩在写成之前，调用方没有拿到 202，用同一个 id 重试；崩在写成之后，消息已经在至少 2 个副本上，不丢。最坏是重复。B：数据库提交之后回。也不丢，但库和日志是两次写，崩在中间就是库里有行而日志里没有消息，这条永远不会被发送，需要 outbox 或者扫描来补。C：供应商返回之后回。请求要挂 0.1 秒到几秒，回执峰值 3.5k/秒乘以 1 秒，就是 3,500 个连接被占着，供应商一挂我们的受理也挂了；超时的重试还可能多发一次。」
- **选 A：** 「A 把供应商和数据库都挡在请求路径之外，受理延迟只有一次日志写，约 5 到 10 毫秒（假设）。崩溃只带来重复，不带来丢失，重复由唯一约束吸收，深入四讲。」
- **日志的配置：** 「复制因子 3，acks=all，min.insync.replicas=2，生产者开幂等。同步副本少于 2 个时，写入被拒绝，我就回 503，绝不回 202。」
- **面试官问的那个崩溃：** 「API 实例是无状态的，崩了没有影响。消息已经在日志里；worker 从上一次提交的位移接着读，先处理后提交位移，所以最坏是重复读一次。状态库里还没有这一行也不要紧，worker 处理时会插入。」
- **202 的含义：** 「202 是『已受理，不会丢』，不是『已送达』。送达与否看状态接口和回调。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 288">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">202 在日志写成之后返回</text>
<rect x="8" y="34" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">产品团队</text>
<rect x="92" y="34" width="72" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="128" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">API</text>
<rect x="176" y="34" width="72" height="38" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="212" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">日志</text>
<rect x="260" y="34" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="296" y="57" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">worker</text>
<text x="48" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">POST id=r1</text>
<polyline points="44,110 128,110" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,110 121,113.2 121,106.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">append（acks=all）</text>
<polyline points="128,144 212,144" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,144 205,147.2 205,140.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="166" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">≥ 2 副本已写入</text>
<polyline points="212,178 128,178" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="128,178 135,181.2 135,174.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="48" y="200" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">202 Accepted</text>
<polyline points="128,212 44,212" fill="none" stroke-width="1.3" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="44,212 51,215.2 51,208.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="234" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">以下全是异步</text>
<line x1="8" y1="230" x2="128" y2="230" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="230" x2="332" y2="230" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<text x="216" y="258" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">拉取 · 发送 · 提交</text>
<polyline points="296,270 212,270" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="212,270 219,273.2 219,266.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="44" y1="74" x2="44" y2="292" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="74" x2="128" y2="292" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="74" x2="212" y2="121" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="135" x2="212" y2="155" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="169" x2="212" y2="292" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="296" y1="74" x2="296" y2="247" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="296" y1="261" x2="296" y2="292" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 276">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">三种顺序，崩溃各丢什么</text>
<rect x="8" y="26" width="324" height="74" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">A 日志写成后回 202（选它）</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">崩在前：无 202，调用方同 id 重试</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">崩在后：消息已在 ≥2 副本，不丢</text>
<text x="18" y="89.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">最坏：重复，被唯一键吸收</text>
<rect x="8" y="108" width="324" height="74" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">B 库提交后回 202</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">不丢，但库与日志是两次写</text>
<text x="18" y="156.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">库里有行、日志没消息：永远不发</text>
<text x="18" y="171.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">要 outbox 或扫描；受理延迟含库写</text>
<rect x="8" y="190" width="324" height="74" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">C 供应商返回后回 202</text>
<text x="18" y="223.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">请求挂 0.1–数秒：3.5k/秒 × 1 秒</text>
<text x="18" y="238.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">= 3,500 个连接占着；供应商挂则受理挂</text>
<text x="18" y="253.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">超时重试可能发两次</text>
</svg>
```
acks=all
enable.idempotence=true
replication.factor=3
min.insync.replicas=2
# 同步副本 < 2：写失败 -> API 回 503
```
白板上新增：一个时序图，三种顺序的对照，和生产者配置。
**为什么这样说。** （约 4 分钟，累计第 23 分钟。）面试官要听你说出：回 202 发生在哪一步、崩在每一个缝隙里会怎样。他当时从头到尾没有说出这个先后；被问「崩了会怎样」时，说的是「要有一个数据库存下来」，又落回 10 万次每秒的问题。强的回答第一句话给顺序，然后逐个说缝隙；弱的回答是「会有重试」。
**面试官可能接着问。**
- 为什么不先写库再写日志？ → 两次写没有共同的事务：库提交后日志写失败，这一行就卡在 queued。要么用 outbox（同事务写库和 outbox 行，由中继发布），要么反过来，把日志当真相、库由日志喂。我选后者：写入口只有一次写。
- acks=1 更快，为什么不用？ → 领导者确认后、复制前崩溃，这条消息就没了，而调用方已经拿到 202。回执不允许这样。
- 日志整个不可用呢？ → 回 503，调用方用同一个 id 重试。受理的可用性就是日志的可用性，所以日志按 3 副本、跨可用区部署。
- 为什么先处理后提交位移？ → 先提交后处理，崩溃会丢；先处理后提交，崩溃会重复。重复由去重吸收，丢失无法找回。
**常见失分。**
- **只说「会重试」：** 没说回 202 是在哪一步之后，也没说每个缝隙丢什么。
- **在请求路径里调供应商：** 受理延迟被供应商拖住，供应商一挂受理就挂。
- **回 202 之前什么都没写：** 实例一崩，消息就没了，调用方却以为成功。
- **把 202 说成已送达：** 受理和送达是两回事。
