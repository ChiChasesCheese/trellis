---
id: bagu-epoll-io-models-5-reactor
node: a.net.epoll-io-models
type: qa
step: 5
---
## Q
**Reactor 模型 · 单 Reactor 与多 Reactor 怎么选**｜必会

面试官：「Reactor 模型是什么？单 Reactor 和多 Reactor 怎么选？」

## A
**基本回答。** Reactor 是事件循环加分发：一个线程用 epoll 等事件，就绪后分发给处理器去读、算、写。三种形态：单 Reactor 单线程（简单无锁，Redis 这样，但任何慢处理器卡住它管的所有连接，只用一个核）；单 Reactor 加业务线程池（Reactor 只收发，慢业务移出循环，代价是线程间交接、排队和背压要设计）；主从多 Reactor（主只 accept，每个从有自己的 epoll 和线程管一批连接，可用满多核；一个连接固定归一个线程，处理它不用加锁）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="4" y="6" width="90" height="30" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="49" y="25" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新连接</text>
<line x1="95" y1="21" x2="117" y2="21" stroke-width="1.2" stroke="currentColor"/>
<polygon points="117.0,21.0 110.0,24.2 110.0,17.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="118" y="6" width="218" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="227" y="25" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主 Reactor：accept 新连接</text>
<rect x="4" y="62" width="160" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="84" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">从 Reactor 1</text>
<text x="84" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">epoll 管一批连接读写</text>
<rect x="176" y="62" width="160" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">从 Reactor 2</text>
<text x="256" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">epoll 管一批连接读写</text>
<line x1="200" y1="37" x2="100" y2="61" stroke-width="1.2" stroke="currentColor"/>
<polygon points="100.0,61.0 106.1,56.3 107.6,62.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="250" y1="37" x2="250" y2="61" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250.0,61.0 246.8,54.0 253.2,54.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="4" y="132" width="332" height="32" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">业务线程池：查库、鉴权、慢处理</text>
<line x1="84" y1="107" x2="84" y2="131" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<polygon points="84.0,131.0 80.8,124.0 87.2,124.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="256" y1="107" x2="256" y2="131" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<polygon points="256.0,131.0 252.8,124.0 259.2,124.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="4" y="188" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">① 单 Reactor 单线程：简单无锁，慢处理卡全部</text>
<text x="4" y="208" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">② 单 Reactor + 线程池：收发与业务分开</text>
<text x="4" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">③ 主从多 Reactor：多个事件循环并行（图）</text>
<text x="4" y="252" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一个连接固定归一个线程，处理它不用加锁</text>
</svg>
图画的是第三种：主 Reactor 接新连接，两个从 Reactor 各管一批读写，慢活交给业务线程池。每个从 Reactor 仍是单线程，在里面做阻塞调用照样卡住它那一批连接。
**Reactor 与 Proactor。** Reactor 通知「现在可以读了」，由你去读（Linux 的 epoll 加非阻塞 I/O）；Proactor 通知「已读完」，读写由系统异步完成（Windows IOCP、Linux io_uring）。
**业务场景。** 推送网关每个从 Reactor 管 3 万连接，事件循环里直接同步查库，一次慢查询 200 ms，这 3 万个连接全部停顿 200 ms。改成从 Reactor 只收发和编解码，鉴权和查询交给业务线程池，慢查询只占一个业务线程。
**容易错。**
- **以为 Reactor 一定多线程：** 单线程版本（Redis）完全成立。
- **把 Reactor 和 Proactor 说反。**
