---
id: bagu-go-leak-mutex-1-leak-mutex
node: b.runtime.go-leak-mutex
type: qa
step: 1
---
## Q
**goroutine 泄漏 · 避免、发现与 Mutex 模式**｜追问

面试官：「服务跑几天内存一直涨，怀疑 goroutine 泄漏：怎么避免、怎么发现？Mutex 是怎么加锁的？」

## A
**基本回答。** 原则：不知道 goroutine 何时结束就不要启动它。每个 goroutine 配退出路径：`context` 超时或取消、或 channel 信号，并在 `select` 里同时等工作和 `ctx.Done()`；`WithCancel`/`WithTimeout`/`WithDeadline` 创建，父 ctx 取消传播给子 ctx，创建者 `defer cancel()`。典型泄漏：向没人接收的无缓冲 channel 发送、从永远不写入或关闭的 channel 接收、HTTP 请求不设超时、`Ticker` 不 `Stop`。发现：`runtime.NumGoroutine()` 持续上涨，再抓 pprof 的 goroutine profile 按调用栈聚合，看大量 goroutine 卡在哪一行；轻微泄漏（一万个漏十个）要对比不同时间点的 profile。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">泄漏：无缓冲 channel，接收方已超时走了</text>
<rect x="8" y="24" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="58.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">已超时返回</text>
<rect x="130" y="24" width="90" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="175.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">无缓冲 ch</text>
<rect x="236" y="24" width="96" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="284.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">子 goroutine</text>
<line x1="236" y1="37" x2="220" y2="37" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="220.0,37.0 226.4,34.1 226.4,39.9" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="10" y="70" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">发送永远等不到人，goroutine 永远卡住</text>
<text x="10" y="92" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">修复：容量为 1 的缓冲 channel</text>
<rect x="8" y="102" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="58.0" y="119.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">已超时返回</text>
<rect x="130" y="102" width="90" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="175.0" y="119.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">缓冲 ch</text>
<rect x="236" y="102" width="96" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="284.0" y="119.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">子 goroutine</text>
<line x1="236" y1="115" x2="220" y2="115" stroke-width="1.2" stroke="currentColor"/>
<polygon points="220.0,115.0 226.4,112.1 226.4,117.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="10" y="148" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">发送放进缓冲就返回，goroutine 正常退出</text>
<line x1="10" y1="162" x2="330" y2="162" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="10" y="180" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Mutex 两种模式</text>
<rect x="8" y="190" width="130" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="73.0" y="208.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">正常模式</text>
<text x="73.0" y="223.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新来者可抢锁，吞吐高</text>
<line x1="138" y1="212" x2="202" y2="212" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="202.0,212.0 195.6,214.9 195.6,209.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="204" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">超 1ms</text>
<rect x="202" y="190" width="130" height="44" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="267.0" y="208.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">饥饿模式</text>
<text x="267.0" y="223.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">锁直接交给队首</text>
<text x="10" y="256" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">队列空了或等得不久，再切回正常模式</text>
</svg>
上半部分：请求超时走了，子 goroutine 往无缓冲 channel 发结果，没人接收，永远卡住；改成容量为 1 的缓冲 channel 就不会。下半部分：Mutex 的两种模式。
**业务场景。** 支付查询接口调下游，用户侧 2 秒超时就返回，下游 3 秒才回，子 goroutine 往无缓冲 channel 发结果，没人接收，永远阻塞；每个超时请求漏一个，几天后内存涨满被杀。实测 100 个带 20ms 超时的请求泄漏 100 个，channel 改容量 1 后为 0；同时监听 `ctx.Done()`，用户取消时也尽早退出。
**Mutex 两种模式。** 正常模式：新来者可与被唤醒的等待者竞争，吞吐高，但等待者可能一直抢不到；等待超过 1ms 切饥饿模式：锁直接交给队首，新来者直接排队，保证公平；队列空了或等待者等得不久再切回。
**容易错。**
- **以为没人管会被 GC 回收：** 阻塞的 goroutine 和它引用的内存都不释放。
- **带超时的 `WaitGroup.Wait`：** 要自己用 channel 加 `select` 实现，别无限等。
