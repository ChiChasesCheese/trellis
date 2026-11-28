---
id: bagu-general-method-4-stop-bleed
node: a.linux.general-method
type: qa
step: 4
---
## Q
**止血与留证 · 怎么取舍**｜必会

面试官：「故障还在扩大，你是先止血还是先保留现场？」

## A
**基本回答。** 故障在扩大就先止血，但止血前顺手把现场留住。常见止血：回滚、摘除异常实例、限流、降级、扩容、关闭有问题的定时任务。留证只做快的：监控截图、日志、间隔几秒的多份线程栈。多实例时摘一台出流量专门取证，其余照常恢复。
重启前要留：间隔几秒的三份线程栈、GC 日志、top / vmstat / ss 快照、应用日志；OOM 相关再要堆转储，它会暂停进程，堆越大越久，所以提前配好 OOM 自动转储，别事后手动做。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="80" y="4" width="180" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">故障还在扩大</text>
<rect x="100" y="54" width="140" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="72" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">有多个实例吗？</text>
<line x1="170" y1="33" x2="170" y2="53" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,53.0 166.8,46.0 173.2,46.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="130" y1="83" x2="84" y2="108" stroke-width="1.2" stroke="currentColor"/>
<polygon points="84.0,108.0 88.6,101.8 91.7,107.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="210" y1="83" x2="256" y2="108" stroke-width="1.2" stroke="currentColor"/>
<polygon points="256.0,108.0 248.3,107.5 251.4,101.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="100" y="98" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">有</text>
<text x="240" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">只有一个</text>
<rect x="4" y="110" width="160" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="84" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">摘一台出流量</text>
<text x="84" y="142" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">专门取证</text>
<rect x="176" y="110" width="160" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">快速取三份线程栈</text>
<text x="256" y="142" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">和关键指标</text>
<line x1="84" y1="151" x2="84" y2="169" stroke-width="1.2" stroke="currentColor"/>
<polygon points="84.0,169.0 80.8,162.0 87.2,162.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="256" y1="151" x2="256" y2="169" stroke-width="1.2" stroke="currentColor"/>
<polygon points="256.0,169.0 252.8,162.0 259.2,162.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="4" y="170" width="160" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="84" y="186" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">其余回滚/重启</text>
<text x="84" y="202" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">先恢复服务</text>
<rect x="176" y="170" width="160" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="256" y="186" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">再止血、重启</text>
<text x="256" y="202" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">先留证再重启</text>
<text x="4" y="234" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">留证只做快的：栈、日志、监控截图</text>
<text x="4" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">重启会丢内存现场，所以先留再重启</text>
</svg>
流程从上往下：先判断有几个实例。多个实例时一台留证、其余恢复；只有一个实例时，先快速留证再重启，所以高亮的都是「恢复服务」那一步。
**举个例子。** 扣款服务线程池打满，只剩一个实例：
1. **判断：** 只有一个实例，没法摘一台出来，所以要先留证再恢复。
2. **留证：** 连续取三份线程栈，每份间隔 5 秒，同时保存当前监控截图和日志。
3. **分析：** 三份栈里大多数线程都卡在同一个下游调用上，说明根因在这个依赖。
4. **止血：** 对这个依赖降级，并重启服务，线程池恢复。
5. **结果：** 服务恢复了，同时留下了根因证据，复盘时有据可查。
**容易错。**
- **先重启再说：** 内存里的线程栈和堆没了，根因无从查起，事故会重来。
- **留证拖太久：** 留证只做快的，不要为了取一份完整堆转储让故障扩大。
- **以为扩容总是安全止血：** 扩容可能压垮数据库，重试会放大下游压力。
- **只取一份线程栈：** 一份看不出线程是卡在同一处还是只是路过，要取间隔几秒的多份。
