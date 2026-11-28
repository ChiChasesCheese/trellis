---
id: bagu-go-gmp-4-preempt
node: a.runtime.go-gmp
type: qa
step: 4
---
## Q
**Go 调度 · 怎么抢占长时间运行的 goroutine**｜追问

面试官：「如果某个 goroutine 一直在做 CPU 计算，不主动让出，其他 goroutine 会饿死吗？」

## A
**基本回答。** 不会饿死。后台线程 sysmon（不绑定 P）周期性巡检，某个 G 在同一个 P 上连续运行超过 10ms，就向它发抢占请求。Go 1.14 之前只有协作式抢占，函数调用时检查标记，没有函数调用的死循环抢不掉；1.14 起增加基于信号的异步抢占：向线程发 SIGURG，在安全点保存现场并切换，紧循环也能打断。被抢占的 G 回到队列继续运行，只是让出 CPU。GC 要短暂停下所有 G，停不下来的 G 会拖长停顿，所以也依赖抢占。sysmon 还负责回收阻塞在系统调用太久的 P、必要时轮询网络、触发长时间未执行的强制 GC。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 244">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一个 P 上的时间线</text>
<text x="168" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">超过 10ms：发抢占请求</text>
<line x1="168" y1="42" x2="168" y2="50" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="168.0,50.0 164.8,43.0 171.2,43.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="50" width="160" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="88.0" y="69.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">G1：CPU 密集计算</text>
<rect x="168" y="50" width="80" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="208.0" y="69.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">G2</text>
<rect x="248" y="50" width="84" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="290.0" y="69.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">G3</text>
<text x="8" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Go 1.14 之前：协作式抢占</text>
<rect x="8" y="122" width="150" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83.0" y="140.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">函数调用时检查标记</text>
<rect x="170" y="122" width="162" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="251.0" y="140.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">死循环：抢不掉</text>
<text x="8" y="178" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Go 1.14 起：异步抢占</text>
<rect x="8" y="188" width="150" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83.0" y="206.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">sysmon 发 SIGURG 信号</text>
<rect x="190" y="188" width="142" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="261.0" y="206.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">安全点切换</text>
<line x1="158" y1="202" x2="190" y2="202" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="190.0,202.0 183.0,205.2 183.0,198.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="236" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">被抢占的 G 回到队列，之后继续运行</text>
</svg>
上图是 P 上的时间线：G1 连续跑超过 10ms，sysmon 发出抢占请求，换 G2 上场。下面对比两种抢占方式能不能打断死循环。
**业务场景。** 对局服务里引擎算棋是纯 CPU 密集的 goroutine，收发走棋消息的 goroutine 排在同一个 P 的队列里；10ms 的时间片抢占让网络收发不被饿死，对局计时误差保持在毫秒级。要更彻底的隔离，把引擎放到单独进程或服务。
**容易错。**
- **以为 1.14 之前死循环也能被抢占：** 只有协作式时，没有函数调用的紧循环抢不掉。
