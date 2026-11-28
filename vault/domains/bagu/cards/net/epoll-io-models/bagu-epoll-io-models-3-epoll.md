---
id: bagu-epoll-io-models-3-epoll
node: a.net.epoll-io-models
type: qa
step: 3
---
## Q
**epoll · 红黑树加就绪链表为什么高效**｜必会

面试官：「epoll 的原理是什么？为什么能支撑十万连接？」

## A
**基本回答。** 把「登记关心谁」和「等待事件」拆开：`epoll_create` 建实例（一次），`epoll_ctl` 注册、修改、删除 fd，`epoll_wait` 睡眠等待并只返回就绪的 fd。内核用红黑树存已登记的 fd（增删改 O(log n)，也能快速判断是否已登记），数据到达时通过回调把 fd 挂上就绪链表，`epoll_wait` 只取这条链表，复杂度 O(就绪数)，不随总连接数增长，所以连接涨 10 倍每次调用成本基本不变。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<rect x="4" y="6" width="130" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="69" y="19" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">epoll_create</text>
<text x="69" y="35" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">建一个实例</text>
<text x="142" y="27" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只做一次</text>
<rect x="4" y="58" width="130" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="69" y="71" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">epoll_ctl</text>
<text x="69" y="87" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">登记/改/删 fd</text>
<rect x="158" y="44" width="178" height="62" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="247" y="63" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">红黑树</text>
<text x="247" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">所有已登记的 fd</text>
<text x="247" y="95" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">增删改 O(log n)</text>
<line x1="135" y1="75" x2="157" y2="75" stroke-width="1.2" stroke="currentColor"/>
<polygon points="157.0,75.0 150.0,78.2 150.0,71.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="158" y="134" width="178" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="247" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">就绪链表</text>
<text x="247" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只放有数据的 fd</text>
<line x1="247" y1="107" x2="247" y2="133" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="247.0,133.0 243.8,126.0 250.2,126.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="253" y="125" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">数据到了</text>
<rect x="4" y="140" width="130" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="69" y="153" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">epoll_wait</text>
<text x="69" y="169" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只取就绪的</text>
<line x1="157" y1="157" x2="135" y2="157" stroke-width="1.2" stroke="currentColor"/>
<polygon points="135.0,157.0 142.0,153.8 142.0,160.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="4" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">登记一次，状态留在内核，取的时候只拿就绪的</text>
</svg>
左边三个系统调用，右边两个内核结构：登记走红黑树，等待只读就绪链表；数据到达挂链表这一步不需要进程参与。
**业务场景。** 10 万个连接都已登记，某一刻 300 个有数据：内核把它们挂上就绪链表，`epoll_wait` 只带回这 300 个，其余 99700 个空闲连接 CPU 什么也不做。优势来自「连接多、活跃少」，连接很少时与 select 差别不大。
**容易错。**
- **以为 epoll 用哈希表：** 红黑树管登记，就绪链表管通知。
- **以为 epoll_wait 耗时随连接数增长：** 只跟就绪数有关。
- **拿 epoll 监听普通文件：** 文件总是可读，磁盘异步要用 io_uring 或线程池。
