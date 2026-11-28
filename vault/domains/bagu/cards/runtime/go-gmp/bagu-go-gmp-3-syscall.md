---
id: bagu-go-gmp-3-syscall
node: a.runtime.go-gmp
type: qa
step: 3
---
## Q
**Go 调度 · goroutine 阻塞在系统调用时，P 怎么处理**｜必会

面试官：「某个 goroutine 调用了会阻塞的系统调用，比如读磁盘文件，它占着的线程怎么办？其他 goroutine 会被卡住吗？」

## A
**基本回答。** G 进入阻塞的系统调用时，M 跟着阻塞在内核里，阻塞的是线程而不是 P。后台监控线程 sysmon（不需要绑定 P）发现这个 P 停在系统调用里超过一个巡检周期（最短约 20 微秒）、且还有待运行的 G，就把 P 摘走交给另一个 M，其他 G 继续跑。系统调用返回后，G 去拿回 P，拿不到就进全局队列排队。网络 IO 走 epoll，由 netpoller 管理，G 挂起而线程不阻塞；普通文件读写无法 epoll，才占用线程。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 318">
<rect x="10" y="6" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60.0" y="23.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">M0 线程</text>
<rect x="120" y="6" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="23.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">sysmon</text>
<rect x="230" y="6" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="280.0" y="23.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">M1 线程</text>
<line x1="60" y1="32" x2="60" y2="236" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="280" y1="32" x2="280" y2="170" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<rect x="10" y="52" width="100" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="60.0" y="68.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 阻塞的系统</text>
<text x="60.0" y="83.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">调用，卡在内核</text>
<rect x="120" y="112" width="100" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="128.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② P 停得太久</text>
<text x="170.0" y="143.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">且还有 G 在等</text>
<line x1="120" y1="140" x2="62" y2="140" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="62.0,140.0 69.0,136.8 69.0,143.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="230" y="172" width="100" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="280.0" y="188.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 接手这个 P</text>
<text x="280.0" y="203.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">继续跑别的 G</text>
<line x1="170" y1="152" x2="230" y2="192" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="230.0,192.0 222.4,190.8 226.0,185.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="10" y="236" width="100" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60.0" y="252.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 调用返回</text>
<text x="60.0" y="267.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">想拿回 P</text>
<text x="8" y="298" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">拿不到 P → G 进全局队列排队</text>
<text x="130" y="90" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">（最短约 20 微秒）</text>
</svg>
四个角色自左向右：M0 卡在内核里，sysmon 发现 P 停太久，把它交给 M1 继续跑别的 G，M0 回来后想拿回 P。
**业务场景。** 文件存储服务为每个分块上传起一个 goroutine 写本地磁盘，高峰时几千个同时阻塞在写系统调用上，不断新建线程，线程数飙升（默认上限 10000，`debug.SetMaxThreads`，超过直接崩溃），内存和调度开销增大；用带缓冲的 channel 做信号量限制同时落盘的数量后恢复稳定。磁盘 IO 和 cgo 调用都要这样限流。
**容易错。**
- **以为一个阻塞的 G 会卡死整个 P：** P 会被移交。
- **以为所有 IO 都占线程：** 网络 IO 只挂起 G。
