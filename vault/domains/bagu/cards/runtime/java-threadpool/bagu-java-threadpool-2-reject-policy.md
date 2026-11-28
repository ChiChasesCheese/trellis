---
id: bagu-java-threadpool-2-reject-policy
node: a.runtime.java-threadpool
type: qa
step: 2
---
## Q
**线程池 · 拒绝策略有哪些，CallerRunsPolicy 的风险**｜必会

面试官：「队列满了、线程也到最大了，新任务怎么办？你会选哪种拒绝策略，有什么坑？」

## A
**基本回答。** 内置四种：`AbortPolicy`（默认，抛 `RejectedExecutionException`，调用方明确知道没被接受）、`CallerRunsPolicy`（提交者线程自己执行，提交者被占住就不能继续提交，产生反压）、`DiscardPolicy`（静默丢，最容易让问题悄悄发生）、`DiscardOldestPolicy`（丢队头最老的再重试）。CallerRuns 的反压要看提交者是谁：若是 Tomcat 请求线程，长任务占住它，接口延迟上升甚至耗尽线程；提交者持锁或事务时还会延长持有时间；线程池关闭后它直接丢弃任务。任务不能丢时自定义策略：记录拒绝并告警、返回明确失败或写入 MQ/数据库稍后重试；队列必须有界，上游能降级（返回「系统繁忙」）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 276">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">队列满、线程也到最大后，新任务去哪</text>
<rect x="8" y="28" width="148" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="82.0" y="48.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">AbortPolicy</text>
<text x="164" y="48" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">抛出异常，这是默认策略</text>
<rect x="8" y="72" width="148" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="82.0" y="92.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CallerRunsPolicy</text>
<text x="164" y="92" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">提交任务的线程自己执行</text>
<rect x="8" y="116" width="148" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="82.0" y="136.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">DiscardPolicy</text>
<text x="164" y="136" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">静默丢弃，什么都不说</text>
<rect x="8" y="160" width="148" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="82.0" y="180.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">DiscardOldestPolicy</text>
<text x="164" y="180" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">丢掉队头最老的，再重试</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">CallerRuns：提交者被占住，才有反压</text>
<text x="8" y="234" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">提交者若是请求线程，接口延迟上升</text>
<text x="8" y="256" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">任务不能丢：记录、告警、写入 MQ 重试</text>
</svg>
四种内置策略各一行；高亮的 CallerRuns 让提交者自己干活，有反压，但提交者被占住也有代价。
**举个例子。** 核心 1、最大 1、队列 1，用 `CallerRunsPolicy`（实测）：任务 1 占住唯一线程不结束，任务 2 入队，任务 3 触发拒绝，由 main 自己执行（打印 `task 3 on main`）；main 执行期间无法继续提交，起到反压，若 main 是请求线程，这个请求卡到任务 3 完成。
**业务场景。** 判题线程池用了 CallerRunsPolicy，比赛高峰时 Tomcat 线程自己去执行判题调度，请求线程被耗尽，整站无响应；改成有界队列加快速拒绝并返回「判题繁忙」，其他接口不受影响。
**容易错。**
- **以为 CallerRunsPolicy 一定安全：** 见上，提交者是请求线程时反而拖垮接口。
- **用 DiscardPolicy 当「保护」：** 用户无感知，任务不能丢时要自定义策略。
- **无界队列：** 永远不触发拒绝，把问题推迟到内存耗尽。
