---
id: bagu-go-gmp-1-what-is-gmp
node: a.runtime.go-gmp
type: qa
step: 1
---
## Q
**Go 调度 · G、M、P 各是什么**｜必会

面试官：「Go 的 GMP 调度模型是什么？G、M、P 各代表什么，为什么要有 P？」

## A
**基本回答。** G 是 goroutine，待执行的任务，初始栈约 2KB；M 是 machine，操作系统线程，真正执行代码；P 是 processor，逻辑处理器，持有一个本地运行队列，数量默认等于 CPU 核数（`GOMAXPROCS`）。M 必须绑定一个 P 才能运行 G，所以同时执行 Go 代码的线程最多 P 个；阻塞在系统调用里的 M 不占 P，线程总数可以更多。大量 G 复用少量线程，是 M:N 调度。为什么要有 P：早期只有 G 和 M，所有 G 在一个全局队列里，一把全局锁，线程多了竞争严重；有了 P，多数调度不抢全局锁，本地队列空了去偷别的 P 的任务，线程阻塞在系统调用时 P 也能交给别的线程。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 238">
<rect x="8" y="8" width="324" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="26.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">全局队列：G  G  G  G  G</text>
<rect x="8" y="56" width="150" height="52" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83.0" y="78.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">P0（本地队列）</text>
<text x="83.0" y="93.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">G  G  G</text>
<rect x="182" y="56" width="150" height="52" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="257.0" y="78.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">P1（本地队列）</text>
<text x="257.0" y="93.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">G  G</text>
<rect x="43" y="142" width="80" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83.0" y="160.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">M0 线程</text>
<rect x="217" y="142" width="80" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="257.0" y="160.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">M1 线程</text>
<line x1="83" y1="142" x2="83" y2="108" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="83.0,108.0 86.2,115.0 79.8,115.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="257" y1="142" x2="257" y2="108" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="257.0,108.0 260.2,115.0 253.8,115.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="91" y="130" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">绑定</text>
<text x="265" y="130" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">绑定</text>
<text x="8" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">M2 阻塞在系统调用里：不占 P</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">M 必须绑定 P，才能运行 G</text>
<text x="8" y="230" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">同时跑 Go 代码的 M 最多 P 个</text>
</svg>
每个 P 带一条本地队列，M 绑定 P 才能跑队列里的 G；顶上的全局队列是后备。阻塞在系统调用里的 M 不占 P。
**业务场景。** 12 核机器上的聊天网关（`GOMAXPROCS` 为 12，12 个 P）为 10 万个长连接各起一个读 goroutine，绝大多数阻塞在 channel 或网络读上，不占线程也不占 P；有消息的 G 才进某个 P 的本地队列，同时最多 12 个在跑。实测 10 万个阻塞 goroutine 每个栈约 2051 字节，约 200MB；代价是栈内存，事件循环更省但要自己拆成回调和状态机。
**容易错。**
- **以为容器里 GOMAXPROCS 自动正确：** Go 1.25 起运行时才参考 cgroup 的 CPU 限制；低版本要手动设置或用 automaxprocs。
