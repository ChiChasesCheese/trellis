---
id: hi-sdx-step-2pc-commit-point
node: sd.patterns.multi-step-processes.more
type: qa
step: 1
---
## Q
**两阶段提交：提交点与悬而未决**｜补充 · 多步骤流程 · 必会

面试官：「讲一下两阶段提交（2PC）的两个阶段，指出提交点在哪。已经投了 yes 的参与者，为什么不能超时后自己中止？」

## A
**结论。** 提交点是协调者把「提交」决定写进自己的持久日志的那一刻，之后不可撤销。投了 yes 的参与者不知道协调者是否已过提交点，擅自中止就可能破坏原子性，所以只能保持悬而未决，持着锁等答案。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="10" y="8" width="214" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="117.0" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 协调者发 prepare</text>
<text x="117.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">带全局事务号</text>
<polyline points="117,48 117.0,57.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="117,64 113.8,57.0 120.2,57.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="64" width="214" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="117.0" y="82.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 参与者写好日志与锁</text>
<text x="117.0" y="97.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">投 yes：承诺崩溃后也能提交</text>
<polyline points="117,108 117.0,117.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="117,124 113.8,117.0 120.2,117.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="124" width="214" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="117.0" y="142.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 协调者把「提交」写进日志</text>
<text x="117.0" y="157.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">提交点，不可撤销</text>
<polyline points="117,168 117.0,177.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="117,184 113.8,177.0 120.2,177.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="184" width="214" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="117.0" y="202.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 协调者发 commit</text>
<text x="117.0" y="217.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一直重试到全部确认</text>
<polyline points="232,64 252,64 252,228 232,228" fill="none" stroke-width="1.3" stroke="currentColor"/>
<text x="260" y="128" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">悬而未决</text>
<text x="260" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">持着锁，</text>
<text x="260" y="162" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不能擅自</text>
<text x="260" y="178" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">中止</text>
<text x="8" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">投 yes 之后，参与者不知道协调者是否已过提交点。</text>
</svg>

**要点。**
- **准备阶段：** 协调者发 prepare，参与者把修改和锁持久写入日志，回答 yes（承诺此后无论怎样崩溃都能提交）或 no。
- **提交阶段：** 全部 yes 后，协调者先写自己的提交日志，再发 commit，重试到每个参与者都确认。
- **为什么不能自己中止：** commit 消息可能只是丢了或慢了。参与者若中止而决定其实是提交，其他参与者提交了、它没有，原子性就破了。
- **悬而未决的代价：** 它持着锁，挡住所有冲突事务，直到协调者或它恢复后的日志给出答案。
- **三阶段提交：** 只在同步网络、故障检测可靠时才消除阻塞，真实网络给不了这些假设，所以没人用。

**面试里这样说。** 「2PC 的提交点是协调者写下提交决定的那条日志。投过 yes 的参与者不能自己超时中止，因为决定可能已经是提交；它只能持锁等协调者，所以协调者必须可恢复，通常把决定写进复制日志。」

**易错。**
- **把提交点说成参与者都投了 yes：** 决定持久写入之前，协调者仍可中止。
- **以为投 yes 的参与者超时就能回滚：** 这会让不同参与者得出不同结论。
