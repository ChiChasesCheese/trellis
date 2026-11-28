---
id: bagu-matchmaking-clock-1-elo-server-clock
node: b.scenario.matchmaking-clock
type: qa
step: 1
---
## Q
**对战匹配 · Elo 窗口与服务端棋钟**｜追问

面试官：「在线对弈按 Elo 等级分匹配，等久了怎么放宽？棋钟为什么必须由服务端说了算，网络延迟怎么补偿？」

## A
**基本回答。** 匹配：每个时间制（3 分钟、10 分钟）一个有序集合，score 是 Elo，`ZRANGEBYSCORE` 取 `rating ± w` 内的近邻；要求分数完全相等几乎匹配不上、扫全池又太贵。窗口 w 随等待放宽（起步 ±50，每 5 秒加 50，上限 ±400），窄则公平但等得久，宽则等得短但实力差距大。防配到同一人两次：按时间制分片、每片单写者，或 Lua 原子取出两人并删除；配对时有人掉线就把另一方放回队列。Elo 更新：期望 `E = 1/(1+10^((Rb−Ra)/400))`，`R' = R + K×(S−E)`，新手用较大的 K 收敛更快。计时：客户端倒计时只用来显示（信任客户端会被暂停时钟作弊）；服务端存 `turnStartedAt` 和双方剩余毫秒，走子到达时一次结算 `now − turnStartedAt`（没有每秒写压力），并补偿有上限的延迟 `min(估计延迟, 200ms)`，不冤枉高延迟玩家又不无限宽容。超时给当前方设延迟任务，到期先重读时钟再判，同一局事件串行处理，避免与刚到的走子竞态；只用服务端单调时钟，节点宕机后新所有者从日志重算并重挂定时器。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 290">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一步棋怎么扣时间</text>
<line x1="14" y1="60" x2="326" y2="60" stroke-width="1.2" stroke="currentColor"/>
<polygon points="326.0,60.0 319.0,63.2 319.0,56.8" fill="currentColor" stroke-width="0.5" stroke="currentColor"/>
<line x1="50" y1="52" x2="50" y2="68" stroke-width="1.2" stroke="currentColor"/>
<line x1="210" y1="52" x2="210" y2="68" stroke-width="1.2" stroke="currentColor"/>
<line x1="290" y1="52" x2="290" y2="68" stroke-width="1.2" stroke="currentColor"/>
<text x="50" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">轮到你</text>
<text x="50" y="86" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">turnStartedAt</text>
<text x="206" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">走子发出</text>
<text x="290" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">服务端收到</text>
<line x1="210" y1="60" x2="290" y2="60" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="250" y="86" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">延迟 d</text>
<text x="8" y="112" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">扣时 = 收到时刻 − turnStartedAt</text>
<text x="8" y="130" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">再减去延迟补偿 min(d, 200ms)</text>
<line x1="8" y1="144" x2="332" y2="144" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="8" y="162" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">匹配窗口随等待放宽</text>
<text x="8" y="182" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">0 秒：±50</text>
<rect x="151" y="186" width="38" height="10" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">10 秒：±150</text>
<rect x="114" y="218" width="112" height="10" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="8" y="246" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">35 秒：±400（上限）</text>
<rect x="20" y="250" width="300" height="10" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="170" y1="182" x2="170" y2="264" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<text x="170" y="284" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">中心线是自己的 Elo</text>
</svg>
上半部分是一步棋怎么扣时间：以服务端时刻为准，只补回有上限的延迟；下半部分是匹配窗口随等待变宽直到上限。
**举个例子。** A 的 Elo 1500 在 10 分钟队列等：0 秒窗口 ±50 没人；10 秒窗口 ±150，找到 1620 的 B（差 120），原子取出两人开局。A 比 B 弱，E 小于 0.5，A 赢了涨得多。走子时服务端 `now − turnStartedAt` 为 8.6 秒，估计路上花 0.3 秒，补偿 `min(0.3 秒, 200ms)` = 200ms，实际扣 8.4 秒。
**容易错。**
- **窗口固定不放宽：** 冷门时段永远匹配不上。
- **超时和走子各判各的：** 会出现双重结果。
