---
id: hi-sdx-coordinated-omission
node: sd.core-concepts.numbers-to-know.more
type: qa
step: 1
---
## Q
**压测漏掉排队的样本**｜补充 · 必须知道的数字 · 追问

压测工具每个线程「发请求、等响应、再发下一个」。服务中途卡了 10 秒，压测得到的 p99 却还是 10 ms。哪里错了？怎么测对？

## A
**结论。** 这叫协同遗漏（coordinated omission）：服务卡住时工具跟着停发，排队等待的请求根本没被记录。要按固定计划发请求，并从「计划发送时刻」起算延迟。

**要点。**
- **闭环为什么错：** 服务卡住时线程在等唯一的那个请求，本该在这 10 秒里发出的上千个请求没发出，也就没有对应的慢样本。
- **算一笔账：** 计划每秒 100 个。90 秒正常（9000 条 10 ms）加 1 条 10 秒的慢样本，p99 仍是 10 ms。
- **开环怎么记：** 停顿期间计划发出 1000 个，每个从计划时刻算到完成，延迟从 10 秒递减到 10 ms，共 1000 条慢样本，p99 约 9000 ms。
- **怎么做：** 用按固定到达率发压的工具（如 wrk2、k6 的 constant-arrival-rate），或补记缺失的样本（HdrHistogram 的期望间隔校正）。
- **在客户端测：** 用户等待的是排队加服务，只在服务端计时看不到排队。

**为什么。** 真实用户不会因为你的服务卡了就停止到来。压测要模拟「到达与服务快慢无关」的负载。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 230">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">服务在中间停顿 10 秒</text>
<rect x="120" y="72" width="120" height="26" rx="3" stroke-width="1" fill="currentColor" fill-opacity="0.18" stroke="currentColor"/>
<rect x="120" y="146" width="120" height="26" rx="3" stroke-width="1" fill="currentColor" fill-opacity="0.18" stroke="currentColor"/>
<text x="8" y="66" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">闭环：等响应再发下一个</text>
<line x1="24" y1="78" x2="24" y2="90" stroke-width="1.2" stroke="currentColor"/>
<line x1="36" y1="78" x2="36" y2="90" stroke-width="1.2" stroke="currentColor"/>
<line x1="48" y1="78" x2="48" y2="90" stroke-width="1.2" stroke="currentColor"/>
<line x1="60" y1="78" x2="60" y2="90" stroke-width="1.2" stroke="currentColor"/>
<line x1="72" y1="78" x2="72" y2="90" stroke-width="1.2" stroke="currentColor"/>
<line x1="84" y1="78" x2="84" y2="90" stroke-width="1.2" stroke="currentColor"/>
<line x1="96" y1="78" x2="96" y2="90" stroke-width="1.2" stroke="currentColor"/>
<line x1="108" y1="78" x2="108" y2="90" stroke-width="1.2" stroke="currentColor"/>
<line x1="120" y1="84" x2="240" y2="84" stroke-width="3" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="248" y1="78" x2="248" y2="90" stroke-width="1.2" stroke="currentColor"/>
<line x1="260" y1="78" x2="260" y2="90" stroke-width="1.2" stroke="currentColor"/>
<line x1="272" y1="78" x2="272" y2="90" stroke-width="1.2" stroke="currentColor"/>
<line x1="284" y1="78" x2="284" y2="90" stroke-width="1.2" stroke="currentColor"/>
<line x1="296" y1="78" x2="296" y2="90" stroke-width="1.2" stroke="currentColor"/>
<line x1="308" y1="78" x2="308" y2="90" stroke-width="1.2" stroke="currentColor"/>
<text x="8" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只记 1 条慢样本</text>
<text x="8" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">开环：按计划发，从计划时刻计时</text>
<line x1="24" y1="152" x2="24" y2="164" stroke-width="1.2" stroke="currentColor"/>
<line x1="36" y1="152" x2="36" y2="164" stroke-width="1.2" stroke="currentColor"/>
<line x1="48" y1="152" x2="48" y2="164" stroke-width="1.2" stroke="currentColor"/>
<line x1="60" y1="152" x2="60" y2="164" stroke-width="1.2" stroke="currentColor"/>
<line x1="72" y1="152" x2="72" y2="164" stroke-width="1.2" stroke="currentColor"/>
<line x1="84" y1="152" x2="84" y2="164" stroke-width="1.2" stroke="currentColor"/>
<line x1="96" y1="152" x2="96" y2="164" stroke-width="1.2" stroke="currentColor"/>
<line x1="108" y1="152" x2="108" y2="164" stroke-width="1.2" stroke="currentColor"/>
<line x1="120" y1="152" x2="120" y2="164" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="132" y1="152" x2="132" y2="164" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="144" y1="152" x2="144" y2="164" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="156" y1="152" x2="156" y2="164" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="168" y1="152" x2="168" y2="164" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="180" y1="152" x2="180" y2="164" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="192" y1="152" x2="192" y2="164" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="204" y1="152" x2="204" y2="164" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="216" y1="152" x2="216" y2="164" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="228" y1="152" x2="228" y2="164" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="240" y1="152" x2="240" y2="164" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="252" y1="152" x2="252" y2="164" stroke-width="1.2" stroke="currentColor"/>
<line x1="264" y1="152" x2="264" y2="164" stroke-width="1.2" stroke="currentColor"/>
<line x1="276" y1="152" x2="276" y2="164" stroke-width="1.2" stroke="currentColor"/>
<line x1="288" y1="152" x2="288" y2="164" stroke-width="1.2" stroke="currentColor"/>
<line x1="300" y1="152" x2="300" y2="164" stroke-width="1.2" stroke="currentColor"/>
<line x1="312" y1="152" x2="312" y2="164" stroke-width="1.2" stroke="currentColor"/>
<text x="8" y="188" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">停顿期间计划发出 1000 次，全算慢样本</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">p99：闭环 10 ms，开环约 9,000 ms</text>
</svg>

**面试里这样说。** 「我会用开环压测，按固定速率发请求，延迟从计划发送时刻算。闭环会因为服务变慢而自己降速，漏掉排队的样本，p99 会好看得离谱。」

**易错。**
- **只看平均值或服务端日志：** 排队时间不在服务端的处理耗时里。
- **相信 10 ms 的 p99：** 同一次事故里，闭环测出 10 ms，开环测出约 9 秒。
