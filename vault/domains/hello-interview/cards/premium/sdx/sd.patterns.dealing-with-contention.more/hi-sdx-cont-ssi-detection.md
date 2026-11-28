---
id: hi-sdx-cont-ssi-detection
node: sd.patterns.dealing-with-contention.more
type: qa
step: 5
---
## Q
**SSI 在哪两个时刻发现读到了过期的前提**｜补充 · 处理争用 · 加分

面试官：「SSI 让事务在快照上不加锁地运行，再中止那些依据过期信息的事务。引擎具体在哪两个时刻发现一个事务依据的信息已经过期？为什么两个方向都要查？」

## A
**结论。** 两处发现的是同一件事，即读被并发的写作废了，只是方向相反：读的时候发现有并发的未提交写；写的时候发现写进了别人读过的范围。真正中止推迟到提交，误报更少。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 268">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">同一件事，从两个方向发现：读被并发写作废</text>
<rect x="10" y="28" width="148" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="84.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写先发生</text>
<text x="84.0" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">T2 写了 x，尚未提交</text>
<polyline points="158,50 173.0,50.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="180,50 173.0,53.2 173.0,46.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="180" y="28" width="150" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255.0" y="46.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">T1 读 x：快照看不到</text>
<text x="255.0" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">记一条读写依赖</text>
<rect x="10" y="92" width="148" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="84.0" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读先发生</text>
<text x="84.0" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">T1 读了范围 R</text>
<polyline points="158,114 173.0,114.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="180,114 173.0,117.2 173.0,110.8" style="fill:var(--accent,#3b6fd4)"/>
<rect x="180" y="92" width="150" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255.0" y="110.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">T1 留下 SIRead 标记</text>
<text x="255.0" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">T2 写进 R：记依赖</text>
<polyline points="170,148 170.0,161.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,168 166.8,161.0 173.2,161.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="168" width="320" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="184.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">提交时分析依赖</text>
<text x="170.0" y="199.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">可能成环就中止其中一个，应用重试</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">推迟到提交再中止：使前提失效的写者</text>
<text x="8" y="248" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">可能自己回滚，读者也可能是只读事务。</text>
</svg>

**要点。**
- **写先发生：** 读的时候 MVCC 发现这个对象有一个并发、尚未可见的事务写的版本，说明快照忽略了一个写。此时不中止，因为写者还可能回滚；写者提交后，读者若再提交写入就被中止。
- **读先发生：** 读在所触及的数据或索引范围上留下标记（PostgreSQL 的 SIRead 锁，不阻塞，读完仍保留）。并发事务写进被标记的范围，就记下一条读写依赖。
- **为什么两个方向：** 读者与写者可以按任意顺序提交，后发生的一方必须能看见碰撞。
- **为什么推迟到提交：** 使前提失效的写者可能自己回滚，读者也可能是只读事务。

**面试里这样说。** 「SSI 记录读写依赖，不在发现冲突时立刻中止，而是等提交时看依赖是否可能成环；所以会有误报，应用必须重试。」

**易错。**
- **以为 SIRead 锁会阻塞别人：** 它只做标记，不阻塞。
- **以为发现冲突就立刻中止：** 那会产生更多不必要的中止。
